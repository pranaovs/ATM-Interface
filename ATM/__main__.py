import sys
from ATM.ui import cli


def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} [cli]")
        return

    if sys.argv[1] == "cli":
        cli.interface().cmdloop()


if __name__ == "__main__":
    main()
