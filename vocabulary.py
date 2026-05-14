# vocabulary.py
from transformers import AutoTokenizer
from prior_knowledge import PRIOR_KEYWORDS, normalize_keyword

class ExtendedVocab:
    def __init__(self):
        self.llama_tokenizer = AutoTokenizer.from_pretrained("/home/xyq/codellama")
        self.base_vocab = self.llama_tokenizer.vocab  # CodeLlama原生词表
        self.special_tokens = self.llama_tokenizer.special_tokens_map  # 特殊Token：<s>, </s>, <unk>

        self.extended_vocab = self.base_vocab.copy()
        for kw in PRIOR_KEYWORDS:
            if kw not in self.extended_vocab:
                self.extended_vocab[kw] = len(self.extended_vocab)  # 新增关键词分配新ID

        self.token2id = self.extended_vocab
        self.id2token = {v: k for k, v in self.token2id.items()}
        print(f"📚 CodeLlama基础词表大小：{len(self.base_vocab)}")
        print(f"📚 扩展后词表大小：{len(self.extended_vocab)}")

    def tokenize(self, code: str) -> list:
        """用CodeLlama BPE分词（适配代码，替代空格分词）"""
        # 归一化（不处理特殊Token）
        code = normalize_keyword(code)
        # 返回Token列表（不含特殊Token）
        tokens = self.llama_tokenizer.tokenize(code)
        return tokens

    def get_malicious_tokens(self, tokens: list) -> list:
        """匹配恶意关键词Token集合K（从分词结果中筛选）"""
        malicious_tokens = [t for t in tokens if t in PRIOR_KEYWORDS]
        return malicious_tokens