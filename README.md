# screen-ocr-clipboard

Drag-select any text visible on screen and copy it to your clipboard via OCR.
Built as a workaround for apps that block copy-paste (e.g. Claude's web terminal output).

## Install

Requires [tesseract](https://github.com/tesseract-ocr/tesseract) on your system:

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# Then install the tool
pip install git+https://github.com/staticplayHub/claude-copy-paste-workaround.git
```

## Usage

```bash
screen-ocr
```

| Hotkey | Action |
|---|---|
| `Ctrl+Shift+C` | Activate overlay — click and drag to select text |
| `Escape` | Cancel selection |
| `Ctrl+Shift+Q` | Quit |

The selected region is OCR'd and the text lands in your clipboard instantly.

## Autostart (Linux)

Copy the included `.desktop` entry to autostart:

```bash
cp screen-ocr-clipboard.desktop ~/.config/autostart/
```
