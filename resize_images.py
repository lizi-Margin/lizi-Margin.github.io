#!/usr/bin/env python
"""
Resize my_photo.jpg to match various image requirements for the site.
"""
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'pillow'])
    from PIL import Image

def resize_and_save(source_path, target_path, size, background_color=(255, 255, 255)):
    """
    Resize image to target size, centering on a background.
    """
    img = Image.open(source_path)

    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', size, background_color)
        # Convert to RGB first
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2),
                        img if img.mode == 'RGBA' else None)
        result = background
    else:
        # For JPEG, resize with aspect ratio preservation and center
        img.thumbnail(size, Image.Resampling.LANCZOS)
        result = Image.new('RGB', size, background_color)
        offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        result.paste(img, offset)

    result.save(target_path, quality=95)
    print(f"[OK] Created {target_path} ({size[0]}x{size[1]})")

def main():
    source = Path("images/my_photo.jpg")

    if not source.exists():
        print(f"Error: {source} not found!")
        return

    # Open original to check dimensions
    original = Image.open(source)
    print(f"Original photo dimensions: {original.size}")
    print(f"Original photo format: {original.format}\n")

    # Define target sizes and files
    targets = [
        ("images/android-chrome-512x512.png", (512, 512)),
        ("images/android-chrome-192x192.png", (192, 192)),
        ("images/apple-touch-icon.png", (180, 180)),
        ("images/favicon-32x32.png", (32, 32)),
        ("images/favicon-16x16.png", (16, 16)),
        ("images/500x300.png", (500, 300)),
    ]

    print("Resizing images for the following files:")
    for target_path, size in targets:
        resize_and_save(str(source), target_path, size)

    print("\nAll images have been successfully resized and saved!")

if __name__ == "__main__":
    main()
