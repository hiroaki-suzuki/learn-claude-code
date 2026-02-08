"""テキスト処理ユーティリティのテスト"""

import pytest

from app.utils.text import remove_all_spaces, remove_fullwidth_spaces


class TestRemoveAllSpaces:
    """remove_all_spaces関数のテスト"""

    def test_remove_halfwidth_spaces_only(self) -> None:
        """半角スペースのみを含む文字列から全スペースを除去"""
        # Arrange: テストデータを準備
        text = "hello world"

        # Act: テスト対象の処理を実行
        result = remove_all_spaces(text)

        # Assert: 期待する結果を検証
        assert result == "helloworld"

    def test_remove_fullwidth_spaces_only(self) -> None:
        """全角スペースのみを含む文字列から全スペースを除去"""
        # Arrange
        text = "こんにちは　世界"

        # Act
        result = remove_all_spaces(text)

        # Assert
        assert result == "こんにちは世界"

    def test_remove_mixed_spaces(self) -> None:
        """半角・全角スペースが混在する文字列から全スペースを除去"""
        # Arrange
        text = "  mixed　spaces  here  "

        # Act
        result = remove_all_spaces(text)

        # Assert
        assert result == "mixedspaceshere"

    def test_no_spaces(self) -> None:
        """スペースを含まない文字列はそのまま返される"""
        # Arrange
        text = "NoSpacesHere"

        # Act
        result = remove_all_spaces(text)

        # Assert
        assert result == "NoSpacesHere"

    def test_empty_string(self) -> None:
        """空文字列は空文字列のまま返される"""
        # Arrange
        text = ""

        # Act
        result = remove_all_spaces(text)

        # Assert
        assert result == ""

    def test_only_spaces(self) -> None:
        """スペースのみの文字列は空文字列になる"""
        # Arrange
        text = "   　　 　 "

        # Act
        result = remove_all_spaces(text)

        # Assert
        assert result == ""

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello world", "helloworld"),
            ("こんにちは　世界", "こんにちは世界"),
            ("  mixed　spaces  here  ", "mixedspaceshere"),
            ("NoSpaces", "NoSpaces"),
            ("", ""),
            ("   　　 　 ", ""),
            ("　", ""),
            (" ", ""),
        ],
    )
    def test_remove_all_spaces_parametrized(
        self, input_text: str, expected: str
    ) -> None:
        """パラメータ化テスト：様々な入力パターンで正しく動作する"""
        assert remove_all_spaces(input_text) == expected


class TestRemoveFullwidthSpaces:
    """remove_fullwidth_spaces関数のテスト"""

    def test_halfwidth_spaces_remain(self) -> None:
        """半角スペースはそのまま残る"""
        # Arrange
        text = "hello world"

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == "hello world"

    def test_remove_fullwidth_spaces_only(self) -> None:
        """全角スペースのみが除去される"""
        # Arrange
        text = "こんにちは　世界"

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == "こんにちは世界"

    def test_mixed_spaces_halfwidth_remain(self) -> None:
        """混在する場合、全角スペースのみ除去され半角スペースは残る"""
        # Arrange
        text = "mixed　spaces here"

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == "mixedspaces here"

    def test_no_spaces(self) -> None:
        """スペースを含まない文字列はそのまま返される"""
        # Arrange
        text = "NoSpacesHere"

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == "NoSpacesHere"

    def test_empty_string(self) -> None:
        """空文字列は空文字列のまま返される"""
        # Arrange
        text = ""

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == ""

    def test_only_fullwidth_spaces(self) -> None:
        """全角スペースのみの文字列は空文字列になる"""
        # Arrange
        text = "　　　"

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == ""

    def test_only_halfwidth_spaces(self) -> None:
        """半角スペースのみの文字列はそのまま返される"""
        # Arrange
        text = "   "

        # Act
        result = remove_fullwidth_spaces(text)

        # Assert
        assert result == "   "

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello world", "hello world"),
            ("こんにちは　世界", "こんにちは世界"),
            ("mixed　spaces here", "mixedspaces here"),
            ("NoSpaces", "NoSpaces"),
            ("", ""),
            ("　　　", ""),
            ("   ", "   "),
            ("　 　 ", "  "),
        ],
    )
    def test_remove_fullwidth_spaces_parametrized(
        self, input_text: str, expected: str
    ) -> None:
        """パラメータ化テスト：様々な入力パターンで正しく動作する"""
        assert remove_fullwidth_spaces(input_text) == expected
