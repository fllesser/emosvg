import pytest


def test_no_emoji_text(font_path, cache_dir):
    from PIL import Image, ImageFont

    import emosvg

    font = ImageFont.truetype(font_path, 24)
    with Image.new("RGB", (3000, 2100), (255, 248, 220)) as image:  # 纸黄背景
        emosvg.text_without_wrap(image, (10, 10), "Hello World", font, fill=(0, 0, 0))
        image.save(cache_dir / "no_emoji_text.png")


def test_other_font():
    from PIL import ImageFont

    from emosvg.core import get_font_size, get_font_height

    # test ImageFont
    font = ImageFont.load_default_imagefont()
    pytest.raises(ValueError, get_font_height, font)
    pytest.raises(ValueError, get_font_size, font)

    # test transparent font
    font = ImageFont.TransposedFont(font)
    pytest.raises(ValueError, get_font_height, font)
    pytest.raises(ValueError, get_font_size, font)


def test_no_text(font_path):
    from PIL import Image, ImageFont

    import emosvg

    font = ImageFont.truetype(font_path, 24)
    with Image.new("RGB", (3000, 2100), (255, 248, 220)) as image:  # 纸黄背景
        emosvg.text_without_wrap(image, (10, 10), "", font, fill=(0, 0, 0))


def test_no_emoji():
    from emosvg.core import get_emoji_image

    emoji = "1"
    width = 100
    height = 100

    emj_img = get_emoji_image(emoji, width, height)

    assert emj_img is None
