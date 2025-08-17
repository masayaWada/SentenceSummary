# 日本語テキスト要約システム (Japanese Text Summarization System)

## 概要

このシステムは、日本語テキストの自動要約を行うPythonプログラムです。`pysummarization`ライブラリとMeCab（日本語形態素解析器）を使用して、長い日本語テキストから重要な文を抽出し、理解しやすい要約を生成します。

## 主な機能

### 🖥️ **GUIアプリケーション**
- **直感的な操作**: ドラッグ&ドロップでファイル選択
- **リアルタイム表示**: 要約結果を即座に確認
- **パラメータ調整**: スライダーやドロップダウンで簡単設定
- **テキスト編集**: 入力テキストを直接編集可能

### 🎯 **粒度調整機能**
- **FINE（詳細）**: 多くの文を含む詳細な要約（要約率: 約40%）
- **MEDIUM（中程度）**: バランスの取れた要約（要約率: 約25%）
- **COARSE（粗い）**: 要点のみの簡潔な要約（要約率: 約15%）

### 🔍 **高度な要約アルゴリズム**
- **TF-IDFコサイン類似度**による類似文の除去
- **重要度ランキング**による上位文の抽出
- **文の順序保持**で元文書の流れを維持
- **接続詞の自動追加**で読みやすさを向上

### 📊 **詳細な統計情報**
- 要約率、文数、類似性閾値などの詳細情報
- 目標文数と実際の文数の比較
- 元文書の文数と要約文数の比率

## インストール方法

### 1. 必要なライブラリのインストール

```bash
# pysummarizationライブラリのインストール
pip install pysummarization

# MeCab本体のインストール（macOS）
brew install mecab
brew install mecab-ipadic

# Pythonバインディングのインストール
pip install mecab-python3
```

### 2. MeCabの設定

```bash
# MeCab辞書のパスを設定
echo "dicdir = /usr/local/lib/mecab/dic/ipadic" >> /usr/local/etc/mecabrc
```

### 3. 動作確認

```bash
# MeCabが正常にインポートできるかテスト
python -c "import MeCab; print('MeCab imported successfully')"

# MeCabTokenizerが正常にインポートできるかテスト
python -c "from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer; print('MeCabTokenizer imported successfully')"
```

## 使用方法

### 1. GUIアプリケーション（推奨）

最も使いやすい方法です。グラフィカルなインターフェースで直感的に操作できます。

```bash
# GUIアプリケーションを起動
python gui_app.py
```

**GUIの主な機能:**
- 📁 **ファイル選択**: ドラッグ&ドロップでファイルを選択
- ⚙️ **パラメータ調整**: スライダーやドロップダウンで簡単設定
- 📝 **テキスト編集**: 入力テキストを直接編集可能
- 📊 **リアルタイム表示**: 要約結果を即座に表示
- 💾 **自動保存**: 実行時間を含むファイル名で自動保存

### 2. コマンドライン

高度なユーザーや自動化に適しています。

```bash
# デフォルト設定で要約実行
python main.py

# カスタムファイルパスで実行
python main.py --input "入力ファイル.txt" --output "出力ファイル.txt"

# 粒度レベルを指定して実行
python main.py --granularity fine
python main.py --granularity medium
python main.py --granularity coarse
```

### コマンドラインオプション

| オプション           | 短縮形 | デフォルト値              | 説明                                   |
| -------------------- | ------ | ------------------------- | -------------------------------------- |
| `--input`            | `-i`   | `./test/インプット.txt`   | 入力ファイルのパス                     |
| `--output`           | `-o`   | `./test/アウトプット.txt` | 出力ファイルのパス                     |
| `--granularity`      | `-g`   | `medium`                  | 要約の粒度レベル（fine/medium/coarse） |
| `--similarity_limit` | `-s`   | `0.3`                     | 類似性フィルターの閾値（0.1-0.5）      |
| `--min_sentences`    | -      | `3`                       | 最小文数                               |
| `--max_sentences`    | -      | `20`                      | 最大文数                               |

### 使用例

```bash
# 詳細な要約を生成
python main.py --granularity fine --input "長文.txt" --output "要約_詳細.txt"

# 粗い要約を生成（類似性フィルターを厳しく）
python main.py --granularity coarse --similarity_limit 0.2 --input "長文.txt" --output "要約_要点.txt"

# カスタム文数範囲で要約
python main.py --min_sentences 5 --max_sentences 15 --input "長文.txt" --output "要約_カスタム.txt"
```

