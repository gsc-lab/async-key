# async-key

비대칭키(공개키/개인키)의 서명·검증과 암호화·복호화 원리를 실습하는 예제입니다.

## 준비

```
git clone https://github.com/gsc-lab/async-key.git
cd async-key
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

키 파일은 저장소에 없으므로 직접 만듭니다.

```
ssh-keygen -t ed25519 -f test -N ""
```

- `test`, `test.pub` : 서명용 키 (Ed25519)
- 암호화용 RSA 키는 따로 만들지 않고, `ed25519_to_rsa.py` 가 `test` 를 RSA 키로 변환해 사용합니다.

## 실습 1. 서명과 검증

| 프로그램 | 역할 | 사용하는 키 |
|---|---|---|
| `sign_send.py` | 송신자: 메시지에 서명 | 개인키 `test` |
| `sign_recv.py` | 수신자: 서명 검증 | 공개키 `test.pub` |

1. `python sign_send.py` 를 실행해 메시지를 입력하고, 출력된 서명을 복사합니다.
2. `python sign_recv.py` 를 실행해 같은 메시지와 복사한 서명을 입력합니다.
3. 메시지를 한 글자 바꿔서 다시 입력하면 검증이 실패하는지 확인합니다.

서명은 메시지를 숨기지 않습니다. 메시지는 평문 그대로 전달되고, 서명은 "누가 보냈는지"와 "변경되지 않았는지"만 확인합니다.

## 실습 2. 암호화와 복호화

| 프로그램 | 역할 | 사용하는 키 |
|---|---|---|
| `encrypt_send.py` | 송신자: 메시지 암호화 | `test` 를 변환한 RSA 공개키 |
| `encrypt_recv.py` | 수신자: 암호문 복호화 | `test` 를 변환한 RSA 개인키 |

Ed25519 와 RSA 는 수학 구조가 달라 키를 직접 변환할 수 없습니다. 그래서 Ed25519 개인키의 시드를 난수의 씨앗으로 써서 RSA 키를 만듭니다. 같은 `test` 에서는 항상 같은 RSA 키가 나옵니다. 시드는 개인키에만 있으므로 `test.pub` 만으로는 변환할 수 없고, 이 실습에서는 송신자도 `test` 를 읽습니다.

1. `python encrypt_send.py` 를 실행해 메시지를 입력하고, 출력된 암호문을 복사합니다.
2. `python encrypt_recv.py` 를 실행해 복사한 암호문을 입력합니다.
3. 같은 메시지를 다시 암호화하면 암호문이 매번 달라지는지 확인합니다.

## 참고

`test.py` 는 서명과 검증을 한 파일에서 실행하는 예제입니다.
