"""
CLIコマンドのテスト
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from osananajimi.cli import cli, get_project_root


def test_cli_version():
    """バージョン表示のテスト"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0


def test_get_project_root():
    """プロジェクトルート検出のテスト"""
    # 現在のディレクトリがプロジェクトルートとして検出される
    root = get_project_root()
    assert isinstance(root, Path)
    assert root.exists()


def test_status_command(tmp_path, monkeypatch):
    """ステータスコマンドのテスト"""
    # テスト用プロジェクトを作成
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    
    # mkdocs.ymlを作成
    mkdocs_file = tmp_path / "mkdocs.yml"
    mkdocs_file.write_text("site_name: Test")
    
    # テスト用章ファイルを作成
    chapter_file = docs_dir / "chapter01.md"
    chapter_file.write_text("# 第1話　テスト\n\nテスト内容です。")
    
    # 作業ディレクトリを変更
    monkeypatch.chdir(tmp_path)
    
    runner = CliRunner()
    result = runner.invoke(cli, ['status'])
    
    assert result.exit_code == 0
    assert "📊 プロジェクト状態" in result.output
    assert "📝 Markdownファイル:" in result.output


def test_build_command_no_config():
    """設定ファイルがない場合のビルドテスト"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['build'])
        assert result.exit_code == 1
        assert "❌ mkdocs.yml が見つかりません" in result.output


def test_serve_command_no_config():
    """設定ファイルがない場合のサーブテスト"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['serve', '--help'])
        assert result.exit_code == 0
        assert "開発サーバーを起動してサイトをプレビュー" in result.output


if __name__ == "__main__":
    pytest.main([__file__])