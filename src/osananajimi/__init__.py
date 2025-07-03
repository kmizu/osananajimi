"""
隣の恋文 (Osananajimi Novel) - 京都中京区を舞台にした学園ラブコメ小説

MkDocsベースの小説プロジェクト管理ツール
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__author__ = "Claude Code"
__email__ = "noreply@anthropic.com"
__description__ = "隣の恋文 - 京都中京区を舞台にした学園ラブコメ小説"

# パッケージレベルの設定
NOVEL_TITLE = "隣の恋文"
NOVEL_SUBTITLE = "京都中京区を舞台にした学園ラブコメ"
AUTHOR_NAME = "久野真一"  # 文体参考作者
SETTING_LOCATION = "京都市中京区"
PROTAGONIST = "藤原拓海"
HEROINE = "桜井美月"

# プロジェクト設定
PROJECT_NAME = "osananajimi-novel"
DOCS_DIR = "docs"
BUILD_DIR = "site"
MKDOCS_CONFIG = "mkdocs.yml"

__all__ = [
    "__version__",
    "__author__",
    "__email__", 
    "__description__",
    "NOVEL_TITLE",
    "NOVEL_SUBTITLE", 
    "AUTHOR_NAME",
    "SETTING_LOCATION",
    "PROTAGONIST",
    "HEROINE",
    "PROJECT_NAME",
    "DOCS_DIR",
    "BUILD_DIR", 
    "MKDOCS_CONFIG",
]