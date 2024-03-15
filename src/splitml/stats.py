import tiktoken
from tclogger import logger


openai_tokenizer = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    return len(openai_tokenizer.encode(text))


def stat_tokens(nodes, console_abnormal=False):
    key = "text_tokens"
    counts = [item[key] for item in nodes]
    total_tokens = sum(counts)
    avg_tokens = round(total_tokens / len(nodes))
    max_tokens = max(counts)
    min_tokens = min(counts)
    logger.mesg(
        f"- Tokens: {total_tokens} (total), {avg_tokens} (avg), {max_tokens} (max), {min_tokens} (min)",
        indent=4,
    )
    statistics = {
        "total": total_tokens,
        "avg": avg_tokens,
        "max": max_tokens,
        "min": min_tokens,
    }

    # print the text with abnormal tokens
    if console_abnormal:
        for idx, item in enumerate(nodes):
            if item[key] < 10:
                logger.warn(
                    f"- [{idx}]: ({item[key]} tokens): {item['text'][:100]}",
                    indent=6,
                )
    return statistics
