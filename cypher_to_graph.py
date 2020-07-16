import re
from graph import Graph


def cypher_to_graph(input_file):
    graph = Graph([], [])

    with open(input_file) as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            print(f"Line: {line}")
            if 'SET' in line:
                args = re.match(re.compile(
                    '^SET ([0-9a-zA-Z]+).([a-zA-Z]+) = \'?([0-9a-zA-Z]+)\'?$'
                ), line).groups()
                if len(args) != 3:
                    print("Nasol")
                    exit(1)
            elif '[' in line and ']' in line:
                args = re.match(re.compile(
                    '^MERGE \(([0-9a-zA-Z]+)\)([-<]{1,2})\[:([A-Z,_]+)\]([->]{1,2})\(([0-9a-zA-Z]+)\)$'
                ), line).groups()
                if len(args) != 5:
                    print("Nasol")
                    exit(1)
            elif 'MERGE' in line:
                args = re.match(re.compile(
                    '^MERGE \(([0-9a-zA-Z]+)((?::[a-zA-Z]+)+) {((?:[a-zA-Z]+:[0-9a-zA-Z]+(?:, )?)+)}\)$'
                ), line).groups()
                if len(args) != 3:
                    print("Nasol")
                    exit(1)
            else:
                print("Nasol rau")
                exit(1)

            print(f"Graph: {graph}")

            #"MERGE (p2:Product {docId:2, available:true, sensible:false, ignored:false})"
            #"SET c1.lineName = 'Soft Lines' "
            #"MERGE (p1)-[:IN_CATEGORY]->(c1)"
            #"MERGE (p1)<-[:IS_MAIN_VENDOR]-(v1) "

    return Graph([], [])

def merge_node(graph, )
