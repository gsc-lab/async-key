# [송신자] 수신자의 공개키로 메시지를 암호화한다
# 키 생성: ssh-keygen -t rsa -b 2048 -f test_rsa -N ""
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

# 패딩 방식 (송신자와 수신자가 같아야 한다)
oaep = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), label=None)

# 1. 수신자의 공개키 읽기
public_key = load_ssh_public_key(Path("test_rsa.pub").read_bytes())

# 2. 보낼 메시지 입력
message = input("보낼 메시지: ").encode("utf-8")

# 3. 공개키로 암호화 (암호문만 전달한다)
ciphertext = public_key.encrypt(message, oaep)
print("암호문:", ciphertext.hex())
