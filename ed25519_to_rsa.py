# Ed25519 개인키에서 RSA 키를 만들어 낸다
#
# Ed25519(타원곡선)와 RSA(소인수분해)는 수학 구조가 달라서 키를 직접 변환할 수 없다.
# 대신 Ed25519 개인키의 시드(32바이트)를 난수의 씨앗으로 써서 RSA 키를 생성한다.
# 같은 Ed25519 키에서는 항상 같은 RSA 키가 나오므로, 결과적으로 "변환"처럼 동작한다.
#
# 주의: 시드는 개인키에만 들어 있으므로 공개키(test.pub)만으로는 변환할 수 없다.
import hashlib
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_ssh_private_key,
)

E = 65537
SMALL_PRIMES = [p for p in range(3, 2000, 2) if all(p % d for d in range(3, int(p**0.5) + 1, 2))]


def _is_prime(n):
    """밀러-라빈 소수 판정"""
    if any(n % p == 0 for p in SMALL_PRIMES):
        return False
    d, r = n - 1, 0
    while d % 2 == 0:
        d, r = d // 2, r + 1
    for a in [2] + SMALL_PRIMES[:39]:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_bytes(seed):
    """시드에서 항상 같은 순서의 난수 바이트를 만들어 내는 생성기"""
    counter = 0
    while True:
        yield hashlib.sha512(b"ed25519-to-rsa" + seed + counter.to_bytes(8, "big")).digest()
        counter += 1


def _next_prime(blocks, bits):
    """난수 생성기에서 후보를 꺼내 bits 비트 소수를 찾는다"""
    while True:
        data = b"".join(next(blocks) for _ in range(bits // 8 // 64))
        # 최상위 두 비트를 1로 (p*q 가 정확히 2*bits 비트가 되도록), 최하위 비트를 1로 (홀수)
        n = int.from_bytes(data, "big") | (0b11 << (bits - 2)) | 1
        if (n - 1) % E != 0 and _is_prime(n):
            return n


def rsa_from_ed25519(path, bits=2048):
    """SSH Ed25519 개인키 파일을 읽어 RSA 개인키로 변환한다"""
    ed_key = load_ssh_private_key(Path(path).read_bytes(), password=None)
    if not isinstance(ed_key, Ed25519PrivateKey):
        raise TypeError(f"{path} 는 Ed25519 개인키가 아닙니다")

    # Ed25519 개인키의 시드(32바이트)를 꺼내 난수의 씨앗으로 사용
    seed = ed_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    blocks = _random_bytes(seed)

    p = _next_prime(blocks, bits // 2)
    q = _next_prime(blocks, bits // 2)
    d = pow(E, -1, (p - 1) * (q - 1))

    return rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=rsa.rsa_crt_dmp1(d, p),
        dmq1=rsa.rsa_crt_dmq1(d, q),
        iqmp=rsa.rsa_crt_iqmp(p, q),
        public_numbers=rsa.RSAPublicNumbers(E, p * q),
    ).private_key()
