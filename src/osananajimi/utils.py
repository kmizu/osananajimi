"""
小説プロジェクト用ユーティリティ関数
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChapterInfo:
    """章情報"""
    number: int
    title: str
    file_path: Path
    char_count: int
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


@dataclass
class NovelStats:
    """小説統計情報"""
    total_chapters: int
    total_characters: int
    average_chars_per_chapter: int
    chapters: List[ChapterInfo]


def count_japanese_characters(text: str) -> int:
    """日本語文字数をカウント（改行・空白除く）"""
    # Markdownヘッダーを除去
    text = re.sub(r'^#.*$', '', text, flags=re.MULTILINE)
    
    # 改行・空白・記号を除去して日本語文字のみカウント
    japanese_chars = re.findall(r'[ぁ-んァ-ンー一-龯]', text)
    return len(japanese_chars)


def parse_chapter_title(content: str) -> Optional[str]:
    """Markdownコンテンツから章タイトルを抽出"""
    match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def analyze_chapter(file_path: Path) -> Optional[ChapterInfo]:
    """章ファイルを解析"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # 章番号をファイル名から抽出
        match = re.search(r'chapter(\d+)', file_path.stem)
        if not match:
            return None
        
        chapter_num = int(match.group(1))
        title = parse_chapter_title(content) or f"第{chapter_num}話"
        char_count = count_japanese_characters(content)
        
        # ファイル時刻情報
        stat = file_path.stat()
        created_at = datetime.fromtimestamp(stat.st_ctime)
        modified_at = datetime.fromtimestamp(stat.st_mtime)
        
        return ChapterInfo(
            number=chapter_num,
            title=title,
            file_path=file_path,
            char_count=char_count,
            created_at=created_at,
            modified_at=modified_at
        )
    except Exception:
        return None


def analyze_novel_project(project_root: Path) -> NovelStats:
    """小説プロジェクト全体を解析"""
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        return NovelStats(0, 0, 0, [])
    
    chapters = []
    
    # 全ての章ファイルを検索
    for md_file in docs_dir.rglob("chapter*.md"):
        chapter_info = analyze_chapter(md_file)
        if chapter_info:
            chapters.append(chapter_info)
    
    # 章番号でソート
    chapters.sort(key=lambda x: x.number)
    
    # 統計計算
    total_chapters = len(chapters)
    total_characters = sum(ch.char_count for ch in chapters)
    avg_chars = total_characters // total_chapters if total_chapters > 0 else 0
    
    return NovelStats(
        total_chapters=total_chapters,
        total_characters=total_characters,
        average_chars_per_chapter=avg_chars,
        chapters=chapters
    )


def generate_progress_report(stats: NovelStats) -> str:
    """進捗レポートを生成"""
    report = []
    report.append("📊 小説プロジェクト統計")
    report.append("=" * 30)
    report.append(f"総章数: {stats.total_chapters}話")
    report.append(f"総文字数: {stats.total_characters:,}文字")
    report.append(f"平均文字数: {stats.average_chars_per_chapter:,}文字/話")
    report.append("")
    
    if stats.chapters:
        report.append("📝 章別詳細:")
        for chapter in stats.chapters:
            report.append(
                f"  第{chapter.number:2d}話: {chapter.title:<20} "
                f"({chapter.char_count:4,}文字)"
            )
    
    return "\n".join(report)


def validate_chapter_structure(project_root: Path) -> List[str]:
    """章構成の妥当性をチェック"""
    issues = []
    stats = analyze_novel_project(project_root)
    
    if not stats.chapters:
        issues.append("❌ 章ファイルが見つかりません")
        return issues
    
    # 連番チェック
    numbers = [ch.number for ch in stats.chapters]
    expected = list(range(1, max(numbers) + 1))
    missing = set(expected) - set(numbers)
    
    if missing:
        issues.append(f"❌ 欠番の章があります: {sorted(missing)}")
    
    # 文字数チェック
    for chapter in stats.chapters:
        if chapter.char_count < 2000:
            issues.append(f"⚠️  第{chapter.number}話の文字数が少ない: {chapter.char_count}文字")
        elif chapter.char_count > 4000:
            issues.append(f"⚠️  第{chapter.number}話の文字数が多い: {chapter.char_count}文字")
    
    if not issues:
        issues.append("✅ 章構成に問題はありません")
    
    return issues


def export_for_kakuyomu(project_root: Path, output_path: Path) -> bool:
    """カクヨム投稿用フォーマットでエクスポート"""
    try:
        stats = analyze_novel_project(project_root)
        
        if not stats.chapters:
            return False
        
        # 全章を結合
        content_parts = []
        content_parts.append("隣の恋文")
        content_parts.append("=" * 20)
        content_parts.append("")
        
        for chapter in stats.chapters:
            chapter_content = chapter.file_path.read_text(encoding='utf-8')
            
            # Markdownヘッダーを除去
            chapter_content = re.sub(r'^#.*$', '', chapter_content, flags=re.MULTILINE)
            chapter_content = chapter_content.strip()
            
            content_parts.append(f"第{chapter.number}話　{chapter.title}")
            content_parts.append("")
            content_parts.append(chapter_content)
            content_parts.append("")
            content_parts.append("-" * 40)
            content_parts.append("")
        
        # 統計情報を追加
        content_parts.append("")
        content_parts.append(generate_progress_report(stats))
        
        # ファイル出力
        output_content = "\n".join(content_parts)
        output_path.write_text(output_content, encoding='utf-8')
        
        return True
    except Exception:
        return False