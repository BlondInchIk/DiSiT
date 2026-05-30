import argparse
from core import core

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
    
    if args.command == "genkey":
        private_key, public_key = core.generate_keypair()
        core.save_private_key(args.private, private_key)
        core.save_public_key(args.public, public_key)

        print("Ключевая пара успешно сгенерирована.")
        print(f"Закрытый ключ сохранён в файл: {args.private}")
        print(f"Открытый ключ сохранён в файл: {args.public}")

    elif args.command == "sign":
        data = core.read_file(args.file)
        private_key = core.load_private_key(args.private)

        signature = core.sign(data, private_key)
        core.save_signature(args.signature, signature)

        print("Подпись успешно сформирована.")
        print(f"Подпись сохранена в файл: {args.signature}")

    elif args.command == "verify":
        data = core.read_file(args.file)
        public_key = core.load_public_key(args.public)
        signature = core.load_signature(args.signature)

        result = core.verify(data, public_key, signature)

        if result:
            print("Подпись корректна.")
        else:
            print("Подпись некорректна.")
