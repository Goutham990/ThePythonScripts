import base64
import json
import re
import sys
from scapy.all import rdpcap
from io import BytesIO

def decode_base64(data):
    try:
        return base64.b64decode(data)
    except Exception:
        return None

def extract_bmp_number(bmp_bytes):
    if not bmp_bytes:
        return 0
    try:
        pattern = b"ABC{"
        idx = bmp_bytes.find(pattern)
        if idx == -1:
            return 0
        end_idx = bmp_bytes.find(b"}", idx)
        if end_idx == -1:
            return 0
        number_bytes = bmp_bytes[idx + 4:end_idx]
        number_str = number_bytes.decode("ascii")
        if number_str.isdigit():
            return int(number_str)
        return 0
    except:
        return 0

def extract_pcap_number(pcap_bytes):
    if not pcap_bytes:
        return 0
    try:
        packets = rdpcap(BytesIO(pcap_bytes))
        for pkt in packets:
            pkt_bytes = bytes(pkt)
            idx = pkt_bytes.find(b"ABC{")
            if idx != -1:
                end_idx = pkt_bytes.find(b"}", idx)
                if end_idx != -1:
                    number_bytes = pkt_bytes[idx + 4:end_idx]
                    number_str = number_bytes.decode("ascii")
                    if number_str.isdigit():
                        return (int(number_str) % 10007) + 3
        return 0
    except:
        return 0

def simulate_mysticlang(bytecode, memory_address):
    if bytecode is None or not (0 <= memory_address <= 255):
        return 0

    memory = [0] * 256
    pc = 0
    try:
        while pc < len(bytecode):
            opcode = bytecode[pc]

            if opcode == 0x01:
                if pc + 2 >= len(bytecode): break
                addr, val = bytecode[pc + 1], bytecode[pc + 2]
                memory[addr % 256] = val % 256
                pc += 3
            elif opcode == 0x02:
                if pc + 3 >= len(bytecode): break
                a1, a2, dest = bytecode[pc + 1], bytecode[pc + 2], bytecode[pc + 3]
                memory[dest % 256] = (memory[a1 % 256] + memory[a2 % 256]) % 256
                pc += 4
            elif opcode == 0x03:
                if pc + 2 >= len(bytecode): break
                src, dest = bytecode[pc + 1], bytecode[pc + 2]
                memory[dest % 256] = memory[src % 256]
                pc += 3
            elif opcode == 0x04:
                if pc + 1 >= len(bytecode): break
                addr = bytecode[pc + 1]
                memory[addr % 256] = (memory[addr % 256] + 1) % 256
                pc += 2
            elif opcode == 0x05:
                if pc + 1 >= len(bytecode): break
                addr = bytecode[pc + 1]
                memory[addr % 256] = (memory[addr % 256] - 1) % 256
                pc += 2
            elif opcode == 0xFF:
                break
            else:
                break
    except:
        return 0

    return memory[memory_address]

def process_test_case(case):
    try:
        bmp_data = decode_base64(case.get("bmp", ""))
        pcap_data = decode_base64(case.get("pcap", ""))
        mystic_code = decode_base64(case.get("mystic", ""))
        mem_addr = case.get("memory_address", 0)

        if bmp_data is None or pcap_data is None or mystic_code is None:
            return "0 0 0"

        bmp_result = extract_bmp_number(bmp_data)
        pcap_result = extract_pcap_number(pcap_data)
        mystic_result = simulate_mysticlang(list(mystic_code), mem_addr)

        return "{} {} {}".format(bmp_result, pcap_result, mystic_result)
    except:
        return "0 0 0"

def main():
    input_data = sys.stdin.read().strip()
    try:
        decoded_json = base64.b64decode(input_data).decode()
        test_cases = json.loads(decoded_json)
        for case in test_cases:
            print(process_test_case(case))
    except:
        print("0 0 0")

if __name__ == "__main__":
    main()
