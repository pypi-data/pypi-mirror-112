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
    gpackets = []
    with PcapReader(str(input_file)) as packets:
        for packet_idx, p in enumerate(packets):
            payload = str(p[Raw].load)
            payload = payload.replace("b'", "")[:-1]
            gpackets.append(payload)
            if p.haslayer(TCP) and p.haslayer(Raw):
                #if (len(payload) < 4):
                #    continue



                class JSONNode():

                    def __init__(self, idx: int, packet_idx: int):
                        self.idx = idx
                        self.packet_idx = packet_idx
                        self.packets_list = []

                    def __str__(self):
                        return f"i:{self.idx} p:{self.packet_idx} c:{self.packets_list}"

                    def __repr__(self):
                        return str(self)


                #




                root_nodes = []

                #print(f"{payload:100.100}")

                def parse(brackets):
                    for idx, c in enumerate(payload):
                        if (c == "{"):
                            brackets.append(JSONNode(idx, packet_idx))
                            continue
                        if (c == "}"):
                            if (len(brackets) <= 0):
                                print(f"invalid payload")
                                break
                            node = brackets.pop()
                            # check if root element
                            if (len(brackets) == 0):
                                root_nodes.append(
                                    (node, JSONNode(idx, packet_idx)))
                            continue
                    #print(len(root_nodes))
                    return brackets


                if (args.port == p[TCP].dport):
                    req_brackets = parse(req_brackets)
                    if (len(req_brackets) > 0):
                        print("req_brackets")
                        req_brackets[0].packets_list.append(packet_idx)
                        continue
                    buffer += "->REQUEST\n"
                else:
                    res_brackets = parse(res_brackets)
                    if (len(res_brackets) > 0):
                        print("res_brackets")
                        res_brackets[0].packets_list.append(packet_idx)
                        continue
                    buffer += "<-RESPONSE\n"



                # set new payload and adjust offset
                for node in root_nodes:
                    new_payload = ""
                    if (len(node[0].packets_list) <= 0):
                        new_payload = payload[node[0].idx:node[1].idx+1]
                        #print(new_payload)
                    else:
                        adjust_offset = 1
                        for pidx in node[0].packets_list:
                            adjust_offset += len(gpackets[pidx])
                            new_payload += gpackets[pidx]
                        new_payload += gpackets[node[1].packet_idx]
                        node[1].idx += adjust_offset

                        #new_payload = new_payload[node[0].idx:node[1].idx]

                        print(node)
                        #print(gpackets[15])

                        #print(new_payload[0:20])

                        #print(new_payload[node[0].idx:node[1].idx])
                        new_payload = new_payload[node[0].idx:node[1].idx]
                        #print(new_payload)

                        #new_payload = json.loads(new_payload, strict=False)

                        #print(payload[node[1].idx-20:node[1].idx])


                    new_payload = new_payload.replace("'", "\\'")
                    new_payload = json.loads(new_payload, strict=False)
                    new_payload = json.dumps(new_payload, indent=2)
                    new_payload = "\t".expandtabs(
                        8) + new_payload.replace("\n", "\n\t".expandtabs(8))
                    buffer += f"{new_payload}\n"

                


    #print(buffer)



if __name__ == "__main__":
    main()
