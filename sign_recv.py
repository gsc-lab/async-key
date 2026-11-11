# [수신자] 송신자의 공개키로 서명을 검증한다
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

# 1. 송신자의 공개키 읽기
public_key = load_ssh_public_key(Path("test.pub").read_bytes())

# 2. 전달받은 메시지와 서명 입력
message = input("받은 메시지: ").encode("utf-8")
signature = bytes.fromhex(input("받은 서명: "))

# 3. 공개키로 검증
try:
    public_key.verify(signature, message)
    print("서명 검증 성공!")
except InvalidSignature:
    print("서명 검증 실패! 메시지 또는 서명이 변경되었습니다.")
