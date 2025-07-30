#!/usr/bin/env python3
"""
Enhanced CustomTkinter widget wrappers that add missing functionality
"""

import tkinter as tk
from typing import Optional, Callable, Any, Dict, Union
import threading
import time

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    # Create dummy classes
    class CTkButton: pass
    class CTkEntry: pass
    class CTkLabel: pass
    class CTkFrame: pass
    class CTkCheckBox: pass
    class CTkSlider: pass

from .a11y_engine import speak
from .platform_adapter import set_accessible_name, set_accessible_description


class EnhancedCTKButton(ctk.CTkButton if CTK_AVAILABLE else object):
    """Enhanced CTK Button with proper focus management and accessibility"""
    
    def __init__(self, master, **kwargs):
        # Extract accessibility parameters
        self.accessible_name = kwargs.pop('accessible_name', None)
        self.accessible_description = kwargs.pop('accessible_description', None)
        self.accessible_role = kwargs.pop('accessible_role', 'button')
        
        # Store original command
        self._original_command = kwargs.get('command', None)
        
        # Replace command with our enhanced version
        if self._original_command:
            kwargs['command'] = self._enhanced_command
        
        # Initialize the CTK button
        super().__init__(master, **kwargs)
        
        # Focus management
        self._has_focus = False
        self._focus_callbacks = []
        self._focus_in_callbacks = []
        self._focus_out_callbacks = []
        
        # Set up accessibility
        self._setup_accessibility()
        
        # Set up enhanced focus handling
        self._setup_focus_handling()
        
        # Set up keyboard bindings
        self._setup_keyboard_bindings()
        
        # Register with focus manager
        self._register_with_focus_manager()
    
    def _setup_accessibility(self):
        """Set up accessibility features"""
        if self.accessible_name:
            set_accessible_name(self, self.accessible_name)
        if self.accessible_description:
            set_accessible_description(self, self.accessible_description)
    
    def _setup_focus_handling(self):
        """Set up enhanced focus handling"""
        # Bind focus events to internal widgets
        if hasattr(self, '_text_label'):
            self._text_label.bind('<FocusIn>', self._on_focus_in, add='+')
            self._text_label.bind('<FocusOut>', self._on_focus_out, add='+')
        
        if hasattr(self, '_canvas'):
            self._canvas.bind('<FocusIn>', self._on_focus_in, add='+')
            self._canvas.bind('<FocusOut>', self._on_focus_out, add='+')
        
        # Make the button itself focusable
        self.bind('<FocusIn>', self._on_focus_in, add='+')
        self.bind('<FocusOut>', self._on_focus_out, add='+')
    
    def _setup_keyboard_bindings(self):
        """Set up keyboard bindings for accessibility"""
        # Bind to all internal widgets that can receive focus
        widgets_to_bind = [self]
        
        if hasattr(self, '_text_label'):
            widgets_to_bind.append(self._text_label)
        if hasattr(self, '_canvas'):
            widgets_to_bind.append(self._canvas)
        
        for widget in widgets_to_bind:
            try:
                # Space and Enter should activate the button
                widget.bind('<KeyPress-space>', self._on_key_activate, add='+')
                widget.bind('<KeyPress-Return>', self._on_key_activate, add='+')
                
                # Tab navigation (let the focus manager handle this)
                widget.bind('<KeyPress-Tab>', self._on_tab, add='+')
                widget.bind('<KeyPress-Shift-Tab>', self._on_shift_tab, add='+')
                
            except tk.TclError:
                # Some widgets might not support binding
                pass
    
    def _enhanced_command(self):
        """Enhanced command that includes accessibility feedback"""
        # Announce button activation
        if self.accessible_name:
            speak(f"{self.accessible_name} activated")
        
        # Call original command
        if self._original_command:
            try:
                self._original_command()
            except Exception as e:
                print(f"Error in button command: {e}")
    
    def _on_focus_in(self, event):
        """Handle focus in events"""
        if not self._has_focus:
            self._has_focus = True
            
            # Announce focus
            if self.accessible_name:
                announcement = f"{self.accessible_name}, button"
                if self.accessible_description:
                    announcement += f", {self.accessible_description}"
                speak(announcement)
            
            # Call focus callbacks
            for callback in self._focus_in_callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
            
            # Generate virtual FocusIn event for the button itself
            self.event_generate('<FocusIn>')
    
    def _on_focus_out(self, event):
        """Handle focus out events"""
        if self._has_focus:
            self._has_focus = False
            
            # Call focus callbacks
            for callback in self._focus_out_callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
            
            # Generate virtual FocusOut event for the button itself
            self.event_generate('<FocusOut>')
    
    def _on_key_activate(self, event):
        """Handle keyboard activation (Space/Enter)"""
        if self._has_focus:
            self._enhanced_command()
            return 'break'
    
    def _on_tab(self, event):
        """Handle Tab key - let focus manager handle it"""
        return None  # Don't break, let it propagate
    
    def _on_shift_tab(self, event):
        """Handle Shift+Tab key - let focus manager handle it"""
        return None  # Don't break, let it propagate
    
    def focus_set(self):
        """Enhanced focus_set that works properly"""
        try:
            # Try to focus the text label first (most reliable for CTK buttons)
            if hasattr(self, '_text_label'):
                self._text_label.focus_set()
                return
            
            # Fallback to canvas
            if hasattr(self, '_canvas'):
                self._canvas.focus_set()
                return
            
            # Last resort - standard focus
            super().focus_set()
            
        except Exception:
            # If all else fails, try the parent focus_set
            try:
                super().focus_set()
            except Exception:
                pass
    
    def focus_force(self):
        """Enhanced focus_force"""
        try:
            if hasattr(self, '_text_label'):
                self._text_label.focus_force()
            elif hasattr(self, '_canvas'):
                self._canvas.focus_force()
            else:
                super().focus_force()
        except Exception:
            try:
                super().focus_force()
            except Exception:
                pass
    
    def add_focus_callback(self, callback: Callable):
        """Add a callback for focus events"""
        if callback not in self._focus_callbacks:
            self._focus_callbacks.append(callback)
            self._focus_in_callbacks.append(callback)
    
    def remove_focus_callback(self, callback: Callable):
        """Remove a focus callback"""
        if callback in self._focus_callbacks:
            self._focus_callbacks.remove(callback)
        if callback in self._focus_in_callbacks:
            self._focus_in_callbacks.remove(callback)
    
    def has_focus(self) -> bool:
        """Check if this widget has focus"""
        return self._has_focus
    
    def configure(self, **kwargs):
        """Enhanced configure that handles accessibility attributes"""
        # Handle accessibility attributes
        if 'accessible_name' in kwargs:
            self.accessible_name = kwargs.pop('accessible_name')
            set_accessible_name(self, self.accessible_name)
        
        if 'accessible_description' in kwargs:
            self.accessible_description = kwargs.pop('accessible_description')
            set_accessible_description(self, self.accessible_description)
        
        if 'command' in kwargs:
            self._original_command = kwargs['command']
            kwargs['command'] = self._enhanced_command
        
        # Call parent configure
        super().configure(**kwargs)
    
    def _register_with_focus_manager(self):
        """Register this widget with the focus manager"""
        try:
            from .focus_manager import get_focus_manager
            root = self.winfo_toplevel()
            focus_manager = get_focus_manager(root)
            focus_manager.register_widget(self)
        except (AttributeError, ImportError, tk.TclError):
            # Focus manager not available or widget not ready
            pass


