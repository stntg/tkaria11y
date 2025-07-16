# ROADMAP

## Vision

tk-a11y aims to be the definitive, zero-boilerplate accessibility toolkit for the entire Tk ecosystem—empowering developers to build inclusive, ARIA-style, screen-reader-ready desktop apps in pure Python.

---

## Milestones

### Version 0.1 (Alpha)

- Core accessibility mixin (`AccessibleMixin`) with `accessible_name`, `role`, `description`  
- Dynamic factory for zero-boilerplate `Accessible<Button/Entry/Label/...>` classes  
- Basic TTS engine (`pyttsx3`) with focus/hover announcements  
- High-contrast theme toggle and OpenDyslexic font support  
- Keyboard navigation utilities (`<Tab>` / `<Shift-Tab>`)  
- Initial unit tests and CI for linting, type checking, stub generation, and pytest  
- First “no-op” PyPI release to reserve `tk-a11y`

---

### Version 0.2 (Beta)

- Runtime Widget Inspector (F2 toggle) showing widget tree and metadata  
- Automated stub-generator (`generate_stubs.py`) wired into CI and pre-commit  
- CLI codemod prototype: swap plain Tkinter → `Accessible*` + infer `accessible_name` from `text=`  
- Color-blind & low-vision palettes, WCAG contrast checker  
- Command-line flags and config file support for theme & a11y toggles  
- Expanded test coverage for inspector and codemod

---

### Version 0.3 (Release Candidate)

- Deep OS-level integration:
  - Windows UIA
  - Linux AT-SPI
  - macOS VoiceOver API  
- Braille display support via `brlapi` and BRF exporter  
- Speech-to-text/voice-control command registry using `speech_recognition` or `Vosk`  
- Internationalization framework: resource bundles, RTL/LTR support  
- In-app Settings pane for themes, scaling, voices, and a11y toggles  
- First community plugin (e.g., chart widget with pattern overlays)

---

### Version 1.0 (Stable)

- Plugin architecture & marketplace: publish and install third-party adapters  
- Opt-in analytics dashboard: TTS usage, focus-order anomalies, a11y bottlenecks  
- Interactive tutorials & contextual help overlays  
- Full documentation site (MkDocs/Sphinx) with samples, API reference, ARIA guidelines  
- Official PyPI launch of 1.0-stable release

---

## Beyond 1.0

- AI-driven accessibility suggestions (WCAG fix recommendations)  
- Real-time collaboration and annotation for A11y audits  
- Adapters for other Python GUI toolkits (PyQt/PySide, wxPython, BeeWare/Toga)  
- Accessibility certification tools and compliance reports  
- Community-driven ecosystem: themes, speech engines, testing tools  

---

## How You Can Help

- ⭐ Star the repo and watch for new releases  
- 🐛 Report issues or request widgets you need  
- 🤖 Test the codemod on your existing Tkinter apps  
- 📚 Contribute guides, examples, or translations  
- 📦 Build plugins for charts, forms, or specialized controls  

Let’s make Tk projects accessible by default—one milestone at a time. 🚀