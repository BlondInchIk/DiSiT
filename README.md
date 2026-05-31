# DiSiT

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/github/license/BlondInchIk/DiSiT?style=for-the-badge)
![Release](https://img.shields.io/github/v/release/BlondInchIk/DiSiT?style=for-the-badge)
![Downloads](https://img.shields.io/github/downloads/BlondInchIk/DiSiT/total?style=for-the-badge)
![Platform](https://img.shields.io/badge/Linux-Windows-blue?style=for-the-badge)

![Stars](https://img.shields.io/github/stars/BlondInchIk/DiSiT?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/BlondInchIk/DiSiT?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/BlondInchIk/DiSiT?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/BlondInchIk/DiSiT?style=for-the-badge)

## О проекте

![Screenshot](docs/image.png)

Данный проект реализует алгоритм электронной цифровой подписи по стандарту  
[**ГОСТ Р 34.10-2012**](https://upload.wikimedia.org/wikipedia/commons/b/bc/%D0%93%D0%9E%D0%A1%D0%A2_%D0%A0_34.10-2012._%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F_%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F._%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%B8.pdf) на Python с использованием собственной криптографической реализации. Он позволяет генерировать ключи, создавать и проверять цифровые подписи файлов.

## Возможности

- Генерация ключевой пары ([private.key](private.key) / [public.key](public.key))
- Создание цифровой подписи файла
- Валидация цифровой подписи
- Кроссплатформенность (Linux / Windows)

## Варианты использования

### Запуск исполняемого файла

Шаг 1. Скачать исполняемый файл:

| Версия ОС | Ссылка на скачивание |
|------|-------------|
| Скачать для Windows | https://github.com/BlondInchIk/DiSiT/releases/latest/download/DiSiT.exe |
| Скачать для Linux | https://github.com/BlondInchIk/DiSiT/releases/latest/download/DiSiT.bin |

Шаг 2. Запустить

### Запуск из исходников

```bash
git clone https://github.com/BlondInchIk/DiSiT.git
cd DiSiT
pip install -r requirements.txt
python start.py
```

## Режимы работы

### Графический режим (GUI)

Windows
```bash
.\DiSiT.exe # Либо ТЫК по .exe
```
Linux
```bash
./DiSiT.bin
```

### Консольный режим (CLI)

Linux
```bash
$ ./DiSiT.bin --help
```
```bash
usage: DiSiT.bin [-h] {genkey,sign,verify} ...

Реализация электронной подписи ГОСТ Р 34.10-2012

positional arguments:
  {genkey,sign,verify}
    genkey              Сгенерировать ключевую пару
    sign                Сформировать электронную подпись
    verify              Проверить электронную подпись

options:
  -h, --help            show this help message and exit
```
```bash
$ ./DiSiT.bin verify --file data.txt --public public.key --signature data.txt.sig 
```
```bash
Подпись корректна.
```

Windows
```bash
.\DiSiT.exe --help
```
```bash
usage: DiSiT.exe [-h] {genkey,sign,verify} ...

Реализация электронной подписи ГОСТ Р 34.10-2012

positional arguments:
  {genkey,sign,verify}
    genkey              Сгенерировать ключевую пару
    sign                Сформировать электронную подпись
    verify              Проверить электронную подпись

options:
  -h, --help            show this help message and exit
```
```bash
.\DiSiT.exe verify --file data.txt --public public.key --signature data.txt.sig 
```
```bash
Подпись корректна.
```

## License

MIT