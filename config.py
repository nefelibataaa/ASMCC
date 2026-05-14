# config.py
# ASMCC 模型全局配置参数
THRESHOLD_ATTENTION = 0.3    # 注意力分数阈值θ
CONTEXT_WINDOW_SIZE = 21     # 上下文窗口大小（前后各10）
LAMBDA_POS = 1.0             # 位置衰减系数λ
DIM_K = 64                   # Q/K向量维度dk