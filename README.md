# QWDownloader

A modern, easy-to-use downloader for QuakeWorld maps (.bsp) from [maps.quakeworld.nu](https://maps.quakeworld.nu/all/).

![QWDownloader GUI](https://raw.githubusercontent.com/ChumaSuey/QWDownloader/master/logo_placeholder.png) <!-- Note: Replace with actual screenshot if available -->

## Features

- **Sleek GUI**: Built with Tkinter and the beautiful **Sun-Valley** dark theme.
- **Efficient Downloading**: Automatically scans the QuakeWorld map database.
- **Duplicate Prevention**: Intelligently checks your local folder to skip files you already have.
- **Responsive Design**: Uses multi-threading so the interface never freezes during long downloads.
- **Status Log**: Real-time feedback on every download action.
- **Shortcuts**:
  - `Ctrl + D`: Start Download
  - `Ctrl + S`: Stop Download

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ChumaSuey/QWDownloader.git
   cd QWDownloader
   ```

2. **Install dependencies**:

   ```bash
   pip install requests beautifulsoup4 sv-ttk
   ```

## Usage

Simply run the GUI version:

```bash
python gui_main.py
```

Or use the legacy CLI versions (`main.py` or `main2.0.py`) if preferred.

## Automation & Testing

The project includes an automation suite located in the `/tests` folder:

- `test_manual_stop.py`: Automates the UI to start downloading.
- `test_timed_stop.py`: Runs a 10-second test of the downloader.

## Credits

- **Author**: [ChumaSuey](https://github.com/ChumaSuey)
- **Suggestions & Improvements**: Admer, Em3rald.
- **Theme**: [Sun-Valley TTK Theme](https://github.com/rdbende/Sun-Valley-ttk-theme)

---
*Created with ❤️ for the QuakeWorld community.*
