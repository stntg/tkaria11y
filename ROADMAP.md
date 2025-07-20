# ROADMAP

## Vision

tkaria11y aims to be the definitive, zero-boilerplate accessibility toolkit for the entire Python GUI ecosystem—empowering developers to build inclusive, ARIA-compliant, screen-reader-ready desktop applications with minimal effort.

**Our Mission**: Make accessibility the default, not an afterthought, in Python GUI development.

---

## Milestones

### Version 0.1 (Alpha) ✅ COMPLETED

- ✅ Core accessibility mixin (`AccessibleMixin`) with `accessible_name`, `role`, `description`  
- ✅ Dynamic factory for zero-boilerplate `Accessible<Button/Entry/Label/...>` classes  
- ✅ TTS engine (`pyttsx3`) with focus/hover announcements and configurable settings  
- ✅ High-contrast theme system and OpenDyslexic font support with fallbacks  
- ✅ Enhanced keyboard navigation utilities (`<Tab>` / `<Shift-Tab>`) with logical focus order  
- ✅ Comprehensive unit tests (40+ tests) and CI for linting, type checking, stub generation  
- ✅ First “no-op” PyPI release to reserve `tkaria11y`

---

### Version 0.2 (Beta) 🚧 IN PROGRESS

- ✅ Runtime Widget Inspector (F2 toggle) showing widget tree and metadata  
- ✅ Automated stub-generator (`generate_stubs.py`) wired into CI and pre-commit  
- ✅ CLI codemod tool: swap plain Tkinter → `Accessible*` + infer `accessible_name` from `text=`  
- ✅ Expanded test coverage for inspector and codemod (40+ comprehensive tests)
- ✅ Comprehensive accessibility test suite (`a11y_test_suite/`)
- 🚧 Color-blind & low-vision palettes, WCAG contrast checker
- 🚧 Command-line flags and config file support for theme & a11y toggles
- 🚧 PyPI release and package distribution

---

### Version 0.3 (Release Candidate) 📋 PLANNED

- 🎯 **Enhanced OS Integration**:
  - Windows UIA (User Interface Automation) support
  - Linux AT-SPI (Assistive Technology Service Provider Interface)
  - macOS VoiceOver API integration
- 🔤 **Braille Support**: Display integration via `brlapi` and BRF export functionality
- 🎤 **Voice Control**: Speech-to-text command registry using `speech_recognition` or `Vosk`
- 🌍 **Internationalization**: Resource bundles, RTL/LTR text support, multi-language TTS
- ⚙️ **Settings Panel**: In-app configuration for themes, scaling, voices, and accessibility toggles
- 🔌 **Plugin System**: Extensible architecture with first community plugin (accessible charts)
- 📊 **WCAG Compliance**: Full WCAG 2.1 AA compliance testing and certification
- 🚀 **Performance**: Optimized TTS engine and reduced memory footprint

---

### Version 1.0 (Stable) 🎯 FUTURE

- 🏪 **Plugin Marketplace**: Architecture for publishing and installing third-party accessibility adapters
- 📊 **Analytics Dashboard**: Opt-in telemetry for TTS usage, focus-order analysis, and accessibility bottlenecks
- 🎓 **Interactive Tutorials**: Contextual help overlays and guided accessibility implementation
- 📚 **Documentation Site**: Complete MkDocs/Sphinx site with samples, API reference, and ARIA guidelines
- 🎉 **Stable Release**: Official PyPI 1.0 launch with long-term support commitment
- 🏆 **Certification**: Official accessibility certification and compliance verification tools
- 🤝 **Community**: Established contributor guidelines, governance, and community support channels

---

## Beyond 1.0 🚀 VISION

- 🤖 **AI-Powered Accessibility**: Machine learning-driven WCAG fix recommendations and automated accessibility auditing
- 👥 **Collaborative Auditing**: Real-time collaboration tools and annotation systems for accessibility reviews
- 🔗 **Multi-Framework Support**: Adapters for PyQt/PySide, wxPython, BeeWare/Toga, and other Python GUI toolkits
- 📋 **Certification Suite**: Comprehensive accessibility certification tools and automated compliance reporting
- 🌐 **Ecosystem Growth**: Community-driven marketplace for themes, speech engines, testing tools, and specialized widgets
- 🎯 **Enterprise Features**: Advanced analytics, team management, and enterprise-grade accessibility governance tools  

---

## How You Can Help 🤝

- ⭐ Star the repo and watch for new releases  
- 🐛 Report issues or request widgets you need  
- 🤖 Test the codemod on your existing Tkinter apps  
- 📚 Contribute guides, examples, or translations  
- 📦 Build plugins for charts, forms, or specialized controls  

Let’s make Tk projects accessible by default—one milestone at a time. 🚀
