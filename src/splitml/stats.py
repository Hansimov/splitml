import tiktoken
from tclogger import logger


openai_tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(openai_tokenizer.encode(text))


def stat_tokens(nodes):
    key = "text_tokens"
    total_tokens = sum([item[key] for item in nodes])
    avg_tokens = round(total_tokens / len(nodes))
    max_tokens = max([item[key] for item in nodes])
    min_tokens = min([item[key] for item in nodes])
    logger.mesg(
        f"  - Tokens: {total_tokens} (total), {avg_tokens} (avg), {max_tokens} (max), {min_tokens} (min)"
    )
