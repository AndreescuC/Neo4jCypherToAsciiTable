import re
from graph import Graph, Node, Edge


def cypher_to_graph(input_file):
    graph = Graph([], [])

    with open(input_file) as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()

            if 'SET' in line:
                match = re.match(re.compile(
                    '^SET ([0-9a-zA-Z_]+).([a-zA-Z]+) = \'?([0-9a-zA-Z\s\-_]+)\'?$'
                ), line)
                if match is None or len(match.groups()) != 3:
                    print(f"Unable to parse cypher SET statement: {line}"
                          "The resulting table will not contain the effect of this statement, "
                          f"so you should probably add it by hand in the table")
                    continue
                args = match.groups()
                set_property(graph=graph, entity_name=args[0], prop=args[1], value=args[2])

            elif '[' in line and ']' in line:
                match = re.match(re.compile(
                    '^MERGE \(([0-9a-zA-Z]+)\)([-<]{1,2})\[([0-9a-zA-Z]+)?:([A-Z,_]+)\]([->]{1,2})\(([0-9a-zA-Z]+)\)$'
                ), line)
                if match is None or len(match.groups()) not in [5, 6]:
                    match = re.match(re.compile(
                        '^CREATE \(([0-9a-zA-Z]+)\)([-<]{1,2})\[([0-9a-zA-Z_]+)?:([A-Z,_]+)\]([->]{1,2})\(([0-9a-zA-Z]+)\)$'
                    ), line)
                    if match is None or len(match.groups()) not in [5, 6]:
                        print(f"Unable to parse cypher relationship creation statement: {line}\n"
                              f"The resulting table will not contain the effect of this statement, "
                              f"so you should probably add it by hand in the table")
                        continue
                args = match.groups()
                if len(args) == 5:
                    add_edge(graph=graph, node1=args[0], node2=args[4], verb=args[2], direction=args[3])
                else:
                    add_edge(graph=graph, node1=args[0], node2=args[5], verb=args[3], direction=args[4], verb_identifier=args[2])

            elif 'MERGE' in line:
                match = re.match(re.compile(
                    '^MERGE \(([0-9a-zA-Z]+)((?::(?:[a-zA-Z]+)+)+)+(?: {((?:[a-zA-Z]+:(?: )?[0-9a-zA-Z]+(?:, )?)+)})?\)$'
                ), line)
                if match is None or len(match.groups()) != 3:
                    print(f"Unable to parse cypher node MERGE statement: {line}"
                          f"The resulting table will not contain the effect of this statement, "
                          f"so you should probably add it by hand in the table")
                    continue
                args = match.groups()
                merge_node(graph=graph, node_name=args[0], unparsed_labels=args[1], unparsed_properties=args[2])

            else:
                print(f"Unable to parse unknown cypher statement: {line}"
                      f"The resulting table will not contain the effect of this statement, "
                      f"so you should probably add it by hand in the table")
                continue

    return graph


def merge_node(graph, node_name, unparsed_labels, unparsed_properties):
    labels = unparsed_labels.split(":")[1:] if unparsed_labels is not None else []

    properties = {
        prop_name: prop_value for prop_name, prop_value in
        [property.split(":") for property in unparsed_properties.split(", ")]
    } if unparsed_properties is not None else {}

    node = Node(name=node_name, labels=labels, properties=properties)
    graph.add_node(node)


def add_edge(graph, node1, node2, verb, direction, verb_identifier=None):
    if direction == "->":
        from_node = node1
        to_node = node2
    else:
        from_node = node2
        to_node = node1

    edge = Edge(name=verb, from_node=from_node, to_node=to_node, identifier=verb_identifier)
    graph.add_edge(edge)


def set_property(graph, entity_name, prop, value):
    node = [n for n in graph.nodes if n.name == entity_name]
    if len(node) == 1:
        node[0].add_property(prop, value)
    else:
        edge = [e for e in graph.edges if e.identifier == entity_name][0]
        edge.add_property(prop, value)
