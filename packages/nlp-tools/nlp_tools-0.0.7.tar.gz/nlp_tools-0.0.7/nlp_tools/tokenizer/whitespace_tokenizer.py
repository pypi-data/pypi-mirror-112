from nlp_tools.tokenizer.base_tokenizer import ABCTokenizer


class WhiteSpaceTokenizer(ABCTokenizer):
    """white space tokenizer
    """

    def __init__(self):
        pass

    def tokenize(self, text: str, **kwargs):
        """
        Tokenize text into token sequence
        Args:
            text: target text sample

        Returns:
            List of tokens in this sample
        """

        return text.split(" ")

    def encode(self, text: str, **kwargs):
        """
        Tokenize text into token sequence
        Args:
            text: target text sample

        Returns:
            List of tokens in this sample
        """

        return text.split(" ")

