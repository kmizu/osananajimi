"""
ユーティリティ関数のテスト
"""

import pytest
from pathlib import Path
from osananajimi.utils import (
    count_japanese_characters,
    parse_chapter_title,
    analyze_chapter,
    validate_chapter_structure,
)


def test_count_japanese_characters():
    """日本語文字数カウントのテスト"""
    # 基本的な日本語文字
    assert count_japanese_characters("こんにちは") == 5
    assert count_japanese_characters("美月") == 2
    assert count_japanese_characters("拓海先輩") == 4
    
    # 英数字・記号は除外
    assert count_japanese_characters("Hello, 世界!") == 2
    assert count_japanese_characters("123あいう456") == 3
    
    # 空文字・空白
    assert count_japanese_characters("") == 0
    assert count_japanese_characters("   ") == 0
    
    # Markdownヘッダーを含む
    text_with_header = """# 第1話　新しい季節

　春の朝、僕は美月と出会った。"""
    assert count_japanese_characters(text_with_header) == 15  # ヘッダー除く


def test_parse_chapter_title():
    """章タイトル抽出のテスト"""
    # 正常なMarkdownヘッダー
    content1 = "# 第1話　新しい季節\n\n本文..."
    assert parse_chapter_title(content1) == "第1話　新しい季節"
    
    # 複数ヘッダーがある場合（最初を取得）
    content2 = """# 第1話　新しい季節

## サブタイトル

本文..."""
    assert parse_chapter_title(content2) == "第1話　新しい季節"
    
    # ヘッダーがない場合
    content3 = "本文のみ..."
    assert parse_chapter_title(content3) is None


def test_chapter_analysis(tmp_path):
    """章解析のテスト"""
    # テスト用章ファイルを作成
    chapter_file = tmp_path / "chapter01.md"
    chapter_content = """# 第1話　新しい季節

　春の朝、僕は美月と出会った。
　桜の花びらが舞い踊る中で。"""
    
    chapter_file.write_text(chapter_content, encoding='utf-8')
    
    # 解析実行
    result = analyze_chapter(chapter_file)
    
    assert result is not None
    assert result.number == 1
    assert result.title == "第1話　新しい季節"
    assert result.char_count > 0
    assert result.file_path == chapter_file


def test_chapter_analysis_invalid_file(tmp_path):
    """無効な章ファイルのテスト"""
    # 章番号がないファイル
    invalid_file = tmp_path / "invalid.md"
    invalid_file.write_text("テスト内容", encoding='utf-8')
    
    result = analyze_chapter(invalid_file)
    assert result is None


def test_validation_empty_project(tmp_path):
    """空プロジェクトの検証テスト"""
    # docsディレクトリがない場合
    issues = validate_chapter_structure(tmp_path)
    assert "❌ 章ファイルが見つかりません" in issues


def test_validation_complete_project(tmp_path):
    """完全なプロジェクトの検証テスト"""
    docs_dir = tmp_path / "docs" / "volume1"
    docs_dir.mkdir(parents=True)
    
    # 正常な章ファイルを作成
    for i in range(1, 4):
        chapter_file = docs_dir / f"chapter{i:02d}.md"
        content = f"""# 第{i}話　テストタイトル

{'　' * 200}テスト内容{'。' * 100}"""  # 約3000文字
        chapter_file.write_text(content, encoding='utf-8')
    
    issues = validate_chapter_structure(tmp_path)
    assert "✅ 章構成に問題はありません" in issues


def test_validation_missing_chapters(tmp_path):
    """欠番章があるプロジェクトの検証テスト"""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(parents=True)
    
    # 章1と章3のみ作成（章2が欠番）
    for i in [1, 3]:
        chapter_file = docs_dir / f"chapter{i:02d}.md"
        content = f"""# 第{i}話　テストタイトル

{'　' * 200}テスト内容{'。' * 100}"""
        chapter_file.write_text(content, encoding='utf-8')
    
    issues = validate_chapter_structure(tmp_path)
    assert any("❌ 欠番の章があります" in issue for issue in issues)


if __name__ == "__main__":
    pytest.main([__file__])