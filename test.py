
from pathlib import Path
from cryptography.hazmat.primitives.serialization import (
    load_ssh_private_key,
    load_ssh_public_key
)
from cryptography.exceptions import InvalidSignature

# 1. SSH 개인키와 공개키 읽기
private_key = load_ssh_private_key(
    Path("test").read_bytes(),
    password=None
)

public_key = load_ssh_public_key(
    Path("test.pub").read_bytes()
)

# 2. 서명할 메시지
message = b"Hello SSH"

# 3. 개인키로 서명
signature = private_key.sign(message)
print("서명:", signature.hex())

# 4. 공개키로 검증
try:
    public_key.verify(signature, message)
    print("서명 검증 성공!")
except InvalidSignature:
    print("서명 검증 실패!")

# 5. 메시지 변조 테스트
modified_message = b"Hello SSH!"

try:
    public_key.verify(signature, modified_message)
    print("서명 검증 성공!")
except InvalidSignature:
    print("서명 검증 실패! 메시지가 변경되었습니다.")
