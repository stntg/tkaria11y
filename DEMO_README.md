# tkaria11y Demo Applications

This directory contains comprehensive demo applications that showcase all the accessible widgets available in the tkaria11y framework.

## Demo Applications

### 1. Simple Demo (`simple_demo.py`)

A streamlined demonstration focusing on the most commonly used widgets.

**Features:**
- Basic Tkinter widgets (Button, Entry, Label, Text, Checkbutton, Radiobutton, Listbox)
- TTK widgets (TTKButton, TTKEntry, Combobox)
- CustomTkinter widgets (if available)
- Form-like interface with validation
- Interactive feedback with text-to-speech

**Usage:**
```bash
python simple_demo.py
```

### 2. Comprehensive Demo (`comprehensive_demo.py`)

A complete showcase of all available accessible widgets across all supported frameworks.

**Features:**
- **Standard Tkinter widgets**: All basic widgets with accessibility enhancements
- **TTK widgets**: Themed widgets with proper ARIA support
- **CustomTkinter widgets**: Modern UI widgets (if CustomTkinter is installed)
- **Interactive demo tab**: Dynamic list management with file operations
- **Full menu system**: File operations, view options, help system
- **Keyboard shortcuts**: Full keyboard navigation support
- **Progress indicators**: Animated progress bars
- **Tree view**: Hierarchical data display
- **Tabbed interface**: Organized widget categories

**Usage:**
```bash
python comprehensive_demo.py
```

## Widget Categories Demonstrated

### Standard Tkinter Widgets
- `AccessibleButton` - Clickable buttons with TTS feedback
- `AccessibleEntry` - Single-line text input
- `AccessibleLabel` - Text display labels
- `AccessibleText` - Multi-line text areas
- `AccessibleCheckbutton` - Checkbox controls
- `AccessibleRadiobutton` - Radio button groups
- `AccessibleScale` - Slider controls
- `AccessibleScrollbar` - Scrolling controls
- `AccessibleListbox` - List selection widgets
- `AccessibleFrame` - Container widgets
- `AccessibleLabelFrame` - Labeled containers
- `AccessibleCanvas` - Drawing areas
- `AccessibleSpinbox` - Numeric input with spin controls
- `AccessiblePanedWindow` - Resizable panes

### TTK (Themed) Widgets
- `AccessibleTTKButton` - Themed buttons
- `AccessibleTTKEntry` - Themed text input
- `AccessibleTTKLabel` - Themed labels
- `AccessibleTTKCheckbutton` - Themed checkboxes
- `AccessibleTTKRadiobutton` - Themed radio buttons
- `AccessibleTTKScale` - Themed sliders
- `AccessibleTTKScrollbar` - Themed scrollbars
- `AccessibleTTKFrame` - Themed containers
- `AccessibleTTKLabelFrame` - Themed labeled containers
- `AccessibleNotebook` - Tabbed interfaces
- `AccessibleTTKProgressbar` - Progress indicators
- `AccessibleTTKSeparator` - Visual separators
- `AccessibleTreeview` - Hierarchical data display
- `AccessibleCombobox` - Dropdown selection
- `AccessibleTTKSpinbox` - Themed numeric input
- `AccessibleTTKPanedWindow` - Themed resizable panes

### CustomTkinter Widgets (Optional)
- `AccessibleCTKButton` - Modern styled buttons
- `AccessibleCTKEntry` - Modern text input
- `AccessibleCTKLabel` - Modern labels
- `AccessibleCTKCheckBox` - Modern checkboxes
- `AccessibleCTKRadioButton` - Modern radio buttons
- `AccessibleCTKSlider` - Modern sliders
- `AccessibleCTKScrollbar` - Modern scrollbars
- `AccessibleCTKFrame` - Modern containers
- `AccessibleCTKTabview` - Modern tabbed interface
- `AccessibleCTKProgressBar` - Modern progress bars
- `AccessibleCTKSwitch` - Toggle switches
- `AccessibleCTKComboBox` - Modern dropdowns
- `AccessibleCTKTextbox` - Modern text areas
- `AccessibleCTKScrollableFrame` - Scrollable containers

## Accessibility Features Demonstrated

### ARIA Support
- Proper accessible names for all widgets
- Role-based announcements
- State change notifications
- Focus management

### Text-to-Speech Integration
- Automatic announcements on focus
- Interactive feedback
- State change notifications
- Error announcements

### Keyboard Navigation
- Tab order management
- Arrow key navigation for lists and trees
- Keyboard shortcuts (Ctrl+N, Ctrl+O, Ctrl+S, etc.)
- Enter/Space activation

### Visual Accessibility
- High-contrast theme support
- Dyslexic-friendly fonts (optional)
- Clear focus indicators
- Consistent visual hierarchy

### Screen Reader Support
- Compatible with NVDA, JAWS, and other screen readers
- Proper widget labeling
- State announcements
- Navigation cues

## Requirements

### Basic Requirements
- Python 3.9+
- tkinter (usually included with Python)
- tkaria11y package

### Optional Requirements
- CustomTkinter (for CTK widgets demonstration)
- pyttsx3 (for text-to-speech, included with tkaria11y)

### Installation
```bash
# Install tkaria11y
pip install tk-a11y

# Optional: Install CustomTkinter for full demo
pip install customtkinter
```

## Usage Tips

### For Developers
1. **Study the code**: Both demos are well-commented and show best practices
2. **Test accessibility**: Use screen readers to test the widgets
3. **Customize**: Modify the demos to test your specific use cases
4. **Learn patterns**: See how accessible_name parameters are used

### For Users with Disabilities
1. **Screen readers**: All widgets work with NVDA, JAWS, and other screen readers
2. **Keyboard navigation**: Use Tab/Shift+Tab to navigate, Enter/Space to activate
3. **Text-to-speech**: Enable TTS for audio feedback
4. **High contrast**: Use the high-contrast theme for better visibility

### Keyboard Shortcuts (Comprehensive Demo)
- `Ctrl+N` - New demo data
- `Ctrl+O` - Load demo data from file
- `Ctrl+S` - Save demo data to file
- `Ctrl+Q` - Quit application
- `Ctrl+T` - Toggle theme
- `F1` - Show keyboard shortcuts help

## Troubleshooting

### Common Issues

**ImportError for CustomTkinter widgets:**
- CustomTkinter is optional. The demos will work without it.
- Install with: `pip install customtkinter`

**No text-to-speech:**
- Ensure pyttsx3 is installed: `pip install pyttsx3`
- Check system TTS settings

**Widgets not announced by screen reader:**
- Ensure screen reader is running
- Check that accessible_name parameters are provided
- Verify screen reader compatibility

### Performance Notes
- The comprehensive demo loads many widgets and may take a moment to start
- TTS initialization may cause a brief delay on first use
- Large tree views may impact performance on older systems

## Contributing

These demos serve as both examples and test cases for the tkaria11y framework. When adding new widgets or features:

1. Update the appropriate demo to showcase the new functionality
2. Ensure proper accessible_name parameters are used
3. Test with screen readers and keyboard navigation
4. Update this documentation

## License

These demo applications are part of the tkaria11y project and follow the same license terms.