---
paths: "**/test_*.py"
---

# テスト規約（pytest）

このプロジェクトではpytestを使用してテストを実施します。

## テストディレクトリ構成

```
project/
└── app/
    ├── models/
    │   └── user.py
    └── services/
    │   └── auth.py
    └── tests/
        ├── models/
        │   └── test_user.py
        └── services/
            └── test_auth.py
```

テストディレクトリはappディレクトリ配下に配置します
テストディレクトリは本番コードの構造を反映させます

## テストファイルの命名

### ファイル名
- `test_<module_name>.py`
- テスト対象モジュールと同じ名前に`test_`プレフィックスを付ける

### テスト関数名
- `test_`プレフィックスで始める
- 何をテストしているか明確にする

```python
def test_calculate_total_returns_correct_value():
    """正しい合計金額が返されることを確認"""
    # テスト実装
```

## テストの構造

### Arrange-Act-Assert パターン
```python
def test_user_creation():
    # Arrange: テストデータを準備
    name = "山田太郎"
    email = "yamada@example.com"

    # Act: テスト対象の処理を実行
    user = create_user(name, email)

    # Assert: 期待する結果を検証
    assert user.name == name
    assert user.email == email
    assert user.created_at is not None
```

## テストの実行

### 全テスト実行
```bash
uv run pytest
```

### 特定ファイルのみ実行
```bash
uv run pytest tests/test_user.py
```

### カバレッジ付き実行
```bash
uv run pytest --cov=app --cov-report=html
```

### 詳細出力（失敗時の詳細表示）
```bash
uv run pytest -v
```

## フィクスチャの使用

### 基本的なフィクスチャ
```python
import pytest

@pytest.fixture
def sample_user():
    """テスト用のユーザーデータを提供"""
    return {
        "name": "テストユーザー",
        "email": "test@example.com",
        "age": 25
    }

def test_user_validation(sample_user):
    """ユーザーバリデーションのテスト"""
    assert validate_user(sample_user) is True
```

### フィクスチャのスコープ
```python
@pytest.fixture(scope="module")
def database_connection():
    """モジュール全体で共有するDB接続"""
    conn = create_connection()
    yield conn
    conn.close()
```

## パラメータ化テスト

同じテストロジックを複数のデータで実行する場合：

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (0, False),
    (1, True),
    (2, True),
    (-1, False),
])
def test_is_positive(input_value, expected):
    """正の数判定のテスト"""
    assert is_positive(input_value) == expected
```

## 例外テスト

```python
import pytest

def test_invalid_email_raises_error():
    """無効なメールアドレスでエラーが発生することを確認"""
    with pytest.raises(ValidationError) as exc_info:
        validate_email("invalid-email")

    assert "無効なメールアドレス" in str(exc_info.value)
```

## モック・パッチ

外部依存をモックする場合：

```python
from unittest.mock import Mock, patch

def test_api_call_with_mock():
    """API呼び出しのモックテスト"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        result = fetch_data_from_api()

        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

## テストマーカー

### slowテスト（実行時間が長いテスト）
```python
@pytest.mark.slow
def test_heavy_computation():
    """時間のかかる処理のテスト"""
    # 実装
```

実行時にskipする：
```bash
uv run pytest -m "not slow"
```

### 統合テスト
```python
@pytest.mark.integration
def test_full_workflow():
    """エンドツーエンドのワークフローテスト"""
    # 実装
```

## ベストプラクティス

### テストの独立性
- 各テストは他のテストに依存しないこと
- テストの実行順序に依存しないこと

### テストデータ
- ハードコードされた本番データを使わない
- テスト用のダミーデータを明示的に作成

### アサーション
- 1つのテストで1つの概念を検証
- アサーションメッセージを適切に設定

```python
def test_user_age():
    user = create_user("太郎", 20)
    assert user.age >= 18, "ユーザーは18歳以上である必要があります"
```

### テストの可読性
- テスト名で何をテストしているか明確にする
- docstringで期待する動作を記述
- 複雑なテストには適切なコメントを付ける

## カバレッジ目標

- 全体カバレッジ: 80%以上
- 重要なビジネスロジック: 100%
- ユーティリティ関数: 90%以上