## 出力形式

### 要約結果の例

```
=== 要約結果 ===
粒度レベル: medium
目標文数: 6
実際の文数: 4
類似性閾値: 0.3

【要約】
人工知能（AI）技術の進歩について詳しく説明いたします。
また、近年、人工知能技術は目覚ましい発展を遂げており、様々な分野で革新的な応用が進んでいます。
また、特に、Transformerアーキテクチャを基盤とした大規模言語モデルは、人間の言語理解能力に迫る性能を示しており、翻訳、要約、文章生成などのタスクで高い品質を実現しています。
また、医療分野でのAI活用も注目されており、画像診断支援システムや薬物発見支援、個別化医療の実現など、様々な応用が研究・開発されています。

【元文書の文数】: 26
【要約率】: 15.4%
```

## 技術仕様

### 使用ライブラリ
- **pysummarization**: 要約アルゴリズムの実装
- **MeCab**: 日本語形態素解析
- **tkinter**: GUIアプリケーション（Python標準ライブラリ）
- **argparse**: コマンドライン引数の処理
- **os**: ファイル操作
- **datetime**: 日時処理

### アルゴリズム
1. **前処理**: テキストの読み込みと結合
2. **トークン化**: MeCabによる日本語形態素解析
3. **類似性フィルタリング**: TF-IDFコサイン類似度による重複除去
4. **要約生成**: 重要度ランキングによる文の選択
5. **後処理**: 文の順序調整と接続詞の追加

### パフォーマンス
- **処理速度**: 中程度の長さのテキスト（1000-5000文字）で数秒
- **メモリ使用量**: 最小限（テキストサイズに比例）
- **精度**: 類似性フィルターの調整により制御可能

## トラブルシューティング

### よくある問題

#### 1. MeCabのインポートエラー
```
ModuleNotFoundError: No module named 'MeCab'
```

**解決方法:**
```bash
# MeCab本体とPythonバインディングをインストール
brew install mecab mecab-ipadic
pip install mecab-python3
```

#### 2. 辞書が見つからないエラー
```
mecab: no such file or directory: /usr/local/lib/mecab/dic/ipadic
```

**解決方法:**
```bash
# MeCab辞書のパスを設定
echo "dicdir = /usr/local/lib/mecab/dic/ipadic" >> /usr/local/etc/mecabrc
```

#### 3. 要約結果が空になる
- 入力ファイルの文字エンコーディングがUTF-8であることを確認
- 類似性フィルターの閾値を調整（`--similarity_limit`）
- 最小文数を調整（`--min_sentences`）

### デバッグ方法

```bash
# 構文チェック
python -m py_compile sammary.py

# 詳細なエラー情報
python sammary.py --input "存在しないファイル.txt"
```

## カスタマイズ

### 新しい区切り文字の追加

```python
# sammary.py の該当箇所を編集
self.auto_abstractor.delimiter_list = ["。", "\n", "！", "？"]
```

### 接続詞のカスタマイズ

```python
# post_process_summary メソッド内で編集
if "しかし" in sent or "だが" in sent or "一方" in sent:
    improved_summary.append(sent)
else:
    improved_summary.append(f"また、{sent}")
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグ報告、機能要望、プルリクエストを歓迎します。以下の手順で貢献してください：

1. このリポジトリをフォーク
2. 新しいブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 更新履歴

- **v1.1.0**: GUIアプリケーション追加
  - グラフィカルなユーザーインターフェース
  - 直感的なパラメータ調整
  - リアルタイム要約結果表示
  - ファイル名自動生成機能

- **v1.0.0**: 初期リリース
  - 基本的な要約機能
  - 粒度調整機能
  - 類似性フィルタリング
  - 後処理機能

## サポート

問題が発生した場合や質問がある場合は、以下の方法でサポートを受けることができます：

1. GitHubのIssuesページで問題を報告
2. 詳細なエラーメッセージと環境情報を提供
3. 再現可能な手順を記載

---

**注意**: このシステムは研究・開発目的で作成されています。本格的な商用利用の前に、十分なテストと検証を行ってください。
