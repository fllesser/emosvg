import pytest


def test_no_emoji_text(font_path, cache_dir):
    from PIL import Image, ImageFont

    import emosvg

    font = ImageFont.truetype(font_path, 24)
    with Image.new("RGB", (3000, 2100), (255, 248, 220)) as image:  # 纸黄背景
        emosvg.text(image, (10, 10), "Hello World", font, fill=(0, 0, 0))
        image.save(cache_dir / "no_emoji_text.png")


def test_other_font():
    from PIL import ImageFont

    import emosvg

    # test ImageFont
    font = ImageFont.load_default_imagefont()
    pytest.raises(ValueError, emosvg.get_font_height, font)
    pytest.raises(ValueError, emosvg.get_font_size, font)

    # test transparent font
    font = ImageFont.TransposedFont(font)
    pytest.raises(ValueError, emosvg.get_font_height, font)
    pytest.raises(ValueError, emosvg.get_font_size, font)


def test_no_text(font_path):
    from PIL import Image, ImageFont

    import emosvg

    font = ImageFont.truetype(font_path, 24)
    with Image.new("RGB", (3000, 2100), (255, 248, 220)) as image:  # 纸黄背景
        emosvg.text(image, (10, 10), "", font, fill=(0, 0, 0))


def test_no_emoji():
    import emosvg

    emoji = "1"
    width = 100
    height = 100

    emj_img = emosvg.get_emoji_image(emoji, width, height)

    assert emj_img is None


def test_wrap_text_no_text():
    from PIL import ImageFont

    import emosvg

    font = ImageFont.load_default_imagefont()
    lines = emosvg.wrap_text("", font, 100)
    assert lines == []

