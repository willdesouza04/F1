import sys
import subprocess


def main():
    result = subprocess.run(["poe"] + sys.argv[1:])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
