# [수신자] 자신의 개인키로 암호문을 복호화한다
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from ed25519_to_rsa import rsa_from_ed25519

# 패딩 방식 (송신자와 수신자가 같아야 한다)
oaep = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), label=None)

# 1. 현재 디렉토리의 Ed25519 키(test)를 RSA 로 변환해 수신자의 개인키 얻기
private_key = rsa_from_ed25519("test")

# 2. 전달받은 암호문 입력
ciphertext = bytes.fromhex(input("받은 암호문: "))

# 3. 개인키로 복호화
message = private_key.decrypt(ciphertext, oaep)
print("복호화 결과:", message.decode("utf-8"))
