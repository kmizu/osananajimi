"""
小説プロジェクト用CLIツール

MkDocsサイトのビルド、サーブ、デプロイ機能を提供
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

import click
from mkdocs.commands.build import build as mkdocs_build
from mkdocs.commands.serve import serve as mkdocs_serve
from mkdocs.config import load_config


def get_project_root() -> Path:
    """プロジェクトルートディレクトリを取得"""
    current = Path.cwd()
    
    # mkdocs.ymlを探して遡る
    while current != current.parent:
        if (current / "mkdocs.yml").exists():
            return current
        current = current.parent
    
    # 見つからない場合は現在のディレクトリ
    return Path.cwd()


@click.group()
@click.version_option()
def cli():
    """隣の恋文 - 小説プロジェクト管理CLI"""
    pass


@cli.command()
@click.option("--host", "-h", default="127.0.0.1", help="サーバーホスト")
@click.option("--port", "-p", default=8000, help="サーバーポート")
@click.option("--open-browser/--no-open-browser", default=True, help="ブラウザを自動で開く")
def serve(host: str, port: int, open_browser: bool):
    """開発サーバーを起動してサイトをプレビュー"""
    project_root = get_project_root()
    config_file = project_root / "mkdocs.yml"
    
    if not config_file.exists():
        click.echo(f"❌ mkdocs.yml が見つかりません: {config_file}", err=True)
        sys.exit(1)
    
    click.echo(f"🚀 開発サーバーを起動中...")
    click.echo(f"📁 プロジェクト: {project_root}")
    click.echo(f"🌐 URL: http://{host}:{port}")
    
    try:
        config = load_config(str(config_file))
        mkdocs_serve(
            config=config,
            host=host,
            port=port,
            open_browser=open_browser,
            livereload=True,
            watch_theme=True,
        )
    except KeyboardInterrupt:
        click.echo("\n👋 サーバーを停止しました")
    except Exception as e:
        click.echo(f"❌ エラーが発生しました: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--clean/--no-clean", default=False, help="ビルド前にsite/を削除")
@click.option("--verbose", "-v", is_flag=True, help="詳細ログを表示")
def build(clean: bool, verbose: bool):
    """静的サイトをビルド"""
    project_root = get_project_root()
    config_file = project_root / "mkdocs.yml"
    
    if not config_file.exists():
        click.echo(f"❌ mkdocs.yml が見つかりません: {config_file}", err=True)
        sys.exit(1)
    
    if clean:
        site_dir = project_root / "site"
        if site_dir.exists():
            click.echo(f"🧹 site/ ディレクトリを削除中...")
            import shutil
            shutil.rmtree(site_dir)
    
    click.echo(f"🔨 サイトをビルド中...")
    click.echo(f"📁 プロジェクト: {project_root}")
    
    try:
        config = load_config(str(config_file))
        mkdocs_build(config=config, dirty=not clean)
        click.echo(f"✅ ビルド完了: {project_root / 'site'}")
    except Exception as e:
        click.echo(f"❌ ビルドエラー: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--remote", default="origin", help="GitHubリモート名")
@click.option("--branch", default="gh-pages", help="デプロイ先ブランチ")
@click.option("--force/--no-force", default=False, help="強制プッシュ")
def deploy(remote: str, branch: str, force: bool):
    """GitHub Pagesにデプロイ"""
    project_root = get_project_root()
    
    click.echo(f"🚀 GitHub Pagesにデプロイ中...")
    click.echo(f"📁 プロジェクト: {project_root}")
    click.echo(f"🔗 リモート: {remote}")
    click.echo(f"🌿 ブランチ: {branch}")
    
    try:
        # まずビルド
        build.callback(clean=True, verbose=False)
        
        # mkdocs gh-deployを実行
        cmd = [
            "mkdocs", "gh-deploy",
            "--remote-name", remote,
            "--remote-branch", branch,
        ]
        if force:
            cmd.append("--force")
        
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)
        
        if result.returncode == 0:
            click.echo("✅ デプロイ完了!")
            click.echo(f"🌐 サイトURL: https://{get_github_username()}.github.io/{get_repo_name()}/")
        else:
            click.echo(f"❌ デプロイエラー: {result.stderr}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ デプロイエラー: {e}", err=True)
        sys.exit(1)


def get_github_username() -> str:
    """GitHubユーザー名を取得"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # https://github.com/user/repo.git -> user
            if "github.com" in url:
                parts = url.split("/")
                return parts[-2]
    except:
        pass
    return "user"


def get_repo_name() -> str:
    """リポジトリ名を取得"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # https://github.com/user/repo.git -> repo
            if "github.com" in url:
                parts = url.split("/")
                return parts[-1].replace(".git", "")
    except:
        pass
    return "osananajimi"


@cli.command()
def status():
    """プロジェクトの状態を表示"""
    project_root = get_project_root()
    
    click.echo("📊 プロジェクト状態")
    click.echo(f"📁 ルート: {project_root}")
    
    # ファイル数カウント
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        md_files = list(docs_dir.rglob("*.md"))
        click.echo(f"📝 Markdownファイル: {len(md_files)}個")
        
        # 文字数カウント（概算）
        total_chars = 0
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                total_chars += len(content)
            except:
                pass
        click.echo(f"📊 総文字数: 約{total_chars:,}文字")
    
    # Git状態
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=project_root
        )
        if result.returncode == 0:
            changes = result.stdout.strip().split("\n") if result.stdout.strip() else []
            click.echo(f"🔄 Git変更: {len(changes)}個のファイル")
    except:
        click.echo("🔄 Git: 利用不可")
    
    # ビルド状態
    site_dir = project_root / "site"
    if site_dir.exists():
        click.echo("✅ ビルド: 完了")
    else:
        click.echo("⏳ ビルド: 未実行")


if __name__ == "__main__":
    cli()