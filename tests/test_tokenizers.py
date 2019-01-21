import pytest
from src.tokenizer import tokenize_text


def test_tokenize_text_simple():
    """Test handling of capital letters, punctuation, etc"""
    string1 = "a string to be tokenized"
    string2 = "A string to be Tokenized"
    string3 = "A string. To; be, tokenized."
    string4 = "a string? to be tokenized!!"

    tokens = ["a", "string", "to", "be", "tokenized"]

    assert tokens == tokenize_text(string1)
    assert tokens == tokenize_text(string2)
    assert tokens == tokenize_text(string3)
    assert tokens == tokenize_text(string4)


def test_tokenize_text_digits():
    """Test handling of digits"""
    string = "I was born in 1986"
    tokens = ["i", "was", "born", "in"]
    assert tokens == tokenize_text(string)

    string = "I was born 1n 1986"
    tokens = ["i", "was", "born"]
    assert tokens == tokenize_text(string)


def test_tokenize_text_accents():
    """Test handling of accented characters"""
    string = "This séntence hàs some âccënts"
    tokens = ["this", "séntence", "hàs", "some", "âccënts"]
    assert tokens == tokenize_text(string)


def test_tokenize_text_weird():
    """Test handling of weird characters"""
    string = "åß©def word ™"
    tokens = ["word"]
    assert tokens == tokenize_text(string)


def test_tokenize_text_other_alphabets():
    """Test that we handle greek, cyrllic, etc properly"""
    for string in [
        # Greek
        "αυτή είναι μια φράση γραμμένη στα αγγλικά μεταφρασμένη σε πολλές γλώσσες",
        # Russian
        "это предложение написано на английском языке переведено на многие языки",
        # Armenian
        "սա անգլերեն լեզվով գրված նախադասություն է որը թարգմանվել է բազմաթիվ լեզուներով",
        # Hebrew
        "זהו משפט כתוב באנגלית שתורגם לשפות רבות",
        # Arabic
        "هذه جملة مكتوبة باللغة الإنجليزية مترجمة إلى العديد من اللغات",
        # Korean
        "이것은 여러 언어로 번역 된 영어로 작성된 문장입니다"
    ]:
        assert string.split(" ") == tokenize_text(string)


def test_tokenize_text_nospaces():
    """TODO: implement simple handling of languages without spaces"""
    for _ in [
        # Chinese (traditional)
        "這是一個用英語翻譯成多種語言的句子",
        # Chinese (simplified)
        "这是一个用英语翻译成多种语言的句子",
        # Japanese
        "これは、英語で書かれた多くの言語に翻訳された文です。"
    ]:
        assert True
