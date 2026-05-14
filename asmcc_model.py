# asmcc_model.py
# ASMCC 恶意代码压缩主模型
from vocabulary import ExtendedVocab
from attention import filter_core_tokens
from reconstruct import extract_context_fragments, deduplicate_and_concat, reconstruct_code
from utils import print_separator

class ASMCCModel:
    def __init__(self):
        self.vocab = ExtendedVocab()

    def compress(self, malicious_code: str) -> str:
        """ASMCC 压缩主流程：输入原始恶意代码，输出压缩代码"""
        print_separator("1. 恶意代码分词")
        tokens = self.vocab.tokenize(malicious_code)
        print(f"原始Token：{tokens}")

        print_separator("2. 匹配恶意关键词TokenK")
        malicious_tokens = self.vocab.get_malicious_tokens(tokens)
        print(f"恶意关键词TokenK：{malicious_tokens}")

        print_separator("3. 注意力筛选核心TokenM")
        core_tokens = filter_core_tokens(tokens, malicious_tokens, self.vocab)
        print(f"核心恶意TokenM：{core_tokens}")

        print_separator("4. 提取上下文窗口片段")
        fragments = extract_context_fragments(tokens, core_tokens)
        print(f"上下文片段：{fragments}")

        print_separator("5. 去重拼接 + 代码重构")
        compressed_tokens = deduplicate_and_concat(fragments)
        compressed_code = reconstruct_code(compressed_tokens)
        return compressed_code