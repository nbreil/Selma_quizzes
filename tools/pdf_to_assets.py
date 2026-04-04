#!/usr/bin/env python3
"""
pdf_to_assets.py — Convert a PDF into a text file + extracted images.

Usage:
    python3 tools/pdf_to_assets.py path/to/file.pdf [output_dir]

Output (placed in output_dir, defaults to a folder named after the PDF):
    text.txt          — full text, one section per page
    images/           — all images found in the PDF, named img_p{page}_{n}.{ext}
    summary.txt       — page count + image count summary
"""

import sys
import os
import io
from pathlib import Path

try:
    import pypdf
except ImportError:
    print("pypdf not installed. Run: pip3 install pypdf")
    sys.exit(1)

# Optional: pillow for image saving
try:
    from PIL import Image as PILImage
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("[warn] Pillow not installed — images will be saved as raw bytes when possible. Run: pip3 install Pillow")


def extract(pdf_path: str, output_dir=None):
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    if output_dir is None:
        output_dir = pdf_path.parent / pdf_path.stem
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    print(f"PDF: {pdf_path.name}  |  {num_pages} pages")

    # ── Text extraction ──────────────────────────────────────────────────────
    text_parts = []
    total_chars = 0
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        total_chars += len(text.strip())
        text_parts.append(f"{'='*60}\nPAGE {i+1}\n{'='*60}\n{text}\n")

    text_file = output_dir / "text.txt"
    text_file.write_text("\n".join(text_parts), encoding="utf-8")
    print(f"Text saved → {text_file}")

    if total_chars == 0:
        print()
        print("=" * 60)
        print("[WARN] PDF appears to be image-based (scanned) — no text extracted.")
        print("  Next step: read each image in images/ visually and update text.txt")
        print("  with the full transcribed content, page by page.")
        print("=" * 60)
    else:
        print(f"  ({total_chars} characters extracted)")

    # ── Image extraction ─────────────────────────────────────────────────────
    img_count = 0
    for i, page in enumerate(reader.pages):
        try:
            images = page.images
        except Exception:
            continue
        for j, img in enumerate(images):
            ext = Path(img.name).suffix.lower() if img.name else ".bin"
            if not ext or ext not in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"):
                ext = ".jpg"  # default assumption
            out_name = images_dir / f"img_p{i+1}_{j+1}{ext}"
            try:
                if HAS_PILLOW:
                    pil_img = PILImage.open(io.BytesIO(img.data))
                    # Normalize to PNG for consistency
                    out_name = out_name.with_suffix(".png")
                    pil_img.save(str(out_name))
                else:
                    out_name.write_bytes(img.data)
                img_count += 1
            except Exception as e:
                print(f"  [warn] Could not save image p{i+1}_{j+1}: {e}")

    print(f"Images saved → {images_dir}  ({img_count} images)")

    # ── Summary ──────────────────────────────────────────────────────────────
    summary = (
        f"Source: {pdf_path.name}\n"
        f"Pages:  {num_pages}\n"
        f"Images: {img_count}\n"
        f"Output: {output_dir}\n"
    )
    (output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    return output_dir


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
