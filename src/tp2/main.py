from tp2.utils.config import logger
from tp2.utils.shellcode import (
    get_capstone_analysis,
    get_llm_analysis,
    get_pylibemu_analysis,
    get_shellcode_strings,
)

# linux/x86 execve /bin/sh shellcode
SHELLCODE = bytes([
    0x31, 0xc0, 0x50, 0x68, 0x2f, 0x2f, 0x73, 0x68,
    0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x50,
    0x53, 0x89, 0xe1, 0xb0, 0x0b, 0xcd, 0x80,
])


def main():
    logger.info("Starting TP2 - Shellcode Analysis")

    print("\n=== Strings ===")
    print(get_shellcode_strings(SHELLCODE))

    print("\n=== Capstone Disassembly ===")
    print(get_capstone_analysis(SHELLCODE))

    print("\n=== Pylibemu Analysis ===")
    print(get_pylibemu_analysis(SHELLCODE))

    print("\n=== LLM Analysis ===")
    print(get_llm_analysis(SHELLCODE))


if __name__ == "__main__":
    main()
