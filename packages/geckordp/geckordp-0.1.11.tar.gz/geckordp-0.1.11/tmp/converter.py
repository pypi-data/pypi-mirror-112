import argparse
import json
from pathlib import Path
from scapy.all import PcapReader, re, Raw, TCP, IP


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=str, default="",
                        help="Input file to convert to.")
    parser.add_argument("-p", "--port", type=int, default=6000,
                        help="The port of the remote debug server.")
    args, _ = parser.parse_known_args()

    input_file = Path(args.input).absolute()
    if (not input_file.exists() or input_file.is_dir()):
        print(f"invalid input file '{input_file}'")

    merged_blocks = 0
    merged_payload = ""
    buffer = ""
    req_brackets = []
    res_brackets = []
    with PcapReader(str(input_file)) as packets:
        for p in packets:
            #if p.haslayer(TCP) and p.haslayer(Raw) and p[TCP].dport == 80:
            #    payload = p[Raw].load
            if p.haslayer(TCP) and p.haslayer(Raw):
                payload = str(p[Raw].load)

                if (len(payload) < 4):
                    continue

                """ print(payload)
                print(payload[-1])

                if (payload[-1] != "'"):
                    merged_blocks += 1
                    merged_payload += payload
                    print("merge")
                    continue
                else:
                    payload = merged_payload
                    if (merged_blocks > 0):
                        merged_payload = "" """

                #print(payload)
                #print(p[TCP].dport)

                """ is_request = True
                if (args.port == p[TCP].dport):
                    buffer += "->REQUEST\n"
                else:
                    is_request = False
                    buffer += "<-RESPONSE\n" """

                """ payload = payload.replace("b'", "")[:-1]
                try:
                    c_count = 0
                    for c in payload:
                        c_count += 1
                        if (c.isdigit()):
                            continue
                        if (c == ':'):
                            break
                    payload = payload[c_count:]
                    payload = json.loads(payload, strict=False)
                    payload = json.dumps(payload, indent=2)
                    payload = "\t".expandtabs(4) + payload.replace("\n", "\n\t".expandtabs(4))
                    #print(payload)

                    buffer += f"{payload}\n"
                except Exception as ex:
                    print(f"ERROR {ex}\n'{payload}'") """

                class JSONNode():

                    def __init__(self, idx: int):
                        self.idx = idx
                        self.elements = None

                payload = payload.replace("b'", "")[:-1]

                root_nodes = []

                #print(f"{payload:100.100}")
                def parse(brackets):
                    idx = 0
                    for c in payload:
                        if (c == "{"):
                            brackets.append(JSONNode(idx))
                            continue
                        if (c == "}"):
                            brackets_len = len(brackets)
                            if (brackets_len <= 0):
                                print(f"invalid payload")
                                break
                            node = brackets.pop()
                            # check if root element
                            if (brackets_len == 0):
                                root_nodes.append((node.idx, idx))
                            continue
                        idx += 1

                if (args.port == p[TCP].dport):
                    parse(req_brackets)
                    if (len(req_brackets) > 0):
                        print("req_brackets")
                        continue
                    buffer += "->REQUEST\n"
                else:
                    parse(res_brackets)
                    if (len(res_brackets) > 0):
                        print("res_brackets")
                        continue
                    buffer += "<-RESPONSE\n"

                #print(root_nodes)

                #break
    #print(buffer)
if __name__ == "__main__":
    main()
