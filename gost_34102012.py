import argparse
import secrets
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    from pygost.gost34112012 import GOST34112012
except ImportError:
    raise ImportError(
        "Не установлена библиотека pygost.\n"
        "Установите её командой:\n"
        "pip install pygost\n"
        "или используйте другой совместимый пакет с ГОСТ Р 34.11-2012."
    )


Point = Optional[Tuple[int, int]]  # None означает бесконечно удалённую точку


@dataclass
class Curve:
    p: int
    a: int
    b: int
    q: int
    x: int
    y: int


# Параметры тестовой/учебной кривой id-tc26-gost-3410-2012-256-paramSetA
# Используется в ГОСТ Р 34.10-2012 для 256-битного варианта.
CURVE_256_A = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97,
    a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94,
    b=0x00000000000000000000000000000000000000000000000000000000000000A6,
    q=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893,
    x=0x0000000000000000000000000000000000000000000000000000000000000001,
    y=0x8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14
)


def mod_inv(a: int, m: int) -> int:
    """
    Нахождение обратного элемента a^(-1) mod m
    с помощью расширенного алгоритма Евклида.
    """
    if a == 0:
        raise ZeroDivisionError("Обратный элемент для 0 не существует")

    old_r, r = a, m
    old_s, s = 1, 0

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    if old_r != 1:
        raise ValueError("Обратный элемент не существует")

    return old_s % m


def is_on_curve(curve: Curve, point: Point) -> bool:
    """
    Проверка принадлежности точки эллиптической кривой:
    y^2 = x^3 + ax + b mod p.
    """
    if point is None:
        return True

    x, y = point
    left = (y * y) % curve.p
    right = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p
    return left == right


def point_add(curve: Curve, p1: Point, p2: Point) -> Point:
    """
    Сложение двух точек эллиптической кривой.
    """
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % curve.p == 0:
        return None

    if p1 == p2:
        # Удвоение точки
        numerator = (3 * x1 * x1 + curve.a) % curve.p
        denominator = mod_inv((2 * y1) % curve.p, curve.p)
    else:
        # Сложение разных точек
        numerator = (y2 - y1) % curve.p
        denominator = mod_inv((x2 - x1) % curve.p, curve.p)

    lambd = (numerator * denominator) % curve.p

    x3 = (lambd * lambd - x1 - x2) % curve.p
    y3 = (lambd * (x1 - x3) - y1) % curve.p

    return x3, y3


def scalar_mult(curve: Curve, k: int, point: Point) -> Point:
    """
    Умножение точки на скаляр методом double-and-add.
    """
    if k % curve.q == 0 or point is None:
        return None

    if k < 0:
        x, y = point
        return scalar_mult(curve, -k, (x, (-y) % curve.p))

    result = None
    addend = point

    while k:
        if k & 1:
            result = point_add(curve, result, addend)
        addend = point_add(curve, addend, addend)
        k >>= 1

    return result


def streebog_256(data: bytes) -> bytes:
    """
    Вычисление хэш-кода ГОСТ Р 34.11-2012 Стрибог-256.
    """
    h = GOST34112012(data, digest_size=32)
    return h.digest()


def bytes_to_int_le(data: bytes) -> int:
    """
    В ГОСТ Р 34.10-2012 хэш-интерпретация обычно выполняется
    как little-endian.
    """
    return int.from_bytes(data, byteorder="little")


def int_to_bytes_le(value: int, size: int) -> bytes:
    return value.to_bytes(size, byteorder="little")


def hash_to_e(curve: Curve, data: bytes) -> int:
    """
    Вычисление e = alpha mod q, где alpha — число,
    соответствующее хэш-коду сообщения.
    Если e = 0, принимается e = 1.
    """
    digest = streebog_256(data)
    alpha = bytes_to_int_le(digest)
    e = alpha % curve.q
    if e == 0:
        e = 1
    return e


def generate_keypair(curve: Curve = CURVE_256_A) -> Tuple[int, Point]:
    """
    Генерация ключевой пары.
    Закрытый ключ d: 0 < d < q.
    Открытый ключ Q = dP.
    """
    base_point = (curve.x, curve.y)

    while True:
        d = secrets.randbelow(curve.q - 1) + 1
        q_point = scalar_mult(curve, d, base_point)

        if q_point is not None and is_on_curve(curve, q_point):
            return d, q_point


