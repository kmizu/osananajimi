# Makefile for Osananajimi Novel Project

.PHONY: help install dev clean test build serve deploy status
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
MKDOCS := mkdocs

# Help target
help: ## Show this help message
	@echo "隣の恋文 - Makefile コマンド"
	@echo "================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Installation targets
install: ## Install the package in production mode
	$(PIP) install .

dev: ## Install the package in development mode with dev dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

install-deps: ## Install only dependencies
	$(PIP) install -r requirements.txt

# Development targets
clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf site/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

test: ## Run tests
	$(PYTEST) tests/ -v

test-cov: ## Run tests with coverage
	$(PYTEST) tests/ --cov=src/osananajimi --cov-report=html --cov-report=term

lint: ## Run code quality checks
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/
	mypy src/osananajimi

format: ## Format code
	black src/ tests/
	isort src/ tests/

# MkDocs targets
serve: ## Start development server
	$(MKDOCS) serve --host 0.0.0.0 --port 8000

build: ## Build static site
	$(MKDOCS) build --clean

deploy: ## Deploy to GitHub Pages
	$(MKDOCS) gh-deploy --force

# Novel project targets
status: ## Show project status
	@echo "📊 プロジェクト状態"
	@echo "=================="
	@echo "📁 プロジェクトルート: $(shell pwd)"
	@echo "📝 Markdownファイル数: $(shell find docs -name "*.md" | wc -l)"
	@echo "📊 総文字数: $(shell find docs -name "*.md" -exec cat {} \; | wc -c)文字"
	@echo "🔨 ビルド状況: $(shell [ -d site ] && echo "✅ 完了" || echo "⏳ 未実行")"
	@echo "🔄 Git状況: $(shell git status --porcelain | wc -l)個の変更"

validate: ## Validate novel structure
	$(PYTHON) -c "from src.osananajimi.utils import validate_chapter_structure; from pathlib import Path; print('\n'.join(validate_chapter_structure(Path.cwd())))"

stats: ## Show novel statistics
	$(PYTHON) -c "from src.osananajimi.utils import analyze_novel_project, generate_progress_report; from pathlib import Path; print(generate_progress_report(analyze_novel_project(Path.cwd())))"

export-kakuyomu: ## Export for Kakuyomu submission
	$(PYTHON) -c "from src.osananajimi.utils import export_for_kakuyomu; from pathlib import Path; export_for_kakuyomu(Path.cwd(), Path('隣の恋文_カクヨム版.txt')); print('✅ カクヨム版エクスポート完了: 隣の恋文_カクヨム版.txt')"

# Package targets
wheel: clean ## Build wheel package
	$(PYTHON) -m build

upload-test: wheel ## Upload to Test PyPI
	twine upload --repository testpypi dist/*

upload: wheel ## Upload to PyPI
	twine upload dist/*

# Documentation targets
docs-serve: ## Serve documentation locally
	$(MAKE) serve

docs-build: ## Build documentation
	$(MAKE) build

docs-deploy: ## Deploy documentation to GitHub Pages
	$(MAKE) deploy

# Git helpers
git-status: ## Show git status with novel file info
	@echo "🔄 Git状況"
	@echo "=========="
	@git status --short
	@echo ""
	@echo "📝 追跡中のMarkdownファイル:"
	@git ls-files "*.md" | head -10

commit-novel: ## Commit novel changes with auto-generated message
	@echo "📝 小説の変更をコミット中..."
	@git add docs/ mkdocs.yml CLAUDE.md
	@git commit -m "📝 小説更新: $(shell date '+%Y-%m-%d %H:%M')\n\n🤖 Generated with Claude Code\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
	@echo "✅ コミット完了"

# CI/CD helpers
ci-test: ## Run CI tests
	$(PYTEST) tests/ --cov=src/osananajimi --cov-report=xml

ci-build: ## CI build check
	$(PYTHON) -m build --wheel
	$(MKDOCS) build

# Quick commands
quick-serve: install-deps serve ## Quick start: install deps and serve

quick-deploy: test build deploy ## Quick deploy: test, build and deploy

# Project info
info: ## Show project information
	@echo "隣の恋文 (Osananajimi Novel)"
	@echo "============================"
	@echo "📖 ジャンル: 学園ラブコメ"
	@echo "🏫 舞台: 京都市中京区"
	@echo "👨‍🎓 主人公: 藤原拓海"
	@echo "👩‍🎓 ヒロイン: 桜井美月"
	@echo "📚 構成: 第1巻30話完結"
	@echo "💻 技術: MkDocs + Python + Material Design"
	@echo ""
	@echo "🚀 クイックスタート:"
	@echo "  make dev      # 開発環境セットアップ"
	@echo "  make serve    # 開発サーバー起動"
	@echo "  make status   # プロジェクト状態確認"