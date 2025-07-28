#!/usr/bin/env python3
"""
Comprehensive Accessibility Demo for tkaria11y

This demo showcases all accessibility features including:
- Full WCAG 2.1 compliance
- ARIA roles and properties
- Platform-specific screen reader integration
- Advanced focus management
- High contrast themes
- Dyslexic-friendly fonts
- Keyboard navigation
- Automated accessibility testing
- Support for all widget types (Tkinter, TTK, CustomTkinter)
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import sys
import os

# Add the parent directory to the path to import tkaria11y
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tkaria11y import (
    # Core components
    AccessibleApp,
    setup_full_accessibility,
    quick_accessibility_audit,
    # Widgets - Standard Tkinter
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleListbox,
    AccessibleFrame,
    AccessibleText,
    AccessibleSpinbox,
    # Widgets - TTK
    AccessibleTTKButton,
    AccessibleTTKEntry,
    AccessibleTTKLabel,
    AccessibleTTKCheckbutton,
    AccessibleTTKRadiobutton,
    AccessibleTTKScale,
    AccessibleTTKFrame,
    AccessibleTTKNotebook,
    AccessibleTTKProgressbar,
    AccessibleTTKCombobox,
    AccessibleTTKTreeview,
    # Specialized widgets
    AccessibleNotebook,
    AccessibleTreeview,
    AccessibleCombobox,
    # Theming and fonts
    HighContrastTheme,
    set_dyslexic_font,
    set_large_text,
    increase_font_size,
    decrease_font_size,
    apply_colorblind_safe_theme,
    # Focus management
    get_focus_manager,
    configure_advanced_focus_traversal,
    # Validation and testing
    run_accessibility_audit,
    auto_fix_accessibility_issues,
    test_keyboard_navigation,
    test_screen_reader_compatibility,
    # Platform integration
    is_screen_reader_active,
    announce,
    # TTS
    speak,
)


class ComprehensiveAccessibilityDemo:
    """Comprehensive demo of all accessibility features"""

    def __init__(self):
        # Create accessible application
        self.root = AccessibleApp()
        self.root.title("Comprehensive Accessibility Demo - tkaria11y")
        self.root.geometry("1000x800")

        # Set up full accessibility
        setup_full_accessibility(
            self.root,
            high_contrast=False,  # We'll toggle this manually
            dyslexic_font=False,  # We'll toggle this manually
            large_text=False,  # We'll toggle this manually
            auto_fix=True,
        )

        # Track accessibility settings
        self.high_contrast_enabled = tk.BooleanVar()
        self.dyslexic_font_enabled = tk.BooleanVar()
        self.large_text_enabled = tk.BooleanVar()
        self.screen_reader_mode = tk.BooleanVar(value=is_screen_reader_active())

        # Create the interface
        self.create_interface()

        # Announce application ready
        self.root.after(
            1000, lambda: speak("Accessibility demo application ready", priority="high")
        )

    def create_interface(self):
        """Create the complete interface demonstrating all features"""

        # Create main notebook for different sections
        self.main_notebook = AccessibleNotebook(
            self.root,
            accessible_name="Main sections",
            accessible_description="Navigate between different accessibility feature demonstrations",
        )
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create different tabs
        self.create_basic_widgets_tab()
        self.create_advanced_widgets_tab()
        self.create_forms_tab()
        self.create_accessibility_controls_tab()
        self.create_testing_tab()

    def create_basic_widgets_tab(self):
        """Create tab with basic accessible widgets"""
        frame = AccessibleTTKFrame(
            self.main_notebook,
            accessible_name="Basic widgets section",
            accessible_description="Demonstrates basic accessible widgets",
        )
        self.main_notebook.add(frame, text="Basic Widgets")

        # Title
        title = AccessibleTTKLabel(
            frame,
            text="Basic Accessible Widgets",
            font=("Arial", 16, "bold"),
            accessible_name="Basic widgets title",
            accessible_role="heading",
        )
        title.pack(pady=(0, 20))

        # Buttons section
        button_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Button examples",
            accessible_description="Various types of accessible buttons",
        )
        button_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(
            button_frame,
            text="Buttons:",
            font=("Arial", 12, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W)

        # Standard button
        AccessibleTTKButton(
            button_frame,
            text="Standard Button",
            accessible_name="Standard action button",
            accessible_description="Demonstrates a standard accessible button",
            command=lambda: self.show_message("Standard button clicked!"),
        ).pack(side=tk.LEFT, padx=5)

        # Button with icon (simulated)
        AccessibleTTKButton(
            button_frame,
            text="🔍 Search",
            accessible_name="Search button",
            accessible_description="Opens search dialog",
            command=self.open_search_dialog,
        ).pack(side=tk.LEFT, padx=5)

        # Disabled button
        disabled_btn = AccessibleTTKButton(
            button_frame,
            text="Disabled Button",
            accessible_name="Disabled button example",
            accessible_description="This button is disabled to show disabled state",
            state="disabled",
        )
        disabled_btn.pack(side=tk.LEFT, padx=5)

        # Input controls section
        input_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Input controls",
            accessible_description="Various input controls with proper labeling",
        )
        input_frame.pack(fill=tk.X, pady=20)

        AccessibleTTKLabel(
            input_frame,
            text="Input Controls:",
            font=("Arial", 12, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W)

        # Text entry
        entry_frame = AccessibleTTKFrame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(entry_frame, text="Name:", accessible_role="label").pack(
            side=tk.LEFT
        )

        self.name_entry = AccessibleTTKEntry(
            entry_frame,
            accessible_name="Name input field",
            accessible_description="Enter your full name here",
            width=30,
        )
        self.name_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Password entry
        password_frame = AccessibleTTKFrame(input_frame)
        password_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            password_frame, text="Password:", accessible_role="label"
        ).pack(side=tk.LEFT)

        self.password_entry = AccessibleTTKEntry(
            password_frame,
            accessible_name="Password input field",
            accessible_description="Enter your password, characters will be hidden",
            show="*",
            width=30,
        )
        self.password_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Checkboxes and radio buttons
        choice_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Choice controls",
            accessible_description="Checkboxes and radio buttons",
        )
        choice_frame.pack(fill=tk.X, pady=20)

        AccessibleTTKLabel(
            choice_frame,
            text="Choices:",
            font=("Arial", 12, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W)

        # Checkboxes
        self.newsletter_var = tk.BooleanVar()
        AccessibleTTKCheckbutton(
            choice_frame,
            text="Subscribe to newsletter",
            variable=self.newsletter_var,
            accessible_name="Newsletter subscription",
            accessible_description="Check to receive our monthly newsletter",
            command=self.on_newsletter_change,
        ).pack(anchor=tk.W, pady=2)

        self.notifications_var = tk.BooleanVar()
        AccessibleTTKCheckbutton(
            choice_frame,
            text="Enable notifications",
            variable=self.notifications_var,
            accessible_name="Notification settings",
            accessible_description="Check to receive desktop notifications",
        ).pack(anchor=tk.W, pady=2)

        # Radio buttons
        radio_frame = AccessibleTTKFrame(choice_frame)
        radio_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(
            radio_frame, text="Preferred contact method:", accessible_role="label"
        ).pack(anchor=tk.W)

        self.contact_var = tk.StringVar(value="email")

        AccessibleTTKRadiobutton(
            radio_frame,
            text="Email",
            variable=self.contact_var,
            value="email",
            accessible_name="Email contact option",
            accessible_description="Select email as preferred contact method",
        ).pack(anchor=tk.W, padx=20)

        AccessibleTTKRadiobutton(
            radio_frame,
            text="Phone",
            variable=self.contact_var,
            value="phone",
            accessible_name="Phone contact option",
            accessible_description="Select phone as preferred contact method",
        ).pack(anchor=tk.W, padx=20)

        AccessibleTTKRadiobutton(
            radio_frame,
            text="SMS",
            variable=self.contact_var,
            value="sms",
            accessible_name="SMS contact option",
            accessible_description="Select SMS as preferred contact method",
        ).pack(anchor=tk.W, padx=20)

    def create_advanced_widgets_tab(self):
        """Create tab with advanced accessible widgets"""
        frame = AccessibleTTKFrame(
            self.main_notebook,
            accessible_name="Advanced widgets section",
            accessible_description="Demonstrates advanced accessible widgets",
        )
        self.main_notebook.add(frame, text="Advanced Widgets")

        # Title
        title = AccessibleTTKLabel(
            frame,
            text="Advanced Accessible Widgets",
            font=("Arial", 16, "bold"),
            accessible_name="Advanced widgets title",
            accessible_role="heading",
        )
        title.pack(pady=(0, 20))

        # Scale/Slider
        scale_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Slider controls",
            accessible_description="Adjustable slider controls",
        )
        scale_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(
            scale_frame, text="Volume Control:", accessible_role="label"
        ).pack(anchor=tk.W)

        self.volume_var = tk.DoubleVar(value=50)
        volume_scale = AccessibleTTKScale(
            scale_frame,
            from_=0,
            to=100,
            variable=self.volume_var,
            orient=tk.HORIZONTAL,
            accessible_name="Volume slider",
            accessible_description="Adjust volume from 0 to 100 percent",
            command=self.on_volume_change,
        )
        volume_scale.pack(fill=tk.X, pady=5)

        self.volume_label = AccessibleTTKLabel(
            scale_frame,
            text="Volume: 50%",
            accessible_name="Current volume display",
            accessible_role="status",
        )
        self.volume_label.pack(anchor=tk.W)

        # Progress bar
        progress_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Progress indicator",
            accessible_description="Shows progress of operations",
        )
        progress_frame.pack(fill=tk.X, pady=20)

        AccessibleTTKLabel(
            progress_frame, text="Progress:", accessible_role="label"
        ).pack(anchor=tk.W)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = AccessibleTTKProgressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            accessible_name="Operation progress",
            accessible_description="Shows completion percentage of current operation",
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        AccessibleTTKButton(
            progress_frame,
            text="Start Progress Demo",
            accessible_name="Start progress demonstration",
            accessible_description="Starts a simulated progress operation",
            command=self.start_progress_demo,
        ).pack(pady=5)

        # Combobox
        combo_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Dropdown selection",
            accessible_description="Dropdown selection controls",
        )
        combo_frame.pack(fill=tk.X, pady=20)

        AccessibleTTKLabel(combo_frame, text="Country:", accessible_role="label").pack(
            anchor=tk.W
        )

        countries = [
            "United States",
            "Canada",
            "United Kingdom",
            "Australia",
            "Germany",
            "France",
            "Japan",
        ]
        self.country_combo = AccessibleTTKCombobox(
            combo_frame,
            values=countries,
            accessible_name="Country selection",
            accessible_description="Select your country from the dropdown list",
            state="readonly",
        )
        self.country_combo.pack(fill=tk.X, pady=5)
        self.country_combo.set("United States")

        # Listbox
        list_frame = AccessibleTTKFrame(
            frame,
            accessible_name="List selection",
            accessible_description="Multi-item list selection",
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        AccessibleTTKLabel(
            list_frame, text="Available Options:", accessible_role="label"
        ).pack(anchor=tk.W)

        # Create listbox with scrollbar
        listbox_frame = AccessibleTTKFrame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = AccessibleListbox(
            listbox_frame,
            accessible_name="Options list",
            accessible_description="Select one or more options from the list",
            selectmode=tk.EXTENDED,
        )

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate listbox
        options = [
            "Option 1: Basic features",
            "Option 2: Advanced features",
            "Option 3: Premium features",
            "Option 4: Enterprise features",
            "Option 5: Custom solutions",
            "Option 6: Support services",
            "Option 7: Training programs",
            "Option 8: Consulting services",
        ]

        for option in options:
            self.listbox.insert(tk.END, option)

    def create_forms_tab(self):
        """Create tab demonstrating accessible forms"""
        frame = AccessibleTTKFrame(
            self.main_notebook,
            accessible_name="Forms section",
            accessible_description="Demonstrates accessible form design",
        )
        self.main_notebook.add(frame, text="Forms")

        # Title
        title = AccessibleTTKLabel(
            frame,
            text="Accessible Form Example",
            font=("Arial", 16, "bold"),
            accessible_name="Form example title",
            accessible_role="heading",
        )
        title.pack(pady=(0, 20))

        # Create scrollable form
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = AccessibleTTKFrame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Personal Information Section
        personal_frame = AccessibleTTKFrame(
            scrollable_frame,
            accessible_name="Personal information section",
            accessible_description="Enter your personal details",
        )
        personal_frame.pack(fill=tk.X, pady=10, padx=20)

        AccessibleTTKLabel(
            personal_frame,
            text="Personal Information",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        # First Name
        fname_frame = AccessibleTTKFrame(personal_frame)
        fname_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            fname_frame,
            text="First Name *:",
            width=15,
            anchor=tk.W,
            accessible_role="label",
        ).pack(side=tk.LEFT)

        self.first_name = AccessibleTTKEntry(
            fname_frame,
            accessible_name="First name",
            accessible_description="Enter your first name, this field is required",
            width=30,
        )
        self.first_name.pack(side=tk.LEFT, padx=(5, 0))

        # Last Name
        lname_frame = AccessibleTTKFrame(personal_frame)
        lname_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            lname_frame,
            text="Last Name *:",
            width=15,
            anchor=tk.W,
            accessible_role="label",
        ).pack(side=tk.LEFT)

        self.last_name = AccessibleTTKEntry(
            lname_frame,
            accessible_name="Last name",
            accessible_description="Enter your last name, this field is required",
            width=30,
        )
        self.last_name.pack(side=tk.LEFT, padx=(5, 0))

        # Email
        email_frame = AccessibleTTKFrame(personal_frame)
        email_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            email_frame, text="Email *:", width=15, anchor=tk.W, accessible_role="label"
        ).pack(side=tk.LEFT)

        self.email = AccessibleTTKEntry(
            email_frame,
            accessible_name="Email address",
            accessible_description="Enter your email address, this field is required",
            width=30,
        )
        self.email.pack(side=tk.LEFT, padx=(5, 0))

        # Phone
        phone_frame = AccessibleTTKFrame(personal_frame)
        phone_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            phone_frame, text="Phone:", width=15, anchor=tk.W, accessible_role="label"
        ).pack(side=tk.LEFT)

        self.phone = AccessibleTTKEntry(
            phone_frame,
            accessible_name="Phone number",
            accessible_description="Enter your phone number, this field is optional",
            width=30,
        )
        self.phone.pack(side=tk.LEFT, padx=(5, 0))

        # Address Section
        address_frame = AccessibleTTKFrame(
            scrollable_frame,
            accessible_name="Address information section",
            accessible_description="Enter your address details",
        )
        address_frame.pack(fill=tk.X, pady=20, padx=20)

        AccessibleTTKLabel(
            address_frame,
            text="Address Information",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        # Street Address
        street_frame = AccessibleTTKFrame(address_frame)
        street_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            street_frame,
            text="Street Address:",
            width=15,
            anchor=tk.W,
            accessible_role="label",
        ).pack(side=tk.LEFT)

        self.street = AccessibleTTKEntry(
            street_frame,
            accessible_name="Street address",
            accessible_description="Enter your street address",
            width=40,
        )
        self.street.pack(side=tk.LEFT, padx=(5, 0))

        # City, State, ZIP
        location_frame = AccessibleTTKFrame(address_frame)
        location_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            location_frame, text="City:", width=8, anchor=tk.W, accessible_role="label"
        ).pack(side=tk.LEFT)

        self.city = AccessibleTTKEntry(
            location_frame,
            accessible_name="City",
            accessible_description="Enter your city",
            width=15,
        )
        self.city.pack(side=tk.LEFT, padx=(5, 10))

        AccessibleTTKLabel(
            location_frame, text="State:", width=8, anchor=tk.W, accessible_role="label"
        ).pack(side=tk.LEFT)

        self.state = AccessibleTTKEntry(
            location_frame,
            accessible_name="State",
            accessible_description="Enter your state or province",
            width=10,
        )
        self.state.pack(side=tk.LEFT, padx=(5, 10))

        AccessibleTTKLabel(
            location_frame, text="ZIP:", width=8, anchor=tk.W, accessible_role="label"
        ).pack(side=tk.LEFT)

        self.zip_code = AccessibleTTKEntry(
            location_frame,
            accessible_name="ZIP code",
            accessible_description="Enter your ZIP or postal code",
            width=10,
        )
        self.zip_code.pack(side=tk.LEFT, padx=(5, 0))

        # Comments Section
        comments_frame = AccessibleTTKFrame(
            scrollable_frame,
            accessible_name="Comments section",
            accessible_description="Additional comments or notes",
        )
        comments_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        AccessibleTTKLabel(
            comments_frame,
            text="Additional Comments:",
            font=("Arial", 12, "bold"),
            accessible_role="label",
        ).pack(anchor=tk.W, pady=(0, 5))

        self.comments = AccessibleText(
            comments_frame,
            accessible_name="Comments text area",
            accessible_description="Enter any additional comments or special requests",
            height=6,
            width=60,
            wrap=tk.WORD,
        )
        self.comments.pack(fill=tk.BOTH, expand=True)

        # Form buttons
        button_frame = AccessibleTTKFrame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=20, padx=20)

        AccessibleTTKButton(
            button_frame,
            text="Submit Form",
            accessible_name="Submit form button",
            accessible_description="Submit the completed form",
            command=self.submit_form,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            button_frame,
            text="Clear Form",
            accessible_name="Clear form button",
            accessible_description="Clear all form fields",
            command=self.clear_form,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            button_frame,
            text="Validate Form",
            accessible_name="Validate form button",
            accessible_description="Check form for errors without submitting",
            command=self.validate_form,
        ).pack(side=tk.LEFT)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_accessibility_controls_tab(self):
        """Create tab with accessibility control options"""
        frame = AccessibleTTKFrame(
            self.main_notebook,
            accessible_name="Accessibility controls section",
            accessible_description="Control accessibility features and settings",
        )
        self.main_notebook.add(frame, text="Accessibility Controls")

        # Title
        title = AccessibleTTKLabel(
            frame,
            text="Accessibility Controls",
            font=("Arial", 16, "bold"),
            accessible_name="Accessibility controls title",
            accessible_role="heading",
        )
        title.pack(pady=(0, 20))

        # Visual accessibility controls
        visual_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Visual accessibility controls",
            accessible_description="Controls for visual accessibility features",
        )
        visual_frame.pack(fill=tk.X, pady=10, padx=20)

        AccessibleTTKLabel(
            visual_frame,
            text="Visual Accessibility:",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        # High contrast toggle
        AccessibleTTKCheckbutton(
            visual_frame,
            text="High Contrast Mode",
            variable=self.high_contrast_enabled,
            accessible_name="High contrast mode toggle",
            accessible_description="Enable high contrast colors for better visibility",
            command=self.toggle_high_contrast,
        ).pack(anchor=tk.W, pady=2)

        # Dyslexic font toggle
        AccessibleTTKCheckbutton(
            visual_frame,
            text="Dyslexic-Friendly Font",
            variable=self.dyslexic_font_enabled,
            accessible_name="Dyslexic font toggle",
            accessible_description="Use dyslexic-friendly font for better readability",
            command=self.toggle_dyslexic_font,
        ).pack(anchor=tk.W, pady=2)

        # Large text toggle
        AccessibleTTKCheckbutton(
            visual_frame,
            text="Large Text",
            variable=self.large_text_enabled,
            accessible_name="Large text toggle",
            accessible_description="Use larger text sizes for better visibility",
            command=self.toggle_large_text,
        ).pack(anchor=tk.W, pady=2)

        # Font size controls
        font_frame = AccessibleTTKFrame(visual_frame)
        font_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(font_frame, text="Font Size:", accessible_role="label").pack(
            side=tk.LEFT
        )

        AccessibleTTKButton(
            font_frame,
            text="A-",
            accessible_name="Decrease font size",
            accessible_description="Make text smaller",
            command=self.decrease_font_size,
            width=5,
        ).pack(side=tk.LEFT, padx=5)

        AccessibleTTKButton(
            font_frame,
            text="A+",
            accessible_name="Increase font size",
            accessible_description="Make text larger",
            command=self.increase_font_size,
            width=5,
        ).pack(side=tk.LEFT, padx=5)

        # Color blindness support
        colorblind_frame = AccessibleTTKFrame(visual_frame)
        colorblind_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(
            colorblind_frame, text="Color Blindness Support:", accessible_role="label"
        ).pack(anchor=tk.W)

        self.colorblind_var = tk.StringVar(value="none")

        colorblind_options = [
            ("None", "none"),
            ("Protanopia (Red-blind)", "protanopia"),
            ("Deuteranopia (Green-blind)", "deuteranopia"),
            ("Tritanopia (Blue-blind)", "tritanopia"),
            ("Universal Safe", "universal"),
        ]

        for text, value in colorblind_options:
            AccessibleTTKRadiobutton(
                colorblind_frame,
                text=text,
                variable=self.colorblind_var,
                value=value,
                accessible_name=f"Color blindness option: {text}",
                accessible_description=f"Apply color palette safe for {text.lower()}",
                command=self.apply_colorblind_support,
            ).pack(anchor=tk.W, padx=20)

        # Audio accessibility controls
        audio_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Audio accessibility controls",
            accessible_description="Controls for audio accessibility features",
        )
        audio_frame.pack(fill=tk.X, pady=20, padx=20)

        AccessibleTTKLabel(
            audio_frame,
            text="Audio Accessibility:",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        # TTS controls
        tts_frame = AccessibleTTKFrame(audio_frame)
        tts_frame.pack(fill=tk.X, pady=5)

        AccessibleTTKLabel(
            tts_frame, text="Text-to-Speech:", accessible_role="label"
        ).pack(side=tk.LEFT)

        AccessibleTTKButton(
            tts_frame,
            text="Test TTS",
            accessible_name="Test text-to-speech",
            accessible_description="Play a test message using text-to-speech",
            command=self.test_tts,
        ).pack(side=tk.LEFT, padx=5)

        AccessibleTTKButton(
            tts_frame,
            text="Announce Current Focus",
            accessible_name="Announce current focus",
            accessible_description="Announce information about the currently focused element",
            command=self.announce_current_focus,
        ).pack(side=tk.LEFT, padx=5)

        # Screen reader detection
        sr_frame = AccessibleTTKFrame(audio_frame)
        sr_frame.pack(fill=tk.X, pady=10)

        AccessibleTTKLabel(
            sr_frame, text="Screen Reader Status:", accessible_role="label"
        ).pack(side=tk.LEFT)

        sr_status = "Detected" if is_screen_reader_active() else "Not Detected"
        self.sr_status_label = AccessibleTTKLabel(
            sr_frame,
            text=sr_status,
            accessible_name="Screen reader status",
            accessible_description=f"Screen reader is currently {sr_status.lower()}",
            accessible_role="status",
        )
        self.sr_status_label.pack(side=tk.LEFT, padx=10)

        AccessibleTTKButton(
            sr_frame,
            text="Refresh Status",
            accessible_name="Refresh screen reader status",
            accessible_description="Check again for screen reader presence",
            command=self.refresh_screen_reader_status,
        ).pack(side=tk.LEFT, padx=5)

    def create_testing_tab(self):
        """Create tab with accessibility testing tools"""
        frame = AccessibleTTKFrame(
            self.main_notebook,
            accessible_name="Testing tools section",
            accessible_description="Tools for testing accessibility compliance",
        )
        self.main_notebook.add(frame, text="Testing Tools")

        # Title
        title = AccessibleTTKLabel(
            frame,
            text="Accessibility Testing Tools",
            font=("Arial", 16, "bold"),
            accessible_name="Testing tools title",
            accessible_role="heading",
        )
        title.pack(pady=(0, 20))

        # Quick audit section
        audit_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Quick audit section",
            accessible_description="Run quick accessibility audit",
        )
        audit_frame.pack(fill=tk.X, pady=10, padx=20)

        AccessibleTTKLabel(
            audit_frame,
            text="Quick Accessibility Audit:",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        AccessibleTTKButton(
            audit_frame,
            text="Run Quick Audit",
            accessible_name="Run quick accessibility audit",
            accessible_description="Perform a quick accessibility compliance check",
            command=self.run_quick_audit,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            audit_frame,
            text="Run Full Audit",
            accessible_name="Run full accessibility audit",
            accessible_description="Perform comprehensive accessibility compliance audit",
            command=self.run_full_audit,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            audit_frame,
            text="Auto-Fix Issues",
            accessible_name="Auto-fix accessibility issues",
            accessible_description="Automatically fix accessibility issues that can be corrected",
            command=self.auto_fix_issues,
        ).pack(side=tk.LEFT)

        # Test results area
        results_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Test results section",
            accessible_description="Display accessibility test results",
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        AccessibleTTKLabel(
            results_frame,
            text="Test Results:",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create text widget with scrollbar for results
        text_frame = AccessibleTTKFrame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = AccessibleText(
            text_frame,
            accessible_name="Test results display",
            accessible_description="Shows detailed results of accessibility tests",
            wrap=tk.WORD,
            state=tk.DISABLED,
        )

        results_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
        self.results_text.config(yscrollcommand=results_scrollbar.set)
        results_scrollbar.config(command=self.results_text.yview)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Specific testing tools
        tools_frame = AccessibleTTKFrame(
            frame,
            accessible_name="Specific testing tools",
            accessible_description="Individual accessibility testing tools",
        )
        tools_frame.pack(fill=tk.X, pady=10, padx=20)

        AccessibleTTKLabel(
            tools_frame,
            text="Specific Tests:",
            font=("Arial", 14, "bold"),
            accessible_role="heading",
        ).pack(anchor=tk.W, pady=(0, 10))

        test_buttons_frame = AccessibleTTKFrame(tools_frame)
        test_buttons_frame.pack(fill=tk.X)

        AccessibleTTKButton(
            test_buttons_frame,
            text="Test Keyboard Navigation",
            accessible_name="Test keyboard navigation",
            accessible_description="Test keyboard accessibility and navigation",
            command=self.test_keyboard_navigation,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            test_buttons_frame,
            text="Test Screen Reader",
            accessible_name="Test screen reader compatibility",
            accessible_description="Test compatibility with screen readers",
            command=self.test_screen_reader,
        ).pack(side=tk.LEFT, padx=(0, 10))

        AccessibleTTKButton(
            test_buttons_frame,
            text="Test Color Contrast",
            accessible_name="Test color contrast",
            accessible_description="Test color contrast ratios for WCAG compliance",
            command=self.test_color_contrast,
        ).pack(side=tk.LEFT)

    # Event handlers and utility methods
    def show_message(self, message: str):
        """Show accessible message dialog"""
        messagebox.showinfo("Information", message)
        speak(f"Message: {message}")

    def open_search_dialog(self):
        """Open search dialog"""
        search_term = tk.simpledialog.askstring(
            "Search", "Enter search term:", parent=self.root
        )
        if search_term:
            self.show_message(f"Searching for: {search_term}")

    def on_newsletter_change(self):
        """Handle newsletter checkbox change"""
        status = "subscribed to" if self.newsletter_var.get() else "unsubscribed from"
        speak(f"Newsletter {status}")

    def on_volume_change(self, value):
        """Handle volume slider change"""
        volume = int(float(value))
        self.volume_label.config(text=f"Volume: {volume}%")
        # Announce volume changes with debouncing
        if hasattr(self, "_volume_announce_id"):
            self.root.after_cancel(self._volume_announce_id)
        self._volume_announce_id = self.root.after(
            500, lambda: speak(f"Volume {volume} percent", priority="low")
        )

    def start_progress_demo(self):
        """Start progress bar demonstration"""
        self.progress_var.set(0)
        self.update_progress(0)
        speak("Progress demonstration started")

    def update_progress(self, value):
        """Update progress bar"""
        if value <= 100:
            self.progress_var.set(value)
            if value % 25 == 0:  # Announce at 25% intervals
                speak(f"Progress {value} percent", priority="low")
            self.root.after(100, lambda: self.update_progress(value + 2))
        else:
            speak("Progress complete", priority="medium")

    def submit_form(self):
        """Submit form with validation"""
        if self.validate_form_data():
            self.show_message("Form submitted successfully!")
        else:
            speak("Please correct form errors before submitting", priority="high")

    def clear_form(self):
        """Clear all form fields"""
        fields = [
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.street,
            self.city,
            self.state,
            self.zip_code,
        ]

        for field in fields:
            field.delete(0, tk.END)

        self.comments.delete(1.0, tk.END)
        speak("Form cleared")

    def validate_form(self):
        """Validate form and show results"""
        errors = []

        if not self.first_name.get().strip():
            errors.append("First name is required")

        if not self.last_name.get().strip():
            errors.append("Last name is required")

        email = self.email.get().strip()
        if not email:
            errors.append("Email is required")
        elif "@" not in email:
            errors.append("Email format is invalid")

        if errors:
            error_message = "Form validation errors:\n" + "\n".join(
                f"• {error}" for error in errors
            )
            messagebox.showerror("Validation Errors", error_message)
            speak(f"Form has {len(errors)} validation errors", priority="high")
        else:
            messagebox.showinfo("Validation", "Form is valid!")
            speak("Form validation passed")

    def validate_form_data(self):
        """Validate form data and return True if valid"""
        return (
            self.first_name.get().strip()
            and self.last_name.get().strip()
            and self.email.get().strip()
            and "@" in self.email.get()
        )

    # Accessibility control handlers
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        if self.high_contrast_enabled.get():
            HighContrastTheme.apply(self.root)
            speak("High contrast mode enabled")
        else:
            HighContrastTheme.remove(self.root)
            speak("High contrast mode disabled")

    def toggle_dyslexic_font(self):
        """Toggle dyslexic-friendly font"""
        if self.dyslexic_font_enabled.get():
            set_dyslexic_font(self.root)
            speak("Dyslexic-friendly font enabled")
        else:
            # Reset to default font
            from tkaria11y.themes import get_font_manager

            font_manager = get_font_manager(self.root)
            font_manager.restore_original_fonts()
            speak("Default font restored")

    def toggle_large_text(self):
        """Toggle large text mode"""
        if self.large_text_enabled.get():
            set_large_text(self.root)
            speak("Large text mode enabled")
        else:
            # Reset to normal text size
            from tkaria11y.themes import get_font_manager

            font_manager = get_font_manager(self.root)
            font_manager.restore_original_fonts()
            speak("Normal text size restored")

    def increase_font_size(self):
        """Increase font size"""
        increase_font_size(self.root, 2)
        speak("Font size increased")

    def decrease_font_size(self):
        """Decrease font size"""
        decrease_font_size(self.root, 2)
        speak("Font size decreased")

    def apply_colorblind_support(self):
        """Apply color blindness support"""
        colorblind_type = self.colorblind_var.get()
        if colorblind_type != "none":
            apply_colorblind_safe_theme(self.root, colorblind_type)
            speak(f"Applied {colorblind_type} color safe theme")
        else:
            # Reset to default colors
            HighContrastTheme.remove(self.root)
            speak("Default colors restored")

    def test_tts(self):
        """Test text-to-speech"""
        speak(
            "This is a test of the text-to-speech system. If you can hear this message, TTS is working correctly.",
            priority="high",
        )

    def announce_current_focus(self):
        """Announce current focus"""
        focused = self.root.focus_get()
        if focused:
            if hasattr(focused, "accessible_name") and focused.accessible_name:
                announce(f"Current focus: {focused.accessible_name}")
            else:
                announce(f"Current focus: {focused.winfo_class()} widget")
        else:
            announce("No widget currently has focus")

    def refresh_screen_reader_status(self):
        """Refresh screen reader status"""
        status = "Detected" if is_screen_reader_active() else "Not Detected"
        self.sr_status_label.config(text=status)
        speak(f"Screen reader status: {status}")

    # Testing tool handlers
    def run_quick_audit(self):
        """Run quick accessibility audit"""
        self.display_results("Running quick accessibility audit...\n")

        try:
            summary = quick_accessibility_audit(self.root)

            results = f"""Quick Accessibility Audit Results:
            
