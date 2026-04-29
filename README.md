# AutoPro -- Wand (wemod) Patcher GUI

**AutoPro** is a desktop utility built with Python and Tkinter that
demonstrates automated patching workflows for Electron-based
applications.\
It provides a graphical interface to manage application resources,
create backups, modify extracted files, and restore the original state
when needed.

This project is intended for **educational and research purposes**,
showcasing how Electron application packages (`.asar`) can be
programmatically handled.

------------------------------------------------------------------------

## Features

-   Modern graphical interface (Tkinter-based)
-   Automatic detection of installed applications
-   Extraction and repackaging of `.asar` archives
-   Automated file modification workflow
-   Automatic backup system before modification
-   One-click restoration of original files
-   Real-time logging console
-   Threaded operations to keep the UI responsive

------------------------------------------------------------------------

## Project Overview

AutoPro demonstrates a full patching pipeline:

1.  Detect running application processes
2.  Stop the target process safely
3.  Create a secure backup of application resources
4.  Extract the Electron `app.asar` archive
5.  Apply automated modifications to source files
6.  Repackage the modified archive
7.  Restore the application when required

------------------------------------------------------------------------

## Architecture

AutoPro/
├── GUI/
│   ├── Command Center
│   ├── Logging Console
├── Core/
│   ├── Process Management/
│   │   ├── Detection
│   │   ├── Safe Termination
│   │   └── Restart Handling
│   └── File Operations/
│       ├── Backup System
│       ├── Extraction
│       ├── Modification
│       └── Repackaging
└── Recovery/
    └── Restore System (Revert to original state)

------------------------------------------------------------------------

## Requirements

### Software

-   Python
-   Node.js
-   npm / npx

### Python Libraries

-   tkinter
-   glob
-   subprocess
-   threading
-   shutil
-   re

Most libraries are included in the Python standard library.

------------------------------------------------------------------------

## Installation

``` bash
git clone https://github.com/amiayweb/Wand-Wemod-Pro-Patcher.git
cd Wand-Wemod-Pro-Patcher
python patcher.py
```

------------------------------------------------------------------------

## License

This project is provided for educational and research purposes only.
