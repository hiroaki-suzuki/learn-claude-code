"""テキスト処理関連のユーティリティ関数"""


def remove_all_spaces(text: str) -> str:
    """文字列からすべてのスペース（半角・全角）を除去する

    文字列の先頭、途中、末尾を問わず、すべての半角スペースと
    全角スペースを削除します。

    Args:
        text: 処理対象の文字列

    Returns:
        すべてのスペースを除去した文字列

    Examples:
        >>> remove_all_spaces("hello world")
        'helloworld'
        >>> remove_all_spaces("こんにちは　世界")
        'こんにちは世界'
        >>> remove_all_spaces("  mixed　spaces  here  ")
        'mixedspaceshere'
    """
    # 半角スペースを除去
    result = text.replace(" ", "")
    # 全角スペースを除去
    result = result.replace("　", "")
    return result


def remove_fullwidth_spaces(text: str) -> str:
    """文字列から全角スペースのみを除去する

    半角スペースはそのまま残し、全角スペース（U+3000）のみを削除します。

    Args:
        text: 処理対象の文字列

    Returns:
        全角スペースを除去した文字列

    Examples:
        >>> remove_fullwidth_spaces("hello world")
        'hello world'
        >>> remove_fullwidth_spaces("こんにちは　世界")
        'こんにちは世界'
        >>> remove_fullwidth_spaces("mixed　spaces here")
        'mixedspaces here'
    """
    return text.replace("　", "")
