#!/usr/bin/env python3
"""
Comprehensive Demo Application for tkaria11y
============================================

This application demonstrates all accessible widgets available in tkaria11y
across three frameworks: tkinter, ttk, and customtkinter.

Features:
- All accessible widgets with proper ARIA labels
- Text-to-speech feedback
- Keyboard navigation
- High-contrast themes
- Comprehensive widget showcase

Usage:
    python comprehensive_demo.py
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from tkaria11y.app import AccessibleApp
from tkaria11y.a11y_engine import speak
from tkaria11y.widgets import (
    # Standard Tkinter widgets
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleText,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleScrollbar,
    AccessibleListbox,
    AccessibleFrame,
    AccessibleLabelFrame,
    AccessibleCanvas,
    AccessibleMessage,
    AccessibleSpinbox,
    AccessiblePanedWindow,
    # TTK widgets
    AccessibleTTKButton,
    AccessibleTTKEntry,
    AccessibleTTKLabel,
    AccessibleTTKCheckbutton,
    AccessibleTTKRadiobutton,
    AccessibleTTKScale,
    AccessibleTTKScrollbar,
    AccessibleTTKFrame,
    AccessibleTTKLabelFrame,
    AccessibleNotebook,
    AccessibleTTKProgressbar,
    AccessibleTTKSeparator,
    AccessibleTreeview,
    AccessibleCombobox,
    AccessibleTTKSpinbox,
    AccessibleTTKPanedWindow,
    # CustomTkinter widgets (optional)
    AccessibleCTKButton,
    AccessibleCTKEntry,
    AccessibleCTKLabel,
    AccessibleCTKCheckBox,
    AccessibleCTKRadioButton,
    AccessibleCTKSlider,
    AccessibleCTKScrollbar,
    AccessibleCTKFrame,
    AccessibleCTKTabview,
    AccessibleCTKProgressBar,
    AccessibleCTKSwitch,
    AccessibleCTKComboBox,
    AccessibleCTKTextbox,
    AccessibleCTKScrollableFrame,
    CTK_AVAILABLE,
)

try:
    import customtkinter as ctk

    CTK_AVAILABLE = True
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
except ImportError:
    CTK_AVAILABLE = False
    print("CustomTkinter not available. CTK widgets will be disabled.")


class ComprehensiveDemoApp(AccessibleApp):
    """Comprehensive demo application showcasing all tkaria11y widgets."""

    def __init__(self):
        super().__init__(
            title="tkaria11y Comprehensive Widget Demo", high_contrast=True
        )

        # Set window geometry
        self.geometry("1200x800")

        # Application state
        self.current_tab = 0
        self.demo_data = []

        # Create the main interface
        self.create_menu()
        self.create_main_interface()
        self.populate_demo_data()

        # Enable keyboard shortcuts
        self.bind_keyboard_shortcuts()

    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Demo Data", command=self.new_demo_data)
        file_menu.add_command(label="Load Demo Data", command=self.load_demo_data)
        file_menu.add_command(label="Save Demo Data", command=self.save_demo_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        view_menu.add_command(label="Toggle TTS", command=self.toggle_tts)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)

    def toggle_theme(self):
        """Toggle between high contrast and normal theme."""
        if self.is_high_contrast_enabled():
            self.disable_high_contrast()
            speak("Normal theme enabled")
        else:
            self.enable_high_contrast()
            speak("High contrast theme enabled")

    def toggle_tts(self):
        """Toggle text-to-speech on/off."""
        # This would typically toggle TTS settings
        speak("Text-to-speech toggle - feature not implemented in demo")

    def create_main_interface(self):
        """Create the main tabbed interface."""
        # Create main notebook for different widget categories
        self.main_notebook = AccessibleNotebook(
            self, accessible_name="Main Widget Categories"
        )
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs for different widget types
        self.create_tkinter_tab()
        self.create_ttk_tab()
        if CTK_AVAILABLE:
            try:
                self.create_ctk_tab_simple()
            except Exception as e:
                print(f"Warning: Could not create CustomTkinter tab: {e}")
                # Create a placeholder tab instead
                self.create_ctk_placeholder_tab()
        self.create_demo_tab()

    def create_tkinter_tab(self):
        """Create tab showcasing standard Tkinter widgets."""
        tk_frame = AccessibleTTKFrame(self.main_notebook)
        self.main_notebook.add(tk_frame, text="Tkinter Widgets")

        # Create scrollable area
        canvas = AccessibleCanvas(tk_frame, accessible_name="Tkinter Widgets Canvas")
        scrollbar = AccessibleScrollbar(
            tk_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = AccessibleFrame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons section
        buttons_frame = AccessibleLabelFrame(
            scrollable_frame, text="Buttons", accessible_name="Button Widgets Section"
        )
        buttons_frame.pack(fill="x", padx=10, pady=5)

        AccessibleButton(
            buttons_frame,
            text="Standard Button",
            accessible_name="Standard Button Example",
            command=lambda: self.show_message("Standard Button clicked!"),
        ).pack(side="left", padx=5, pady=5)

        AccessibleButton(
            buttons_frame,
            text="Disabled Button",
            accessible_name="Disabled Button Example",
            state="disabled",
        ).pack(side="left", padx=5, pady=5)

        # Entry and Text section
        input_frame = AccessibleLabelFrame(
            scrollable_frame,
            text="Text Input",
            accessible_name="Text Input Widgets Section",
        )
        input_frame.pack(fill="x", padx=10, pady=5)

        AccessibleLabel(
            input_frame, text="Name:", accessible_name="Name Input Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.tk_name_entry = AccessibleEntry(
            input_frame, accessible_name="Name Input Field"
        )
        self.tk_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleLabel(
            input_frame, text="Comments:", accessible_name="Comments Input Label"
        ).grid(row=1, column=0, sticky="nw", padx=5, pady=2)

        self.tk_text = AccessibleText(
            input_frame, height=4, width=40, accessible_name="Comments Text Area"
        )
        self.tk_text.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        input_frame.columnconfigure(1, weight=1)

        # Checkbuttons and Radiobuttons
        selection_frame = AccessibleLabelFrame(
            scrollable_frame,
            text="Selection Widgets",
            accessible_name="Selection Widgets Section",
        )
        selection_frame.pack(fill="x", padx=10, pady=5)

        # Checkbuttons
        check_frame = AccessibleFrame(selection_frame)
        check_frame.pack(side="left", fill="both", expand=True)

        AccessibleLabel(
            check_frame, text="Options:", accessible_name="Checkbutton Options Label"
        ).pack(anchor="w")

        self.tk_check_vars = []
        for i, option in enumerate(["Option 1", "Option 2", "Option 3"]):
            var = tk.BooleanVar()
            self.tk_check_vars.append(var)
            AccessibleCheckbutton(
                check_frame,
                text=option,
                variable=var,
                accessible_name=f"Checkbox for {option}",
                command=lambda opt=option: self.on_checkbox_change(opt),
            ).pack(anchor="w")

        # Radiobuttons
        radio_frame = AccessibleFrame(selection_frame)
        radio_frame.pack(side="right", fill="both", expand=True)

        AccessibleLabel(
            radio_frame,
            text="Choose one:",
            accessible_name="Radio Button Options Label",
        ).pack(anchor="w")

        self.tk_radio_var = tk.StringVar(value="Choice 1")
        for choice in ["Choice 1", "Choice 2", "Choice 3"]:
            AccessibleRadiobutton(
                radio_frame,
                text=choice,
                variable=self.tk_radio_var,
                value=choice,
                accessible_name=f"Radio button for {choice}",
                command=lambda: self.on_radio_change(self.tk_radio_var.get()),
            ).pack(anchor="w")

        # Scale and Spinbox
        numeric_frame = AccessibleLabelFrame(
            scrollable_frame,
            text="Numeric Input",
            accessible_name="Numeric Input Widgets Section",
        )
        numeric_frame.pack(fill="x", padx=10, pady=5)

        AccessibleLabel(
            numeric_frame, text="Scale (0-100):", accessible_name="Scale Widget Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.tk_scale = AccessibleScale(
            numeric_frame,
            from_=0,
            to=100,
            orient="horizontal",
            accessible_name="Value Scale from 0 to 100",
            command=self.on_scale_change,
        )
        self.tk_scale.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleLabel(
            numeric_frame, text="Spinbox:", accessible_name="Spinbox Widget Label"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.tk_spinbox = AccessibleSpinbox(
            numeric_frame, from_=0, to=10, accessible_name="Number Spinbox from 0 to 10"
        )
        self.tk_spinbox.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        numeric_frame.columnconfigure(1, weight=1)

        # Listbox
        list_frame = AccessibleLabelFrame(
            scrollable_frame,
            text="List Selection",
            accessible_name="List Selection Widgets Section",
        )
        list_frame.pack(fill="x", padx=10, pady=5)

        AccessibleLabel(
            list_frame, text="Select items:", accessible_name="Listbox Selection Label"
        ).pack(anchor="w")

        listbox_frame = AccessibleFrame(list_frame)
        listbox_frame.pack(fill="both", expand=True)

        self.tk_listbox = AccessibleListbox(
            listbox_frame,
            selectmode="extended",
            accessible_name="Multi-selection List of Items",
        )
        list_scrollbar = AccessibleScrollbar(
            listbox_frame, orient="vertical", command=self.tk_listbox.yview
        )
        self.tk_listbox.configure(yscrollcommand=list_scrollbar.set)

        self.tk_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        # Populate listbox
        for i in range(20):
            self.tk_listbox.insert("end", f"List Item {i+1}")

        self.tk_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def create_ttk_tab(self):
        """Create tab showcasing TTK widgets."""
        ttk_frame = AccessibleTTKFrame(self.main_notebook)
        self.main_notebook.add(ttk_frame, text="TTK Widgets")

        # Create scrollable area
        canvas = AccessibleCanvas(ttk_frame, accessible_name="TTK Widgets Canvas")
        scrollbar = AccessibleTTKScrollbar(
            ttk_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = AccessibleTTKFrame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # TTK Buttons
        ttk_buttons_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="TTK Buttons",
            accessible_name="TTK Button Widgets Section",
        )
        ttk_buttons_frame.pack(fill="x", padx=10, pady=5)

        AccessibleTTKButton(
            ttk_buttons_frame,
            text="TTK Button",
            accessible_name="TTK Button Example",
            command=lambda: self.show_message("TTK Button clicked!"),
        ).pack(side="left", padx=5, pady=5)

        AccessibleTTKButton(
            ttk_buttons_frame,
            text="Disabled TTK",
            accessible_name="Disabled TTK Button Example",
            state="disabled",
        ).pack(side="left", padx=5, pady=5)

        # TTK Entry and Combobox
        ttk_input_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="TTK Input Widgets",
            accessible_name="TTK Input Widgets Section",
        )
        ttk_input_frame.pack(fill="x", padx=10, pady=5)

        AccessibleTTKLabel(
            ttk_input_frame, text="TTK Entry:", accessible_name="TTK Entry Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ttk_entry = AccessibleTTKEntry(
            ttk_input_frame, accessible_name="TTK Entry Field"
        )
        self.ttk_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleTTKLabel(
            ttk_input_frame, text="Combobox:", accessible_name="Combobox Label"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.ttk_combobox = AccessibleCombobox(
            ttk_input_frame,
            values=["Option A", "Option B", "Option C", "Option D"],
            accessible_name="Selection Combobox",
        )
        self.ttk_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.ttk_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        ttk_input_frame.columnconfigure(1, weight=1)

        # TTK Selection widgets
        ttk_selection_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="TTK Selection",
            accessible_name="TTK Selection Widgets Section",
        )
        ttk_selection_frame.pack(fill="x", padx=10, pady=5)

        # TTK Checkbuttons
        ttk_check_frame = AccessibleTTKFrame(ttk_selection_frame)
        ttk_check_frame.pack(side="left", fill="both", expand=True)

        AccessibleTTKLabel(
            ttk_check_frame,
            text="TTK Options:",
            accessible_name="TTK Checkbutton Options Label",
        ).pack(anchor="w")

        self.ttk_check_vars = []
        for i, option in enumerate(["TTK Option 1", "TTK Option 2", "TTK Option 3"]):
            var = tk.BooleanVar()
            self.ttk_check_vars.append(var)
            AccessibleTTKCheckbutton(
                ttk_check_frame,
                text=option,
                variable=var,
                accessible_name=f"TTK Checkbox for {option}",
                command=lambda opt=option: self.on_checkbox_change(opt),
            ).pack(anchor="w")

        # TTK Radiobuttons
        ttk_radio_frame = AccessibleTTKFrame(ttk_selection_frame)
        ttk_radio_frame.pack(side="right", fill="both", expand=True)

        AccessibleTTKLabel(
            ttk_radio_frame,
            text="TTK Choose one:",
            accessible_name="TTK Radio Button Options Label",
        ).pack(anchor="w")

        self.ttk_radio_var = tk.StringVar(value="TTK Choice 1")
        for choice in ["TTK Choice 1", "TTK Choice 2", "TTK Choice 3"]:
            AccessibleTTKRadiobutton(
                ttk_radio_frame,
                text=choice,
                variable=self.ttk_radio_var,
                value=choice,
                accessible_name=f"TTK Radio button for {choice}",
                command=lambda: self.on_radio_change(self.ttk_radio_var.get()),
            ).pack(anchor="w")

        # TTK Scale and Spinbox
        ttk_numeric_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="TTK Numeric",
            accessible_name="TTK Numeric Input Widgets Section",
        )
        ttk_numeric_frame.pack(fill="x", padx=10, pady=5)

        AccessibleTTKLabel(
            ttk_numeric_frame,
            text="TTK Scale:",
            accessible_name="TTK Scale Widget Label",
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ttk_scale = AccessibleTTKScale(
            ttk_numeric_frame,
            from_=0,
            to=100,
            orient="horizontal",
            accessible_name="TTK Value Scale from 0 to 100",
            command=self.on_scale_change,
        )
        self.ttk_scale.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleTTKLabel(
            ttk_numeric_frame,
            text="TTK Spinbox:",
            accessible_name="TTK Spinbox Widget Label",
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.ttk_spinbox = AccessibleTTKSpinbox(
            ttk_numeric_frame,
            from_=0,
            to=10,
            accessible_name="TTK Number Spinbox from 0 to 10",
        )
        self.ttk_spinbox.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk_numeric_frame.columnconfigure(1, weight=1)

        # TTK Progressbar
        progress_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="Progress Indicators",
            accessible_name="Progress Indicator Widgets Section",
        )
        progress_frame.pack(fill="x", padx=10, pady=5)

        AccessibleTTKLabel(
            progress_frame, text="Progress:", accessible_name="Progress Bar Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ttk_progress = AccessibleTTKProgressbar(
            progress_frame,
            length=300,
            mode="determinate",
            accessible_name="Progress Bar Indicator",
        )
        self.ttk_progress.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleTTKButton(
            progress_frame,
            text="Start Progress",
            accessible_name="Start Progress Button",
            command=self.start_progress,
        ).grid(row=0, column=2, padx=5, pady=2)

        progress_frame.columnconfigure(1, weight=1)

        # TTK Treeview
        tree_frame = AccessibleTTKLabelFrame(
            scrollable_frame,
            text="Tree View",
            accessible_name="Tree View Widget Section",
        )
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create treeview with scrollbars
        tree_container = AccessibleTTKFrame(tree_frame)
        tree_container.pack(fill="both", expand=True)

        self.ttk_tree = AccessibleTreeview(
            tree_container,
            columns=("Name", "Type", "Size"),
            show="tree headings",
            accessible_name="File System Tree View",
        )

        # Configure columns
        self.ttk_tree.heading("#0", text="Item")
        self.ttk_tree.heading("Name", text="Name")
        self.ttk_tree.heading("Type", text="Type")
        self.ttk_tree.heading("Size", text="Size")

        self.ttk_tree.column("#0", width=150)
        self.ttk_tree.column("Name", width=200)
        self.ttk_tree.column("Type", width=100)
        self.ttk_tree.column("Size", width=100)

        tree_v_scroll = AccessibleTTKScrollbar(
            tree_container, orient="vertical", command=self.ttk_tree.yview
        )
        tree_h_scroll = AccessibleTTKScrollbar(
            tree_container, orient="horizontal", command=self.ttk_tree.xview
        )

        self.ttk_tree.configure(
            yscrollcommand=tree_v_scroll.set, xscrollcommand=tree_h_scroll.set
        )

        self.ttk_tree.grid(row=0, column=0, sticky="nsew")
        tree_v_scroll.grid(row=0, column=1, sticky="ns")
        tree_h_scroll.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Populate treeview
        self.populate_treeview()

        # Separator
        AccessibleTTKSeparator(scrollable_frame, orient="horizontal").pack(
            fill="x", padx=10, pady=10
        )

    def create_ctk_placeholder_tab(self):
        """Create placeholder tab when CustomTkinter has issues."""
        ctk_frame = AccessibleTTKFrame(self.main_notebook)
        self.main_notebook.add(ctk_frame, text="CustomTkinter (Unavailable)")

        AccessibleLabel(
            ctk_frame,
            text="CustomTkinter widgets are not available",
            font=("Arial", 16, "bold"),
            accessible_name="CustomTkinter Unavailable Message",
        ).pack(pady=50)

        AccessibleLabel(
            ctk_frame,
            text="This could be due to:\n• CustomTkinter not installed\n• Compatibility issues\n• Missing dependencies",
            justify="left",
            accessible_name="CustomTkinter Issues Explanation",
        ).pack(pady=20)

        AccessibleButton(
            ctk_frame,
            text="Install CustomTkinter",
            accessible_name="Install CustomTkinter Button",
            command=lambda: speak(
                "To install CustomTkinter, run: pip install customtkinter"
            ),
        ).pack(pady=10)

    def create_ctk_tab_simple(self):
        """Create CustomTkinter tab with full accessibility support."""
        if not CTK_AVAILABLE:
            return
        
        # Create a regular Tkinter frame for the tab
        ctk_frame = AccessibleFrame(self.main_notebook)
        self.main_notebook.add(ctk_frame, text="CustomTkinter Widgets")

        # Create a label explaining the new functionality
        AccessibleLabel(
            ctk_frame,
            text="CustomTkinter Demo (Full Accessibility)",
            font=("Arial", 14, "bold"),
            accessible_name="CustomTkinter Demo Section",
        ).pack(pady=10)

        AccessibleLabel(
            ctk_frame,
            text="These CustomTkinter widgets now have full accessibility support\nwith focus indicators, screen reader announcements, and keyboard navigation.",
            justify="center",
            accessible_name="CustomTkinter Features Notice",
        ).pack(pady=5)

        # Create accessible CustomTkinter demo
        container_frame = AccessibleFrame(ctk_frame)
        container_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        demo_frame = AccessibleCTKFrame(
            container_frame,
            accessible_name="CustomTkinter Demo Container"
        )
        demo_frame.pack(fill="both", expand=True)

        # Accessible CTK Button
        ctk_button = AccessibleCTKButton(
            demo_frame,
            text="Accessible CTK Button",
            accessible_name="CustomTkinter Button",
            accessible_description="Click to test CustomTkinter button accessibility",
            command=lambda: speak("Accessible CustomTkinter button clicked!")
        )
        ctk_button.pack(pady=10)

        # Accessible CTK Entry
        ctk_entry = AccessibleCTKEntry(
            demo_frame,
            placeholder_text="Type here...",
            accessible_name="CustomTkinter Entry Field",
            accessible_description="Text input field with accessibility support"
        )
        ctk_entry.pack(pady=10)

        # Accessible CTK Label
        ctk_label = AccessibleCTKLabel(
            demo_frame,
            text="Accessible CTK Label",
            accessible_name="CustomTkinter Label",
            accessible_description="This label has full accessibility support"
        )
        ctk_label.pack(pady=10)

        # Accessible CTK Checkbox
        ctk_checkbox = AccessibleCTKCheckBox(
            demo_frame,
            text="Accessible CTK Checkbox",
            accessible_name="CustomTkinter Checkbox",
            accessible_description="Checkbox with accessibility announcements"
        )
        ctk_checkbox.pack(pady=10)

        # Accessible CTK Slider
        ctk_slider = AccessibleCTKSlider(
            demo_frame,
            from_=0,
            to=100,
            accessible_name="CustomTkinter Slider",
            accessible_description="Slider with value announcements"
        )
        ctk_slider.pack(pady=10)

        # Instructions
        AccessibleLabel(
            ctk_frame,
            text="These CustomTkinter widgets now have full accessibility support:\n• Focus indicators\n• Screen reader announcements\n• Keyboard navigation\n• State change notifications",
            justify="center",
            accessible_name="CustomTkinter Accessibility Features",
        ).pack(pady=10)

    def create_ctk_tab_original(self):
        """Create tab showcasing CustomTkinter widgets."""
        if not CTK_AVAILABLE:
            return

        ctk_frame = AccessibleCTKFrame(self.main_notebook)
        self.main_notebook.add(ctk_frame, text="CustomTkinter Widgets")

        # Create scrollable frame
        self.ctk_scrollable = AccessibleCTKScrollableFrame(
            ctk_frame, accessible_name="CustomTkinter Widgets Scrollable Area"
        )
        self.ctk_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # CTK Buttons
        ctk_buttons_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_buttons_frame.pack(fill="x", pady=10)

        AccessibleCTKLabel(
            ctk_buttons_frame,
            text="CTK Buttons:",
            accessible_name="CTK Buttons Section Label",
        ).pack(anchor="w")

        button_container = AccessibleCTKFrame(ctk_buttons_frame)
        button_container.pack(fill="x", pady=5)

        AccessibleCTKButton(
            button_container,
            text="CTK Button",
            accessible_name="CTK Button Example",
            command=lambda: self.show_message("CTK Button clicked!"),
        ).pack(side="left", padx=5)

        AccessibleCTKButton(
            button_container,
            text="Disabled CTK",
            accessible_name="Disabled CTK Button Example",
            state="disabled",
        ).pack(side="left", padx=5)

        # CTK Input widgets
        ctk_input_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_input_frame.pack(fill="x", pady=10)

        AccessibleCTKLabel(
            ctk_input_frame,
            text="CTK Input:",
            accessible_name="CTK Input Section Label",
        ).pack(anchor="w")

        input_container = AccessibleCTKFrame(ctk_input_frame)
        input_container.pack(fill="x", pady=5)

        AccessibleCTKLabel(
            input_container, text="Entry:", accessible_name="CTK Entry Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ctk_entry = AccessibleCTKEntry(
            input_container,
            placeholder_text="Enter text here...",
            accessible_name="CTK Entry Field",
        )
        self.ctk_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleCTKLabel(
            input_container, text="Textbox:", accessible_name="CTK Textbox Label"
        ).grid(row=1, column=0, sticky="nw", padx=5, pady=2)

        self.ctk_textbox = AccessibleCTKTextbox(
            input_container, height=100, accessible_name="CTK Text Area"
        )
        self.ctk_textbox.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        AccessibleCTKLabel(
            input_container, text="ComboBox:", accessible_name="CTK ComboBox Label"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=2)

        self.ctk_combobox = AccessibleCTKComboBox(
            input_container,
            values=["CTK Option 1", "CTK Option 2", "CTK Option 3"],
            accessible_name="CTK Selection ComboBox",
        )
        self.ctk_combobox.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        input_container.columnconfigure(1, weight=1)

        # CTK Selection widgets
        ctk_selection_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_selection_frame.pack(fill="x", pady=10)

        AccessibleCTKLabel(
            ctk_selection_frame,
            text="CTK Selection:",
            accessible_name="CTK Selection Section Label",
        ).pack(anchor="w")

        selection_container = AccessibleCTKFrame(ctk_selection_frame)
        selection_container.pack(fill="x", pady=5)

        # CTK Checkboxes
        check_container = AccessibleCTKFrame(selection_container)
        check_container.pack(side="left", fill="both", expand=True)

        AccessibleCTKLabel(
            check_container,
            text="CheckBoxes:",
            accessible_name="CTK CheckBox Options Label",
        ).pack(anchor="w")

        self.ctk_check_vars = []
        for i, option in enumerate(["CTK Check 1", "CTK Check 2", "CTK Check 3"]):
            var = tk.BooleanVar()
            self.ctk_check_vars.append(var)
            AccessibleCTKCheckBox(
                check_container,
                text=option,
                variable=var,
                accessible_name=f"CTK Checkbox for {option}",
                command=lambda opt=option: self.on_checkbox_change(opt),
            ).pack(anchor="w", pady=2)

        # CTK RadioButtons
        radio_container = AccessibleCTKFrame(selection_container)
        radio_container.pack(side="right", fill="both", expand=True)

        AccessibleCTKLabel(
            radio_container,
            text="RadioButtons:",
            accessible_name="CTK RadioButton Options Label",
        ).pack(anchor="w")

        self.ctk_radio_var = tk.StringVar(value="CTK Radio 1")
        for choice in ["CTK Radio 1", "CTK Radio 2", "CTK Radio 3"]:
            AccessibleCTKRadioButton(
                radio_container,
                text=choice,
                variable=self.ctk_radio_var,
                value=choice,
                accessible_name=f"CTK Radio button for {choice}",
                command=lambda: self.on_radio_change(self.ctk_radio_var.get()),
            ).pack(anchor="w", pady=2)

        # CTK Slider and Switch
        ctk_controls_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_controls_frame.pack(fill="x", pady=10)

        AccessibleCTKLabel(
            ctk_controls_frame,
            text="CTK Controls:",
            accessible_name="CTK Controls Section Label",
        ).pack(anchor="w")

        controls_container = AccessibleCTKFrame(ctk_controls_frame)
        controls_container.pack(fill="x", pady=5)

        AccessibleCTKLabel(
            controls_container, text="Slider:", accessible_name="CTK Slider Label"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ctk_slider = AccessibleCTKSlider(
            controls_container,
            from_=0,
            to=100,
            accessible_name="CTK Value Slider from 0 to 100",
            command=self.on_slider_change,
        )
        self.ctk_slider.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        AccessibleCTKLabel(
            controls_container, text="Switch:", accessible_name="CTK Switch Label"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.ctk_switch = AccessibleCTKSwitch(
            controls_container,
            text="Enable Feature",
            accessible_name="CTK Feature Toggle Switch",
            command=self.on_switch_change,
        )
        self.ctk_switch.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        controls_container.columnconfigure(1, weight=1)

        # CTK Progress Bar
        ctk_progress_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_progress_frame.pack(fill="x", pady=10)

        AccessibleCTKLabel(
            ctk_progress_frame,
            text="CTK Progress:",
            accessible_name="CTK Progress Section Label",
        ).pack(anchor="w")

        progress_container = AccessibleCTKFrame(ctk_progress_frame)
        progress_container.pack(fill="x", pady=5)

        self.ctk_progress = AccessibleCTKProgressBar(
            progress_container, accessible_name="CTK Progress Bar Indicator"
        )
        self.ctk_progress.pack(fill="x", padx=5, pady=2)

        AccessibleCTKButton(
            progress_container,
            text="Start CTK Progress",
            accessible_name="Start CTK Progress Button",
            command=self.start_ctk_progress,
        ).pack(pady=5)

        # CTK Tabview
        ctk_tabview_frame = AccessibleCTKFrame(self.ctk_scrollable)
        ctk_tabview_frame.pack(fill="both", expand=True, pady=10)

        AccessibleCTKLabel(
            ctk_tabview_frame,
            text="CTK TabView:",
            accessible_name="CTK TabView Section Label",
        ).pack(anchor="w")

        self.ctk_tabview = AccessibleCTKTabview(
            ctk_tabview_frame, accessible_name="CTK Tab Container"
        )
        self.ctk_tabview.pack(fill="both", expand=True, pady=5)

        # Add tabs to tabview
        self.ctk_tabview.add("Tab 1")
        self.ctk_tabview.add("Tab 2")
        self.ctk_tabview.add("Tab 3")

        # Add content to tabs
        AccessibleCTKLabel(
            self.ctk_tabview.tab("Tab 1"),
            text="Content for Tab 1",
            accessible_name="Tab 1 Content Label",
        ).pack(pady=20)

        AccessibleCTKLabel(
            self.ctk_tabview.tab("Tab 2"),
            text="Content for Tab 2",
            accessible_name="Tab 2 Content Label",
        ).pack(pady=20)

        AccessibleCTKLabel(
            self.ctk_tabview.tab("Tab 3"),
            text="Content for Tab 3",
            accessible_name="Tab 3 Content Label",
        ).pack(pady=20)

    def create_demo_tab(self):
        """Create interactive demo tab."""
        demo_frame = AccessibleTTKFrame(self.main_notebook)
        self.main_notebook.add(demo_frame, text="Interactive Demo")

        # Create paned window for layout
        paned = AccessibleTTKPanedWindow(demo_frame, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - Controls
        left_frame = AccessibleTTKLabelFrame(paned, text="Demo Controls")
        paned.add(left_frame, weight=1)

        # Demo data input
        AccessibleTTKLabel(
            left_frame, text="Add Demo Item:", accessible_name="Demo Item Input Label"
        ).pack(anchor="w", padx=5, pady=2)

        self.demo_entry = AccessibleTTKEntry(
            left_frame, accessible_name="Demo Item Name Input"
        )
        self.demo_entry.pack(fill="x", padx=5, pady=2)
        self.demo_entry.bind("<Return>", lambda e: self.add_demo_item())

        AccessibleTTKButton(
            left_frame,
            text="Add Item",
            accessible_name="Add Demo Item Button",
            command=self.add_demo_item,
        ).pack(fill="x", padx=5, pady=2)

        AccessibleTTKButton(
            left_frame,
            text="Remove Selected",
            accessible_name="Remove Selected Demo Item Button",
            command=self.remove_demo_item,
        ).pack(fill="x", padx=5, pady=2)

        AccessibleTTKButton(
            left_frame,
            text="Clear All",
            accessible_name="Clear All Demo Items Button",
            command=self.clear_demo_items,
        ).pack(fill="x", padx=5, pady=2)

        # Demo settings
        AccessibleTTKSeparator(left_frame, orient="horizontal").pack(fill="x", pady=10)

        AccessibleTTKLabel(
            left_frame,
            text="Demo Settings:",
            accessible_name="Demo Settings Section Label",
        ).pack(anchor="w", padx=5, pady=2)

        self.auto_speak_var = tk.BooleanVar(value=True)
        AccessibleTTKCheckbutton(
            left_frame,
            text="Auto-speak changes",
            variable=self.auto_speak_var,
            accessible_name="Auto-speak Changes Checkbox",
            command=self.toggle_auto_speak,
        ).pack(anchor="w", padx=5, pady=2)

        self.demo_theme_var = tk.StringVar(value="default")
        AccessibleTTKLabel(
            left_frame, text="Theme:", accessible_name="Theme Selection Label"
        ).pack(anchor="w", padx=5, pady=2)

        theme_combo = AccessibleCombobox(
            left_frame,
            textvariable=self.demo_theme_var,
            values=["default", "high_contrast", "dark"],
            accessible_name="Theme Selection ComboBox",
            state="readonly",
        )
        theme_combo.pack(fill="x", padx=5, pady=2)
        theme_combo.bind("<<ComboboxSelected>>", self.change_demo_theme)

        # Right panel - Demo list
        right_frame = AccessibleTTKLabelFrame(paned, text="Demo Items")
        paned.add(right_frame, weight=2)

        # Create demo listbox with scrollbar
        list_frame = AccessibleTTKFrame(right_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.demo_listbox = AccessibleListbox(
            list_frame, accessible_name="Demo Items List"
        )
        demo_scrollbar = AccessibleTTKScrollbar(
            list_frame, orient="vertical", command=self.demo_listbox.yview
        )
        self.demo_listbox.configure(yscrollcommand=demo_scrollbar.set)

        self.demo_listbox.pack(side="left", fill="both", expand=True)
        demo_scrollbar.pack(side="right", fill="y")

        self.demo_listbox.bind("<<ListboxSelect>>", self.on_demo_select)

        # Status bar
        self.status_label = AccessibleTTKLabel(
            demo_frame, text="Ready", accessible_name="Application Status"
        )
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=2)

    def populate_demo_data(self):
        """Populate initial demo data."""
        initial_items = [
            "Sample Item 1",
            "Sample Item 2",
            "Sample Item 3",
            "Demo Entry A",
            "Demo Entry B",
        ]

        for item in initial_items:
            self.demo_data.append(item)
            self.demo_listbox.insert("end", item)

    def populate_treeview(self):
        """Populate the treeview with sample data."""
        # Add some sample data
        folders = [
            ("Documents", "Folder", ""),
            ("Pictures", "Folder", ""),
            ("Music", "Folder", ""),
            ("Videos", "Folder", ""),
        ]

        files = [
            ("document.txt", "Text File", "2.5 KB"),
            ("image.jpg", "Image", "1.2 MB"),
            ("song.mp3", "Audio", "3.8 MB"),
            ("video.mp4", "Video", "25.6 MB"),
        ]

        # Insert folders
        folder_items = {}
        for name, type_val, size in folders:
            item_id = self.ttk_tree.insert(
                "", "end", text=name, values=(name, type_val, size)
            )
            folder_items[name] = item_id

        # Insert files into folders
        for i, (name, type_val, size) in enumerate(files):
            folder_name = list(folders)[i % len(folders)][0]
            self.ttk_tree.insert(
                folder_items[folder_name],
                "end",
                text=name,
                values=(name, type_val, size),
            )

    def bind_keyboard_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind("<Control-n>", lambda e: self.new_demo_data())
        self.bind("<Control-o>", lambda e: self.load_demo_data())
        self.bind("<Control-s>", lambda e: self.save_demo_data())
        self.bind("<Control-q>", lambda e: self.quit())
        self.bind("<F1>", lambda e: self.show_shortcuts())
        self.bind("<Control-t>", lambda e: self.toggle_theme())

    # Event handlers
    def show_message(self, message):
        """Show a message dialog."""
        messagebox.showinfo("Demo Message", message)
        speak(f"Showed message: {message}")

    def on_checkbox_change(self, option):
        """Handle checkbox state changes."""
        speak(f"Checkbox {option} changed")
        self.update_status(f"Checkbox {option} toggled")

    def on_radio_change(self, value):
        """Handle radio button changes."""
        speak(f"Selected {value}")
        self.update_status(f"Radio selection: {value}")

    def on_scale_change(self, value):
        """Handle scale value changes."""
        self.update_status(f"Scale value: {float(value):.1f}")

    def on_slider_change(self, value):
        """Handle CTK slider changes."""
        if CTK_AVAILABLE:
            self.update_status(f"Slider value: {float(value):.1f}")

    def on_switch_change(self):
        """Handle CTK switch changes."""
        if CTK_AVAILABLE:
            state = "on" if self.ctk_switch.get() else "off"
            speak(f"Switch turned {state}")
            self.update_status(f"Switch: {state}")

    def on_listbox_select(self, event):
        """Handle listbox selection."""
        selection = event.widget.curselection()
        if selection:
            item = event.widget.get(selection[0])
            speak(f"Selected {item}")
            self.update_status(f"Selected: {item}")

    def on_demo_select(self, event):
        """Handle demo listbox selection."""
        selection = event.widget.curselection()
        if selection:
            item = event.widget.get(selection[0])
            self.update_status(f"Demo item selected: {item}")

    def on_combobox_select(self, event):
        """Handle combobox selection."""
        value = event.widget.get()
        speak(f"Selected {value}")
        self.update_status(f"Combobox: {value}")

    def start_progress(self):
        """Start progress bar animation."""
        self.ttk_progress["value"] = 0
        self.animate_progress()

    def start_ctk_progress(self):
        """Start CTK progress bar animation."""
        if CTK_AVAILABLE:
            self.ctk_progress.set(0)
            self.animate_ctk_progress()

    def animate_progress(self, value=0):
        """Animate TTK progress bar."""
        if value <= 100:
            self.ttk_progress["value"] = value
            self.update_status(f"Progress: {value}%")
            self.after(50, lambda: self.animate_progress(value + 2))
        else:
            speak("Progress complete")
            self.update_status("Progress complete")

    def animate_ctk_progress(self, value=0):
        """Animate CTK progress bar."""
        if CTK_AVAILABLE and value <= 1.0:
            self.ctk_progress.set(value)
            self.update_status(f"CTK Progress: {int(value * 100)}%")
            self.after(50, lambda: self.animate_ctk_progress(value + 0.02))
        else:
            speak("CTK Progress complete")
            self.update_status("CTK Progress complete")

    def add_demo_item(self):
        """Add item to demo list."""
        item = self.demo_entry.get().strip()
        if item:
            self.demo_data.append(item)
            self.demo_listbox.insert("end", item)
            self.demo_entry.delete(0, "end")
            speak(f"Added {item}")
            self.update_status(f"Added: {item}")

    def remove_demo_item(self):
        """Remove selected demo item."""
        selection = self.demo_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.demo_data.pop(index)
            self.demo_listbox.delete(index)
            speak(f"Removed {item}")
            self.update_status(f"Removed: {item}")

    def clear_demo_items(self):
        """Clear all demo items."""
        self.demo_data.clear()
        self.demo_listbox.delete(0, "end")
        speak("Cleared all items")
        self.update_status("All items cleared")

    def toggle_auto_speak(self):
        """Toggle auto-speak feature."""
        state = "enabled" if self.auto_speak_var.get() else "disabled"
        speak(f"Auto-speak {state}")
        self.update_status(f"Auto-speak: {state}")

    def change_demo_theme(self, event):
        """Change demo theme."""
        theme = self.demo_theme_var.get()
        # Note: This would typically change the theme
        speak(f"Theme changed to {theme}")
        self.update_status(f"Theme: {theme}")

    def update_status(self, message):
        """Update status bar."""
        self.status_label.configure(text=message)

    def new_demo_data(self):
        """Create new demo data."""
        self.clear_demo_items()
        speak("Created new demo data")

    def load_demo_data(self):
        """Load demo data from file."""
        filename = filedialog.askopenfilename(
            title="Load Demo Data",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    lines = f.readlines()
                self.clear_demo_items()
                for line in lines:
                    item = line.strip()
                    if item:
                        self.demo_data.append(item)
                        self.demo_listbox.insert("end", item)
                speak(f"Loaded {len(lines)} items")
                self.update_status(f"Loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def save_demo_data(self):
        """Save demo data to file."""
        if not self.demo_data:
            messagebox.showwarning("Warning", "No data to save")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Demo Data",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            try:
                with open(filename, "w") as f:
                    for item in self.demo_data:
                        f.write(f"{item}\n")
                speak(f"Saved {len(self.demo_data)} items")
                self.update_status(f"Saved: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def show_about(self):
        """Show about dialog."""
        about_text = """tkaria11y Comprehensive Demo

This application demonstrates all accessible widgets available in the tkaria11y framework.

Features:
• Full accessibility support with ARIA labels
• Text-to-speech feedback
• Keyboard navigation
• High-contrast themes
• Support for screen readers

Frameworks demonstrated:
• Standard Tkinter widgets
• TTK (themed) widgets
• CustomTkinter widgets (if available)

Version: Demo 1.0
"""
        messagebox.showinfo("About", about_text)

    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        shortcuts_text = """Keyboard Shortcuts:

Ctrl+N - New demo data
Ctrl+O - Load demo data
Ctrl+S - Save demo data
Ctrl+Q - Quit application
Ctrl+T - Toggle theme
F1 - Show this help

Navigation:
Tab - Move to next widget
Shift+Tab - Move to previous widget
Space - Activate buttons/checkboxes
Enter - Activate default button
Arrow keys - Navigate lists/trees
"""
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)


def main():
    """Main application entry point."""
    try:
        app = ComprehensiveDemoApp()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
