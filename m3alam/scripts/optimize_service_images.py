from __future__ import annotations

from pathlib import Path

from PIL import Image


def optimize_service_images(source_dir: Path, output_dir: Path, *, size: int = 420, quality: int = 78) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for source in sorted(source_dir.glob("*.png")):
        target = output_dir / f"{source.stem}.webp"
        with Image.open(source) as image:
            image.thumbnail((size, size), Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            left = (size - image.width) // 2
            top = (size - image.height) // 2
            canvas.alpha_composite(image.convert("RGBA"), (left, top))
            canvas.save(target, "WEBP", quality=quality, method=6)
        count += 1
    return count


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "static" / "images" / "services"
    count = optimize_service_images(root, root / "thumbs")
    print(f"Optimized {count} service images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
