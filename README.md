# ocr-clip

Drag-select any text visible on screen and copy it to your clipboard via OCR.
Works anywhere text is rendered — terminals, PDFs, browser pages, apps that block copy-paste.

## Install

Requires [tesseract](https://github.com/tesseract-ocr/tesseract) on your system:

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

pip install ocr-clip
```

## Usage

```bash
ocr-clip
```

| Hotkey | Action |
|---|---|
| `Ctrl+Shift+C` | Activate overlay — click and drag to select text |
| `Escape` | Cancel selection |
| `Ctrl+Shift+Q` | Quit |

The selected region is OCR'd and the text lands in your clipboard instantly.
Selection automatically pads 8px on each edge to avoid clipping letters at boundaries.

## Autostart (Linux)

The installer places a `.desktop` entry in `~/.config/autostart/` so ocr-clip launches on login automatically.
