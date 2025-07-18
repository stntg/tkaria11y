import tkinter as tk
from tkaria11y.widgets import (
    AccessibleButton,
    AccessibleEntry,
    AccessibleLabel,
    AccessibleCheckbutton,
    AccessibleRadiobutton,
    AccessibleScale,
    AccessibleListbox,
    AccessibleFrame,
    _WIDGET_MAP,
)


def test_accessible_button_inherits_tk_button():
    """Test AccessibleButton inherits from tk.Button"""
    root = tk.Tk()
    btn = AccessibleButton(root, accessible_name="Test")
    assert isinstance(btn, tk.Button)
    # Should have bound events when name present
    events = btn.bind()
    assert "<FocusIn>" in events
    assert "<Enter>" in events
    root.destroy()


def test_accessible_button_attributes():
    """Test AccessibleButton has correct attributes"""
    root = tk.Tk()
    btn = AccessibleButton(root, accessible_name="Test Button")
    assert btn.accessible_name == "Test Button"
    assert btn.accessible_role == "button"
    root.destroy()


def test_accessible_entry_inherits_tk_entry():
    """Test AccessibleEntry inherits from tk.Entry"""
    root = tk.Tk()
    entry = AccessibleEntry(root, accessible_name="Test Entry")
    assert isinstance(entry, tk.Entry)
    assert entry.accessible_name == "Test Entry"
    assert entry.accessible_role == "textbox"
    root.destroy()


def test_accessible_label_inherits_tk_label():
    """Test AccessibleLabel inherits from tk.Label"""
    root = tk.Tk()
    label = AccessibleLabel(root, accessible_name="Test Label")
    assert isinstance(label, tk.Label)
    assert label.accessible_name == "Test Label"
    assert label.accessible_role == "label"
    root.destroy()


def test_accessible_checkbutton_inherits_tk_checkbutton():
    """Test AccessibleCheckbutton inherits from tk.Checkbutton"""
    root = tk.Tk()
    cb = AccessibleCheckbutton(root, accessible_name="Test Checkbox")
    assert isinstance(cb, tk.Checkbutton)
    assert cb.accessible_name == "Test Checkbox"
    assert cb.accessible_role == "checkbox"
    root.destroy()


def test_accessible_radiobutton_inherits_tk_radiobutton():
    """Test AccessibleRadiobutton inherits from tk.Radiobutton"""
    root = tk.Tk()
    rb = AccessibleRadiobutton(root, accessible_name="Test Radio")
    assert isinstance(rb, tk.Radiobutton)
    assert rb.accessible_name == "Test Radio"
    assert rb.accessible_role == "radio"
    root.destroy()


def test_accessible_scale_inherits_tk_scale():
    """Test AccessibleScale inherits from tk.Scale"""
    root = tk.Tk()
    scale = AccessibleScale(root, accessible_name="Test Slider")
    assert isinstance(scale, tk.Scale)
    assert scale.accessible_name == "Test Slider"
    assert scale.accessible_role == "slider"
    root.destroy()


def test_accessible_listbox_inherits_tk_listbox():
    """Test AccessibleListbox inherits from tk.Listbox"""
    root = tk.Tk()
    lb = AccessibleListbox(root, accessible_name="Test Listbox")
    assert isinstance(lb, tk.Listbox)
    assert lb.accessible_name == "Test Listbox"
    assert lb.accessible_role == "listbox"
    root.destroy()


def test_accessible_frame_inherits_tk_frame():
    """Test AccessibleFrame inherits from tk.Frame"""
    root = tk.Tk()
    frame = AccessibleFrame(root, accessible_name="Test Frame")
    assert isinstance(frame, tk.Frame)
    assert frame.accessible_name == "Test Frame"
    assert frame.accessible_role == "region"
    root.destroy()


def test_widget_map_completeness():
    """Test that all widgets in _WIDGET_MAP are properly created"""
    root = tk.Tk()

    for name, (role, base_class) in _WIDGET_MAP.items():
        cls_name = f"Accessible{name}"

        # Import the class dynamically
        from tkaria11y import widgets

        widget_class = getattr(widgets, cls_name)

        # Create instance
        widget = widget_class(root, accessible_name=f"Test {name}")

        # Check inheritance
        assert isinstance(widget, base_class)

        # Check attributes
        assert widget.accessible_name == f"Test {name}"
        assert widget.accessible_role == role

    root.destroy()


def test_widget_without_accessible_name():
    """Test widgets work without accessible_name"""
    root = tk.Tk()
    btn = AccessibleButton(root)
    assert btn.accessible_name == ""
    assert btn.accessible_role == "button"
    root.destroy()


def test_widget_with_description():
    """Test widgets with accessible_description"""
    root = tk.Tk()
    btn = AccessibleButton(
        root,
        accessible_name="Test Button",
        accessible_description="This is a test button",
    )
    assert btn.accessible_name == "Test Button"
    assert btn.accessible_description == "This is a test button"
    root.destroy()
