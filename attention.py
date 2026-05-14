# attention.py
# 修复：注意力分数维度错误 + 标量计算
import numpy as np
from config import THRESHOLD_ATTENTION, LAMBDA_POS, DIM_K
from vocabulary import ExtendedVocab

def calc_pos_weight(k_pos: int, t_pos: int) -> float:
    """公式(1)：位置关联权重w_pos"""
    distance = abs(k_pos - t_pos)
    w_pos = np.exp(-LAMBDA_POS * distance)
    return w_pos

def calc_cooc_weight(k_token: str, t_token: str, tokens: list, window: int = 10) -> float:
    """公式(2)：上下文共现权重w_cooc（窗口内共现）"""
    cooc_count = 0
    n = len(tokens)
    for i in range(n):
        if tokens[i] == k_token:
            start = max(0, i - window)
            end = min(n, i + window + 1)
            cooc_count += tokens[start:end].count(t_token)
    
    k_count = tokens.count(k_token)
    t_count = tokens.count(t_token)
    if k_count == 0 or t_count == 0:
        return 0.0
    w_cooc = cooc_count / np.sqrt(k_count * t_count)
    return w_cooc

def calc_attention_score(
    q: np.ndarray, k: np.ndarray, v: np.ndarray,
    w_pos: float, w_cooc: float
) -> float:
    """公式(3)：综合注意力分数AttentionScore（修复维度问题）"""
    # 1. 原生自注意力计算：QK^T / sqrt(dk) → 输出标量
    attn = np.matmul(q, k.T) / np.sqrt(DIM_K)
    # 2. softmax 归一化（标量）
    attn_softmax = np.exp(attn) / np.sum(np.exp(attn))
    # 3. 对V取均值，压缩为标量，再与权重相乘
    attn_value = np.mean(v)  # 关键修复：将向量转为标量
    # 4. 计算最终分数（纯标量）
    attn_score = float(attn_softmax * attn_value * w_pos * w_cooc)
    return attn_score

def filter_core_tokens(
    tokens: list, malicious_tokens: list, vocab: ExtendedVocab
) -> list:
    """筛选核心恶意Token集合M：分数>阈值的普通Token + 恶意Token"""
    core_tokens = set(malicious_tokens)
    token_emb_dim = DIM_K

    for k_token in malicious_tokens:
        if k_token not in tokens:
            continue
        k_pos = tokens.index(k_token)
        # 随机初始化嵌入向量
        q = np.random.randn(1, token_emb_dim)
        k = np.random.randn(1, token_emb_dim)
        v = np.random.randn(1, token_emb_dim)

        for t_token in tokens:
            if t_token in malicious_tokens:
                continue
            t_pos = tokens.index(t_token)
            
            w_pos = calc_pos_weight(k_pos, t_pos)
            w_cooc = calc_cooc_weight(k_token, t_token, tokens)
            attn_score = calc_attention_score(q, k, v, w_pos, w_cooc)
            
            if attn_score > THRESHOLD_ATTENTION:
                core_tokens.add(t_token)
    
    # 保持原始代码顺序
    core_tokens = [t for t in tokens if t in core_tokens]
    return core_tokens