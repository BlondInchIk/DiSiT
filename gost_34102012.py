import sys

def is_cli_mode():
    return len(sys.argv) > 1

def main():
    if is_cli_mode():
        from cli import cli
        cli.cli()
    else:
        from gui import gui
        gui.gui()

if __name__ == "__main__":
    main()