Compliance Score: {summary['compliance_score']}/100
Total Issues: {summary['total_issues']}
Critical Issues: {summary['critical_issues']}
High Priority Issues: {summary['high_issues']}
Auto-fixable Issues: {summary['auto_fixable_count']}

Recommendations:
"""

            for rec in summary["recommendations"]:
                results += f"• {rec}\n"

            self.display_results(results)
            speak(
                f"Quick audit complete. Compliance score: {summary['compliance_score']} out of 100"
            )

        except Exception as e:
            self.display_results(f"Error running audit: {str(e)}\n")
            speak("Error running accessibility audit")

    def run_full_audit(self):
        """Run full accessibility audit"""
        self.display_results("Running comprehensive accessibility audit...\n")

        try:
            report = run_accessibility_audit(self.root)

            results = f"""Comprehensive Accessibility Audit Results:

Compliance Level: WCAG 2.1 {report['compliance_level']}
Compliance Score: {report['compliance_score']}/100
Total Issues Found: {report['total_issues']}
Audit Duration: {report['audit_duration']:.2f} seconds
Screen Reader Active: {report['screen_reader_active']}

Issues by Severity:
"""

            for severity, issues in report["issues_by_severity"].items():
                results += f"• {severity.title()}: {len(issues)} issues\n"

            results += "\nIssues by Category:\n"
            for category, count in report["summary"].items():
                category_name = (
                    category.replace("_issues", "").replace("_", " ").title()
                )
                results += f"• {category_name}: {count} issues\n"

            if report["all_issues"]:
                results += "\nDetailed Issues:\n"
                for i, issue in enumerate(
                    report["all_issues"][:10], 1
                ):  # Show first 10 issues
                    results += f"\n{i}. {issue['title']} ({issue['severity']})\n"
                    results += f"   {issue['description']}\n"
                    results += f"   Recommendation: {issue['recommendation']}\n"
                    if issue["wcag_criterion"]:
                        results += f"   WCAG Criterion: {issue['wcag_criterion']}\n"

                if len(report["all_issues"]) > 10:
                    results += (
                        f"\n... and {len(report['all_issues']) - 10} more issues\n"
                    )

            self.display_results(results)
            speak(
                f"Full audit complete. Found {report['total_issues']} issues with compliance score of {report['compliance_score']}"
            )

        except Exception as e:
            self.display_results(f"Error running full audit: {str(e)}\n")
            speak("Error running comprehensive audit")

    def auto_fix_issues(self):
        """Auto-fix accessibility issues"""
        self.display_results("Attempting to auto-fix accessibility issues...\n")

        try:
            fixed_count = auto_fix_accessibility_issues(self.root)

            results = (
                f"Auto-fix completed.\nFixed {fixed_count} accessibility issues.\n"
            )

            if fixed_count > 0:
                results += "\nCommon fixes applied:\n"
                results += "• Applied high contrast colors where needed\n"
                results += "• Increased font sizes below minimum\n"
                results += "• Enabled keyboard focus for interactive widgets\n"
                results += "• Changed problematic fonts to readable alternatives\n"

            self.display_results(results)
            speak(f"Auto-fix complete. Fixed {fixed_count} issues")

        except Exception as e:
            self.display_results(f"Error during auto-fix: {str(e)}\n")
            speak("Error during auto-fix process")

    def test_keyboard_navigation(self):
        """Test keyboard navigation"""
        self.display_results("Testing keyboard navigation...\n")

        try:
            issues = test_keyboard_navigation(self.root)

            results = f"Keyboard Navigation Test Results:\n\n"

            if issues:
                results += f"Found {len(issues)} keyboard navigation issues:\n\n"
                for i, issue in enumerate(issues, 1):
                    results += f"{i}. {issue}\n"
            else:
                results += "No keyboard navigation issues found.\n"

            results += "\nKeyboard Navigation Tips:\n"
            results += "• Use Tab to move forward through controls\n"
            results += "• Use Shift+Tab to move backward\n"
            results += "• Use arrow keys within lists and menus\n"
            results += "• Use Enter or Space to activate buttons\n"
            results += "• Use Escape to cancel dialogs\n"

            self.display_results(results)
            speak(f"Keyboard navigation test complete. Found {len(issues)} issues")

        except Exception as e:
            self.display_results(f"Error testing keyboard navigation: {str(e)}\n")
            speak("Error testing keyboard navigation")

    def test_screen_reader(self):
        """Test screen reader compatibility"""
        self.display_results("Testing screen reader compatibility...\n")

        try:
            results_data = test_screen_reader_compatibility(self.root)

            results = f"""Screen Reader Compatibility Test Results:

