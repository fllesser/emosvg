"""Pytest configuration and shared fixtures."""

import sys
import logging
from pathlib import Path

import pytest

# 共享的测试资源路径
RESOURCE_DIR = Path(__file__).parent / "resource"
FONT_PATH = RESOURCE_DIR / "HYSongYunLangHeiW-1.ttf"
LXGW_FONT_PATH = RESOURCE_DIR / "LXGWZhenKaiGB-Regular.ttf"
CACHE_DIR = Path() / ".cache"

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)


@pytest.fixture(scope="session")
def font_path() -> Path:
    """返回测试字体文件路径。"""
    return FONT_PATH


@pytest.fixture(scope="session")
def lxgw_font_path() -> Path:
    """返回测试字体文件路径。"""
    return LXGW_FONT_PATH


@pytest.fixture(scope="session")
def cache_dir() -> Path:
    """返回缓存目录路径。"""
    clean_dir(CACHE_DIR)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def clean_dir(cache_dir: Path):
    if not cache_dir.exists():
        return
    for fd in cache_dir.glob("*"):
        if fd.is_dir():
            clean_dir(fd)
            fd.rmdir()
        else:
            fd.unlink()
