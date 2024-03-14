import tiktoken


openai_tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(openai_tokenizer.encode(text))