class EnhancedCTKEntry(ctk.CTkEntry if CTK_AVAILABLE else object):
    """Enhanced CTK Entry with proper focus management and accessibility"""
    
    def __init__(self, master, **kwargs):
        # Extract accessibility parameters
        self.accessible_name = kwargs.pop('accessible_name', None)
        self.accessible_description = kwargs.pop('accessible_description', None)
        self.accessible_role = kwargs.pop('accessible_role', 'textbox')
        
        # Initialize the CTK entry
        super().__init__(master, **kwargs)
        
        # Focus management
        self._has_focus = False
        self._focus_callbacks = []
        self._focus_in_callbacks = []
        self._focus_out_callbacks = []
        
        # Set up accessibility
        self._setup_accessibility()
        
        # Set up enhanced focus handling
        self._setup_focus_handling()
        
        # Register with focus manager
        self._register_with_focus_manager()
    
    def _setup_accessibility(self):
        """Set up accessibility features"""
        if self.accessible_name:
            set_accessible_name(self, self.accessible_name)
        if self.accessible_description:
            set_accessible_description(self, self.accessible_description)
    
    def _setup_focus_handling(self):
        """Set up enhanced focus handling"""
        # Bind focus events to internal entry widget
        if hasattr(self, '_entry'):
            self._entry.bind('<FocusIn>', self._on_focus_in, add='+')
            self._entry.bind('<FocusOut>', self._on_focus_out, add='+')
        
        # Also bind to the main widget
        self.bind('<FocusIn>', self._on_focus_in, add='+')
        self.bind('<FocusOut>', self._on_focus_out, add='+')
    
    def _on_focus_in(self, event):
        """Handle focus in events"""
        if not self._has_focus:
            self._has_focus = True
            
            # Announce focus
            if self.accessible_name:
                announcement = f"{self.accessible_name}, text field"
                if self.accessible_description:
                    announcement += f", {self.accessible_description}"
                
                # Include current value if any
                current_value = self.get()
                if current_value:
                    announcement += f", current value: {current_value}"
                
                speak(announcement)
            
            # Call focus callbacks
            for callback in self._focus_in_callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
            
            # Generate virtual FocusIn event
            self.event_generate('<FocusIn>')
    
    def _on_focus_out(self, event):
        """Handle focus out events"""
        if self._has_focus:
            self._has_focus = False
            
            # Call focus callbacks
            for callback in self._focus_out_callbacks:
                try:
                    callback(self)
                except Exception:
                    pass
            
            # Generate virtual FocusOut event
            self.event_generate('<FocusOut>')
    
    def focus_set(self):
        """Enhanced focus_set that works properly"""
        try:
            # Focus the internal entry widget
            if hasattr(self, '_entry'):
                self._entry.focus_set()
                return
            
            # Fallback to standard focus
            super().focus_set()
            
        except Exception:
            try:
                super().focus_set()
            except Exception:
                pass
    
    def focus_force(self):
        """Enhanced focus_force"""
        try:
            if hasattr(self, '_entry'):
                self._entry.focus_force()
            else:
                super().focus_force()
        except Exception:
            try:
                super().focus_force()
            except Exception:
                pass
    
    def add_focus_callback(self, callback: Callable):
        """Add a callback for focus events"""
        if callback not in self._focus_callbacks:
            self._focus_callbacks.append(callback)
            self._focus_in_callbacks.append(callback)
    
    def remove_focus_callback(self, callback: Callable):
        """Remove a focus callback"""
        if callback in self._focus_callbacks:
            self._focus_callbacks.remove(callback)
        if callback in self._focus_in_callbacks:
            self._focus_in_callbacks.remove(callback)
    
    def has_focus(self) -> bool:
        """Check if this widget has focus"""
        return self._has_focus
    
    def configure(self, **kwargs):
        """Enhanced configure that handles accessibility attributes"""
        # Handle accessibility attributes
        if 'accessible_name' in kwargs:
            self.accessible_name = kwargs.pop('accessible_name')
            set_accessible_name(self, self.accessible_name)
        
        if 'accessible_description' in kwargs:
            self.accessible_description = kwargs.pop('accessible_description')
            set_accessible_description(self, self.accessible_description)
        
        # Call parent configure
        super().configure(**kwargs)
    
    def _register_with_focus_manager(self):
        """Register this widget with the focus manager"""
        try:
            from .focus_manager import get_focus_manager
            root = self.winfo_toplevel()
            focus_manager = get_focus_manager(root)
            focus_manager.register_widget(self)
        except (AttributeError, ImportError, tk.TclError):
            # Focus manager not available or widget not ready
            pass


# Create aliases for easier importing
if CTK_AVAILABLE:
    AccessibleCTKButton = EnhancedCTKButton
    AccessibleCTKEntry = EnhancedCTKEntry
else:
    AccessibleCTKButton = None
    AccessibleCTKEntry = None