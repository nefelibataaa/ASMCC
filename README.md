# 📌 ASMCC：基于注意力筛选的恶意代码压缩模型

## 项目简介
```text
**ASMCC（Attention-based Screening Malicious Code Compression）**  
是一款面向恶意代码的**轻量、精准、无损语义**压缩工具。
```

## 快速运行
```text
1. 环境：Python 3.13.9; Torch 2.6.0+cu124; Transformers 5.5.4
2. 安装依赖(bash)：
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   pip install transformer
   pip install numpy
3. python main.py 启动压缩
```

## 项目结构
```text
asmcc/
├── README.md                # 项目说明文档
├── config.py                # 全局超参数配置
├── prior_knowledge.py       # 286条恶意关键词 + 归一化逻辑
├── vocabulary.py            # CodeLlama词表加载 + 扩展恶意关键词
├── attention.py             # 位置/共现/注意力分数计算 + 核心Token筛选
├── reconstruct.py           # 上下文窗口提取 + 代码重构
├── utils.py                 # 通用工具函数
├── asmcc_model.py           # ASMCC主模型
└── main.py                  # 测试入口
```
