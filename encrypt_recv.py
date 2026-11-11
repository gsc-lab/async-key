# [수신자] 자신의 개인키로 암호문을 복호화한다
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_ssh_private_key

# 패딩 방식 (송신자와 수신자가 같아야 한다)
oaep = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), label=None)

# 1. 수신자의 개인키 읽기
private_key = load_ssh_private_key(Path("test_rsa").read_bytes(), password=None)

# 2. 전달받은 암호문 입력
ciphertext = bytes.fromhex(input("받은 암호문: "))

# 3. 개인키로 복호화
message = private_key.decrypt(ciphertext, oaep)
print("복호화 결과:", message.decode("utf-8"))