def sign(curve: Curve, data: bytes, private_key: int) -> Tuple[int, int]:
    """
    Формирование электронной подписи по ГОСТ Р 34.10-2012.
    """
    if not (1 <= private_key < curve.q):
        raise ValueError("Некорректный закрытый ключ")

    base_point = (curve.x, curve.y)
    e = hash_to_e(curve, data)

    while True:
        k = secrets.randbelow(curve.q - 1) + 1
        c = scalar_mult(curve, k, base_point)

        if c is None:
            continue

        x_c, _ = c
        r = x_c % curve.q

        if r == 0:
            continue

        s = (r * private_key + k * e) % curve.q

        if s == 0:
            continue

        return r, s


def verify(curve: Curve, data: bytes, public_key: Point, signature: Tuple[int, int]) -> bool:
    """
    Проверка электронной подписи по ГОСТ Р 34.10-2012.
    """
    if public_key is None:
        return False

    if not is_on_curve(curve, public_key):
        return False

    r, s = signature

    if not (0 < r < curve.q and 0 < s < curve.q):
        return False

    e = hash_to_e(curve, data)
    v = mod_inv(e, curve.q)

    z1 = (s * v) % curve.q
    z2 = (-r * v) % curve.q

    base_point = (curve.x, curve.y)

    p1 = scalar_mult(curve, z1, base_point)
    p2 = scalar_mult(curve, z2, public_key)

    c = point_add(curve, p1, p2)

    if c is None:
        return False

    x_c, _ = c
    r_calc = x_c % curve.q

    return r_calc == r


def save_private_key(path: str, private_key: int) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(hex(private_key)[2:])


def load_private_key(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        return int(f.read().strip(), 16)


def save_public_key(path: str, public_key: Point) -> None:
    if public_key is None:
        raise ValueError("Открытый ключ не может быть бесконечно удалённой точкой")

    x, y = public_key

    with open(path, "w", encoding="utf-8") as f:
        f.write(hex(x)[2:] + "\n")
        f.write(hex(y)[2:] + "\n")


def load_public_key(path: str) -> Point:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) != 2:
        raise ValueError("Файл открытого ключа должен содержать две строки: x и y")

    x = int(lines[0], 16)
    y = int(lines[1], 16)

    return x, y


def save_signature(path: str, signature: Tuple[int, int]) -> None:
    r, s = signature

    with open(path, "w", encoding="utf-8") as f:
        f.write(hex(r)[2:] + "\n")
        f.write(hex(s)[2:] + "\n")


def load_signature(path: str) -> Tuple[int, int]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) != 2:
        raise ValueError("Файл подписи должен содержать две строки: r и s")

    r = int(lines[0], 16)
    s = int(lines[1], 16)

    return r, s


def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def cli():
    parser = argparse.ArgumentParser(
        description="Реализация электронной подписи ГОСТ Р 34.10-2012"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("genkey", help="Сгенерировать ключевую пару")
    gen_parser.add_argument("--private", required=True, help="Файл для закрытого ключа")
    gen_parser.add_argument("--public", required=True, help="Файл для открытого ключа")

    sign_parser = subparsers.add_parser("sign", help="Сформировать электронную подпись")
    sign_parser.add_argument("--file", required=True, help="Файл для подписи")
    sign_parser.add_argument("--private", required=True, help="Файл закрытого ключа")
    sign_parser.add_argument("--signature", required=True, help="Файл для сохранения подписи")

    verify_parser = subparsers.add_parser("verify", help="Проверить электронную подпись")
    verify_parser.add_argument("--file", required=True, help="Проверяемый файл")
    verify_parser.add_argument("--public", required=True, help="Файл открытого ключа")
    verify_parser.add_argument("--signature", required=True, help="Файл подписи")

    args = parser.parse_args()
    curve = CURVE_256_A

    if args.command == "genkey":
        private_key, public_key = generate_keypair(curve)
        save_private_key(args.private, private_key)
        save_public_key(args.public, public_key)

        print("Ключевая пара успешно сгенерирована.")
        print(f"Закрытый ключ сохранён в файл: {args.private}")
        print(f"Открытый ключ сохранён в файл: {args.public}")

    elif args.command == "sign":
        data = read_file(args.file)
        private_key = load_private_key(args.private)

        signature = sign(curve, data, private_key)
        save_signature(args.signature, signature)

        print("Подпись успешно сформирована.")
        print(f"Подпись сохранена в файл: {args.signature}")

    elif args.command == "verify":
        data = read_file(args.file)
        public_key = load_public_key(args.public)
        signature = load_signature(args.signature)

        result = verify(curve, data, public_key, signature)

        if result:
            print("Подпись корректна.")
        else:
            print("Подпись некорректна.")


if __name__ == "__main__":
    cli()
