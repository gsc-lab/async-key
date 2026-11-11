# [송신자] 자신의 개인키로 메시지에 서명한다
# 키 생성: ssh-keygen -t ed25519 -f test -N ""
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_ssh_private_key

# 1. 송신자의 개인키 읽기
private_key = load_ssh_private_key(Path("test").read_bytes(), password=None)

# 2. 보낼 메시지 입력
message = input("보낼 메시지: ").encode("utf-8")

# 3. 개인키로 서명 (메시지는 암호화되지 않으므로, 메시지와 서명을 함께 전달한다)
signature = private_key.sign(message)
print("서명:", signature.hex())
