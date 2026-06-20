import os
import re

import capstone
import pylibemu
import requests


def get_shellcode_strings(shellcode: bytes, min_len: int = 4) -> str:
    """
    Return printable ASCII strings found in the shellcode.
    """
    pattern = rb"[ -~]{" + str(min_len).encode() + rb",}"
    found = re.findall(pattern, shellcode)
    return "\n".join(s.decode("ascii", errors="replace") for s in found)


def get_pylibemu_analysis(shellcode: bytes) -> str:
    """
    Return pylibemu emulation profile of the shellcode.
    """
    emu = pylibemu.Emulator(output_size=1024)
    offset = emu.shellcode_getpc_test(shellcode)
    if offset < 0:
        offset = 0
    emu.prepare(shellcode, offset)
    emu.test()
    return emu.emu_profile_output or "No pylibemu profile output"


def get_capstone_analysis(shellcode: bytes) -> str:
    """
    Return Capstone disassembly of the shellcode (x86 32-bit).
    """
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    lines = []
    for insn in md.disasm(shellcode, 0x1000):
        lines.append(f"0x{insn.address:08x}: {insn.mnemonic:<8} {insn.op_str}")
    return "\n".join(lines) if lines else "No instructions disassembled"


def get_llm_analysis(shellcode: bytes) -> str:
    """
    Return LLM explanation of the shellcode based on strings, disassembly and emulation.
    """
    strings = get_shellcode_strings(shellcode)
    disasm = get_capstone_analysis(shellcode)
    emulation = get_pylibemu_analysis(shellcode)

    prompt = (
        "Analyse ce shellcode et explique ce qu'il fait, son but et ses implications de sécurité.\n\n"
        f"Chaînes détectées :\n{strings or 'Aucune'}\n\n"
        f"Désassemblage (Capstone) :\n{disasm}\n\n"
        f"Profil d'émulation (pylibemu) :\n{emulation}"
    )

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('MISTRAL_KEY')}"},
        json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
