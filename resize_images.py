#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def resize_image(image_path: Path, output_path: Path, max_size: int) -> bool:
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("Error: Pillow is required. Install it with: pip install pillow", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Resizing: {image_path.name}...")
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            ext = output_path.suffix.lower()

            if ext in {".jpg", ".jpeg"}:
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                img.save(output_path, format="JPEG", quality=90)
            elif ext == ".png":
                img.save(output_path, format="PNG", optimize=True)
            elif ext == ".webp":
                img.save(output_path, format="WEBP", quality=90)
            else:
                img.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="c-cli resize-images",
        description="Resize images to a maximum width/height while maintaining aspect ratio (never upscales)."
    )
    parser.add_argument("target", help="Path to image file or directory containing images")
    parser.add_argument("--maxsize", type=int, default=2200, help="Max dimension in pixels (default: 2200)")

    args = parser.parse_args()
    target = Path(args.target).expanduser().resolve()

    if not target.exists():
        print(f"Error: '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if target.is_file():
        if target.suffix.lower() not in SUPPORTED_EXTENSIONS:
            valid = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            print(f"Error: '{target.name}' is not supported ({valid}).", file=sys.stderr)
            sys.exit(1)

        out_file = target.with_name(f"{target.stem}_resized{target.suffix}")
        if resize_image(target, out_file, args.maxsize):
            print(f"Done! Output: {out_file}")
            sys.exit(0)
        sys.exit(1)

    if target.is_dir():
        output_folder = target / "processed"
        images = [f for f in target.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]

        if not images:
            print(f"No supported images found in '{target}'.")
            sys.exit(0)

        print(f"Processing images in: {target}")
        print(f"Target max dimension: {args.maxsize}px")
        print(f"Output folder: {output_folder}")
        print("-" * 40)

        success_count = 0
        for img in images:
            out = output_folder / img.name
            if resize_image(img, out, args.maxsize):
                success_count += 1

        print("-" * 40)
        print(f"Done! Successfully processed {success_count}/{len(images)} images.")
        if success_count < len(images):
            sys.exit(1)


if __name__ == "__main__":
    main()