Screen Reader Detected: {results_data['screen_reader_detected']}
Widgets with Accessible Names: {results_data['widgets_with_names']}
Widgets with ARIA Roles: {results_data['widgets_with_roles']}
Widgets with Descriptions: {results_data['widgets_with_descriptions']}

Screen Reader Support Status:
"""

            if results_data["screen_reader_detected"]:
                results += (
                    "✓ Screen reader detected - enhanced announcements available\n"
                )
            else:
                results += "• No screen reader detected - using fallback TTS\n"

            if results_data["widgets_with_names"] > 0:
                results += f"✓ {results_data['widgets_with_names']} widgets have accessible names\n"
            else:
                results += "⚠ No widgets have accessible names\n"

            if results_data["widgets_with_roles"] > 0:
                results += (
                    f"✓ {results_data['widgets_with_roles']} widgets have ARIA roles\n"
                )
            else:
                results += "⚠ No widgets have ARIA roles\n"

            results += "\nRecommendations:\n"
            results += "• Ensure all interactive widgets have accessible names\n"
            results += "• Use appropriate ARIA roles for custom widgets\n"
            results += "• Provide descriptions for complex controls\n"
            results += "• Test with actual screen readers (NVDA, JAWS, VoiceOver)\n"

            self.display_results(results)
            speak("Screen reader compatibility test complete")

        except Exception as e:
            self.display_results(
                f"Error testing screen reader compatibility: {str(e)}\n"
            )
            speak("Error testing screen reader compatibility")

    def test_color_contrast(self):
        """Test color contrast"""
        self.display_results("Testing color contrast ratios...\n")

        try:
            from tkaria11y.aria_compliance import (
                calculate_contrast_ratio,
                validate_contrast_ratio,
            )

            results = "Color Contrast Test Results:\n\n"

            # Test some common color combinations
            test_combinations = [
                ("black", "white", "High contrast"),
                ("#000000", "#FFFFFF", "Pure black on white"),
                ("#333333", "#FFFFFF", "Dark gray on white"),
                ("#666666", "#FFFFFF", "Medium gray on white"),
                ("#999999", "#FFFFFF", "Light gray on white"),
                ("#0000FF", "#FFFFFF", "Blue on white"),
                ("#FF0000", "#FFFFFF", "Red on white"),
            ]

            for fg, bg, description in test_combinations:
                try:
                    ratio = calculate_contrast_ratio(fg, bg)
                    aa_pass = validate_contrast_ratio(fg, bg, "AA", "normal")
                    aaa_pass = validate_contrast_ratio(fg, bg, "AAA", "normal")

                    status = "✓ AAA" if aaa_pass else "✓ AA" if aa_pass else "✗ Fail"
                    results += f"{description}: {ratio:.2f}:1 ({status})\n"

                except Exception:
                    results += f"{description}: Unable to calculate\n"

            results += "\nWCAG Contrast Requirements:\n"
            results += "• AA Level: 4.5:1 for normal text, 3:1 for large text\n"
            results += "• AAA Level: 7:1 for normal text, 4.5:1 for large text\n"
            results += "• Large text: 18pt+ or 14pt+ bold\n"

            self.display_results(results)
            speak("Color contrast test complete")

        except Exception as e:
            self.display_results(f"Error testing color contrast: {str(e)}\n")
            speak("Error testing color contrast")

    def display_results(self, text: str):
        """Display results in the text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        self.results_text.config(state=tk.DISABLED)
        self.results_text.see(1.0)

    def run(self):
        """Run the demo application"""
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the main loop
        self.root.mainloop()

    def on_closing(self):
        """Handle application closing"""
        speak("Closing accessibility demo")
        self.root.destroy()


def main():
    """Main function to run the demo"""
    print("Starting Comprehensive Accessibility Demo...")
    print("This demo showcases all accessibility features of tkaria11y")
    print("Use Tab/Shift+Tab to navigate, Enter/Space to activate controls")
    print("Enable a screen reader for the full accessibility experience")

    try:
        demo = ComprehensiveAccessibilityDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
