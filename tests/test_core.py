from pathlib import Path


def test_get_emoji_image():
    from emosvg.core import get_emoji_image

    emoji = "😀"
    width = 100
    height = 100

    emj_img = get_emoji_image(emoji, width, height)

    assert emj_img is not None
    assert emj_img.width == width
    assert emj_img.height == height


def test_text(font_path: Path, cache_dir: Path):
    from PIL import Image, ImageFont

    import emosvg

    string = "笑脸😀笑脸 smile😀smile"
    image = Image.new("RGB", (400, 200), (255, 255, 255))
    font = ImageFont.truetype(font_path, 24)
    emosvg.text(image, (10, 10), string, font=font, fill=(0, 0, 0))
    image.save(cache_dir / "smile.png")


def test_combo_emoji(font_path: Path, cache_dir: Path):
    from PIL import Image, ImageFont

    import emosvg

    lines = ["👍🏻 👍🏼 👍🏽 👍🏾 👍🏿", "👨‍👩‍👧‍👦 👩‍👩‍👧‍👦 👨‍👨‍👧‍👦 👩‍👦 👨‍👦"]
    image = Image.new("RGB", (400, 200), (255, 255, 255))
    font = ImageFont.truetype(font_path, 24)
    emosvg.text(image, (10, 10), lines, font=font, fill=(0, 0, 0))
    image.save(cache_dir / "combo.png")
