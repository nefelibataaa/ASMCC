# reconstruct.py
# 上下文窗口提取、去重、有序拼接、恶意代码重构
from config import CONTEXT_WINDOW_SIZE

def extract_context_fragments(tokens: list, core_tokens: list) -> list:
    """提取上下文片段：每个核心Token前后各10个（共21）"""
    fragments = []
    half_window = (CONTEXT_WINDOW_SIZE - 1) // 2  # 10
    n = len(tokens)

    for token in core_tokens:
        if token not in tokens:
            continue
        pos = tokens.index(token)
        # 上下文窗口边界
        start = max(0, pos - half_window)
        end = min(n, pos + half_window + 1)
        fragment = tokens[start:end]
        fragments.append(fragment)
    return fragments

def deduplicate_and_concat(fragments: list) -> list:
    """去重 + 有序拼接：保持原始执行逻辑顺序"""
    seen = set()
    compressed_tokens = []
    for frag in fragments:
        for token in frag:
            if token not in seen:
                seen.add(token)
                compressed_tokens.append(token)
    return compressed_tokens

def reconstruct_code(compressed_tokens: list) -> str:
    """重构压缩后的恶意代码"""
    return " ".join(compressed_tokens)