# resize-images-script

CLI tool to downscale images to a maximum width or height while maintaining aspect ratio. It never upscales and automatically corrects EXIF orientation.

## Requirements

- Python 3
- Pillow:
  ```bash
  pip install pillow
  ```

## Supported Formats

- `.jpg`, `.jpeg` (saved at 90% quality; RGBA converted to RGB)
- `.png` (optimized)
- `.webp` (saved at 90% quality)

## Usage

### Single Image

Resizes the image and saves it as `<filename>_resized.<ext>` in the same folder:

```bash
python3 resize_images.py path/to/image.jpg
```

Custom max value of the biggest side (default is `2200` px):

```bash
python3 resize_images.py path/to/image.jpg --maxsize 1600
```

### Directory (Batch)

Resizes all supported images in the target directory and saves them to a `processed/` subfolder:

```bash
python3 resize_images.py path/to/images/
python3 resize_images.py path/to/images/ --maxsize 1600
```

## Options

| Argument | Description | Default |
| --- | --- | --- |
| `target` | Path to an image file or directory | *(Required)* |
| `--maxsize` | Maximum size of the biggest side (either width or height) in pixels | `2200` |

## Note

I use this program through a shell script as a part of my custom toolkit. Here are the contents of that shell script file:
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/resize_images.py" "$@"

```