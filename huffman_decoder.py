from bitarray import bitarray
import json
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--file", required=True, help="File to decompress")
    parser.add_argument("-d", "--decoded", default="decoded.txt", help="Decompressed file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    b = bitarray()
    with open(args.file,'rb') as res:
        header_len = int.from_bytes(res.read(4), "big")
        header = res.read(header_len)
        codes = json.loads(header.decode("utf-8"))
        bit_len = int.from_bytes(res.read(4), "big")
        b.fromfile(res)

    reverse_codes = dict()
    for key in codes.keys():
        reverse_codes.update({
            codes[key]: key
        }) 
        
    data = b.to01()
    result = ''
    current = ''
    for i in range(bit_len):
        current += data[i]
        if current in reverse_codes.keys():
            result += reverse_codes[current]
            current = ''

    with open(args.decoded, 'w') as f:
        f.write(result)

