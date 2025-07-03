# 隣の恋文 (Osananajimi Novel)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![MkDocs](https://img.shields.io/badge/mkdocs-material-green.svg)](https://squidfunk.github.io/mkdocs-material/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

京都市中京区を舞台にした学園ラブコメ小説プロジェクト

## 📖 作品概要

**隣の恋文**は、久野真一の文体を模倣した王道ラブコメ小説です。

- **舞台**: 京都市中京区
- **主人公**: 藤原拓海（高校2年生、プログラミング好き）
- **ヒロイン**: 桜井美月（高校1年生、幼馴染）
- **ジャンル**: 学園ラブコメ
- **構成**: 第1巻30話完結（約9万文字）

## 🎯 ストーリー

隣同士に住む幼馴染の拓海と美月が、高校生活を通じて恋人へと成長していく物語。プログラミングコンテストや文化祭、京都の美しい街並みを背景に、二人の関係が深まっていきます。

## 🚀 クイックスタート

### 1. インストール

```bash
# リポジトリをクローン
git clone https://github.com/mizushima/osananajimi.git
cd osananajimi

# 依存関係をインストール
pip install -e .

# または開発環境セットアップ
pip install -e ".[dev]"
```

### 2. サイトプレビュー

```bash
# 開発サーバー起動
osananajimi-serve

# または
mkdocs serve
```

ブラウザで http://localhost:8000 にアクセスして小説サイトをプレビューできます。

### 3. サイトビルド

```bash
# 静的サイト生成
osananajimi-build

# または
mkdocs build
```

## 📁 プロジェクト構成

```
osananajimi/
├── docs/                   # 小説コンテンツ
│   ├── index.md            # トップページ
│   └── volume1/            # 第1巻
│       ├── chapter01.md    # 第1話
│       ├── chapter02.md    # 第2話
│       └── ...             # 第30話まで
├── src/osananajimi/        # Pythonパッケージ
│   ├── __init__.py         # パッケージ初期化
│   ├── cli.py              # CLIコマンド
│   └── utils.py            # ユーティリティ
├── tests/                  # テストコード
├── mkdocs.yml              # MkDocs設定
├── pyproject.toml          # Python設定
└── requirements.txt        # 依存関係
```

## 🛠️ CLIコマンド

プロジェクトには専用のCLIツールが付属しています：

```bash
# プロジェクト状態確認
osananajimi-serve status

# 開発サーバー起動
osananajimi-serve --host 0.0.0.0 --port 8080

# サイトビルド
osananajimi-build --clean

# GitHub Pagesデプロイ
osananajimi-deploy
```

## 📊 進捗状況

- ✅ **第1巻完結** (30話)
- ✅ **総文字数**: 約90,000文字
- ✅ **MkDocsサイト**: 構築済み
- ✅ **Pythonパッケージ**: 機能完備

### 章構成

| 章 | 話数 | テーマ | 状況 |
|---|-----|-------|------|
| 第1章 | 1-5話 | 春の始まり | ✅ 完成 |
| 第2章 | 6-10話 | 日常の中で | ✅ 完成 |
| 第3章 | 11-15話 | 気づき始める想い | ✅ 完成 |
| 第4章 | 16-20話 | 文化祭 | ✅ 完成 |
| 第5章 | 21-25話 | 夏の終わり | ✅ 完成 |
| 第6章 | 26-30話 | 心を繋ぐ | ✅ 完成 |

## 🎨 特徴

### 文体・スタイル
- 一人称（拓海視点）での心理描写重視
- 久野真一作品の文体を忠実に再現
- 温かみのある日常描写

### 技術スタック
- **MkDocs**: 静的サイト生成
- **Material Design**: モダンなテーマ
- **Python**: CLIツールとユーティリティ
- **GitHub Pages**: デプロイ対応

### 地域設定
- 京都市中京区の実在地域
- 錦市場、新京極、鴨川などの名所
- 桜月堂（和菓子店）などの詳細設定

## 📚 技術仕様

### 文字数設定
- **1話**: 約3,000文字
- **1巻**: 約90,000文字（30話）
- **カクヨム投稿**: 対応可能

### 品質保証
- 自動テスト完備
- 文字数チェック機能
- 章構成検証機能

## 🔧 開発

### テスト実行

```bash
# 全テスト実行
pytest

# カバレッジ付き
pytest --cov=src/osananajimi

# 特定テスト
pytest tests/test_utils.py
```

### コード品質

```bash
# フォーマット
black src/ tests/

# インポートソート
isort src/ tests/

# 型チェック
mypy src/osananajimi

# リント
flake8 src/ tests/
```

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 🤝 貢献

プルリクエストやイシューは大歓迎です！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📞 サポート

- Issues: [GitHub Issues](https://github.com/mizushima/osananajimi/issues)
- Documentation: [プロジェクトサイト](https://mizushima.github.io/osananajimi/)

---

**隣の恋文** - 京都の街角で紡がれる、幼馴染の恋物語 💕