import logging
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw
from PIL.ImageFont import ImageFont, FreeTypeFont, TransposedFont

from . import helper
from .helper import NodeType

PILImage = Image.Image
PILDraw = ImageDraw.ImageDraw
FontT = ImageFont | FreeTypeFont | TransposedFont
ColorT = int | str | tuple[int, int, int] | tuple[int, int, int, int]

# Define the path to the resources directory
RESOURCE_DIR = Path(__file__).parent / "resources"
EMOJI_SVG_DIR = RESOURCE_DIR / "openmoji-svg-color"


def get_emoji_svg_path(emoji: str) -> Path:
    """
    Converts a unicode emoji string to the corresponding SVG file path.
    Example: "😀" -> ".../1F600.svg"
    """
    # Convert emoji to hex string sequence
    # e.g. "😀" -> "1F600"
    codepoints = []
    for char in emoji:
        codepoints.append(f"{ord(char):X}")

    filename = "-".join(codepoints) + ".svg"
    file_path = EMOJI_SVG_DIR / filename

    if not file_path.exists():
        # Try checking if there are variant selectors to remove or handle
        # For now, just raise if not found
        raise FileNotFoundError(
            f"Emoji SVG not found for {emoji} (looked for {filename})"
        )

    return file_path


def get_emoji_bytes(emoji: str, width: float, height: float) -> bytes | None:
    svg_file = get_emoji_svg_path(emoji)

    png_data: bytes | None = cairosvg.svg2png(
        url=str(svg_file), output_width=width, output_height=height
    )

    return png_data


def get_emoji_pil_image(emoji: str, width: float, height: float) -> PILImage | None:
    png_data = get_emoji_bytes(emoji, width, height)

    if png_data is None:
        return None

    # Create PIL Image from bytes
    image = Image.open(BytesIO(png_data)).convert("RGBA")

    return image


def text(
    image: PILImage,
    xy: tuple[int, int],
    lines: list[str] | str,
    font: FontT,
    *,
    fill: ColorT | None = None,
    line_height: int | None = None,
    scale: float = 1.1,
) -> None:
    """Text rendering method with Unicode and optional Discord emoji support.

    Parameters
    ----------
    image: PILImage
        The image to render onto
    xy: tuple[int, int]
        Rendering position (x, y)
    lines: list[str]
        The text lines to render
    font: FontT
        The font to use
    fill: ColorT | None
        Text color, defaults to black
    line_height: int | None
        Line height, defaults to font height
    scale: float
        Emoji scale factor, defaults to 1.1
    """
    if not lines:
        return

    x, y = xy
    draw = ImageDraw.Draw(image)
    line_height = line_height or get_font_height(font)

    if isinstance(lines, str):
        lines = lines.splitlines()

    # Check if lines has emoji
    if not helper.contains_emoji(lines):
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += line_height
        return

    # Parse lines into nodes
    nodes_lst = helper.parse_lines(lines)

    emj_set: set[str] = {
        node.content
        for nodes in nodes_lst
        for node in nodes
        if node.type is NodeType.EMOJI
    }
    logging.debug(f"Collecting {len(emj_set)} emojis: {emj_set}")

    # Render each line
    font_size = get_font_size(font)
    emoji_size = font_size * scale
    x_diff = int((emoji_size - font_size) / 2)
    y_diff = int((emoji_size - line_height) / 2)
    emj_map = {
        emj: get_emoji_pil_image(
            emj,
            emoji_size,
            emoji_size,
        )
        for emj in emj_set
    }

    for line in nodes_lst:
        cur_x = x

        for node in line:
            if node.type is NodeType.EMOJI:
                emj_img = emj_map.get(node.content)
                if emj_img is None:
                    logging.warning(f"Emoji not found: {node.content}")
                    continue
                image.paste(emj_img, (cur_x - x_diff, y - y_diff), emj_img)
                cur_x += int(font_size)
            else:
                draw.text((cur_x, y), node.content, font=font, fill=fill)
                cur_x += int(font.getlength(node.content))

        y += line_height


def get_font_size(font: FontT) -> float:
    match font:
        case FreeTypeFont():
            return font.size
        case TransposedFont():
            return get_font_size(font.font)
        case ImageFont():
            raise ValueError("Not support ImageFont")


def get_font_height(font: FontT) -> int:
    match font:
        case FreeTypeFont():
            ascent, descent = font.getmetrics()
            return ascent + descent
        case TransposedFont():
            return get_font_height(font.font)
        case ImageFont():
            raise ValueError("Not support ImageFont")
