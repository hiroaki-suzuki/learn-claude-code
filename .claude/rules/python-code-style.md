---
paths: "**/*.py"
---

# Pythonコードスタイル規約

このプロジェクトではPython 3.14を使用し、Ruff（リンター/フォーマッター）とty（型チェッカー）でコード品質を維持します。

## 基本原則

### 命名規則
- **関数・変数**: `snake_case`
- **クラス**: `PascalCase`
- **定数**: `UPPER_SNAKE_CASE`
- **プライベート属性**: `_leading_underscore`

### 型ヒント
すべての関数・メソッドに型ヒントを付与してください。

```python
def calculate_total(items: list[int], tax_rate: float) -> float:
    """合計金額を計算する"""
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### インポート順序
1. 標準ライブラリ
2. サードパーティライブラリ
3. ローカルモジュール

各グループ間は空行で区切り、アルファベット順にソートしてください。

## Ruffとの連携

### 自動フォーマット
```bash
uv run ruff format app/
```

### リント実行
```bash
uv run ruff check app/
```

## tyとの連携

### 型チェック実行
```bash
uv run ty check app/
```

## コーディングガイドライン

### 関数の長さ
- 1つの関数は50行以内を推奨
- 複雑な処理は小さな関数に分割

### docstring
パブリックな関数・クラスには必ずdocstringを記述してください。

```python
def process_data(data: dict[str, any]) -> list[str]:
    """
    データを処理して文字列リストを返す

    Args:
        data: 処理対象のデータ辞書

    Returns:
        処理済みの文字列リスト
    """
    # 実装
```

### エラーハンドリング
- 具体的な例外クラスを使用（`Exception`の直接使用は避ける）
- 例外メッセージは日本語でわかりやすく記述

```python
class ValidationError(ValueError):
    """バリデーションエラー"""
    pass

def validate_email(email: str) -> None:
    if "@" not in email:
        raise ValidationError(f"無効なメールアドレス: {email}")
```

## 禁止事項

- `from module import *`の使用
- グローバル変数の乱用
- 過度にネストした条件分岐（3階層以上）
- マジックナンバー（定数化すべき数値の直接記述）

## コード例

### 良い例
```python
from pathlib import Path

MAX_RETRIES: int = 3
DEFAULT_TIMEOUT: float = 30.0

def read_config_file(file_path: Path) -> dict[str, any]:
    """設定ファイルを読み込む"""
    if not file_path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
```

### 悪い例
```python
def readFile(filePath):  # PascalCase/camelCaseは使わない、型ヒントなし
    f = open(filePath)   # withステートメントを使うべき
    data = f.read()
    f.close()
    return data
```
