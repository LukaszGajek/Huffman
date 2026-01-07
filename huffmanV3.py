import argparse
import heapq
import json
from bitarray import bitarray


class Node:
    def __init__(self, value, name):
        self.name = name
        self.value = value
        self.child_left = None
        self.child_right = None
        
    def add_child_left(self,child):
        self.child_left = child
        
    def add_child_right(self,child):
        self.child_right = child
        
    def __repr__(self):
        return f"{self.value,self.name}"
    

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--file", required=True, help="File to compress")
    parser.add_argument("-b", "--binary", default="results.bin", help="Zipped output file")
    return parser.parse_args()
    

def concordance(doc: str):
    con = dict()
    for letter in doc:
        con[letter] = con.setdefault(letter, 0) + 1
            
    return con

# TODO: Do poprawki
# Tutaj robisz markowanie za pomoca '0' i '1' - kazdy taki string zajmuje 1 bajt
# Jezeli mamy duzo znakow - to kazdy znak bedzie zajmowal kilka bajtow w mappingu
# A powinny to byc nie '0', '1' tylko 0b0 i 0b1 - to sa zapisy liczby binarnej
# Przyklad: jezeli kod to 0000101 to powinienes miec zapis: 5
def mark(node, codes, nodes, current_code=""):
    if node.child_left:
        codes[node.child_left.name] = current_code + '0'
        mark(nodes[node.child_left.name], codes, nodes, current_code + '0')
        
    if node.child_right:
        codes[node.child_right.name] = current_code + '1'
        mark(nodes[node.child_right.name], codes, nodes, current_code + '1')
    

def huffman(con):
    nodes = {}
    codes = {}

    queue = []
    for i in con.keys():
        queue.append([con[i],i])
    heapq.heapify(queue)
    
    while len(queue) > 1:
        a = heapq.heappop(queue)
        b = heapq.heappop(queue)
        a_node = Node(a[0],a[1])
        b_node = Node(b[0],b[1])
        new_val = a[0] + b[0]
        new_name = a[1] + b[1]
        new_node = Node(new_val, new_name)
        new_node.add_child_right(a_node)
        new_node.add_child_left(b_node)

        if a_node.name not in nodes.keys():
            nodes.update({
                a_node.name: a_node
            })
        if b_node.name not in nodes.keys():
            nodes.update({
                b_node.name: b_node
            })
        if new_node.name not in nodes.keys():
            nodes.update({
                new_node.name: new_node
            })
        heapq.heappush(queue, [new_val, new_name])
        root = new_node
        
    for i in nodes.keys():
        codes.update({
            i: ''
        })
    mark(root, codes, nodes)
    
    return nodes, codes

if __name__ == "__main__":
    args = parse_args()
    
    with open(args.file, 'r', encoding="utf-8") as f:
        dane = f.read()

    con = concordance(dane)
    result = ''

    nodes, codes = huffman(con)

    # TODO: Tutaj mamy problem
    # Co jesli chcialbys zkompresowac plik ktory ma 100GB?
    # Program padnie na braku pamieci.
    # Jakie jest rozwiazanie na to?
    # Segmentami ladowac plik i miec tylko czesc naraz w pamieci, zbudowac tablice czestosci wystepowania znakow
    # Zbudowac tak tablice Huffmana i nastepnie segmentami zapisywac do pliku wyjsciowego zakodowane linijki (linijka po linijce).
    for d in dane:
        result += codes[d]

    b = bitarray(result)  
    
    # TODO: Format binarny zeby to nie bylo takie wielkie
    codes_leaves = {}
    for key in codes.keys():
        if len(key) == 1:
            codes_leaves.update({
                key: codes[key] 
            })
                      
    with open(args.binary, 'wb') as f:
        header = json.dumps(codes_leaves).encode('utf-8')
        f.write(len(header).to_bytes(4, 'big'))  
        f.write(header)
        f.write(len(result).to_bytes(4, 'big'))  
        b.tofile(f)          

    
