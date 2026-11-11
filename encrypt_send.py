# [송신자] 수신자의 공개키로 메시지를 암호화한다
# 키 생성: ssh-keygen -t ed25519 -f test -N ""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from ed25519_to_rsa import rsa_from_ed25519

# 패딩 방식 (송신자와 수신자가 같아야 한다)
oaep = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), label=None)

# 1. 현재 디렉토리의 Ed25519 키(test)를 RSA 로 변환해 수신자의 공개키 얻기
#    (Ed25519 공개키 test.pub 만으로는 RSA 로 변환할 수 없어 개인키 파일을 읽는다.
#     실제 환경에서는 수신자가 변환한 RSA 공개키만 송신자에게 전달한다)
public_key = rsa_from_ed25519("test").public_key()

# 2. 보낼 메시지 입력
message = input("보낼 메시지: ").encode("utf-8")

# 3. 공개키로 암호화 (암호문만 전달한다)
ciphertext = public_key.encrypt(message, oaep)
print("암호문:", ciphertext.hex())
