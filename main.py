import argparse
from cypher_to_graph import cypher_to_graph
from graph_to_ascii import graph_to_ascii


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', type=str, required=True,
        help='The input file containing cypher statements (one cypher statement per line)'
    )
    parser.add_argument('-o', '--output', type=str, default="ascii_table_out.java", required=False,
                        help='The output file in which the resulting ascii table will be written')
    parser.add_argument('-d', '--dimensions', nargs='+', required=True,
                        help='List of dimensions used for building the matrices; each matrix should respect the format: ' \
                             '"(LabelUsedForColumns,propertyUsedForColumnsHeader - LabelUsedForRows,propertyUsedForRowsHeader)"; ' \
                             'Matrices should be provided with no character between them in the input\n' \
                             'e. g.: for building 2 matrices, customers-products and users-products: ' \
                             '-d "(Customer,customerId - Product,docId)(User,userId - Product,docId)"')
    args = parser.parse_args()

    return args.input, args.output, parse_dimension_arg(args.dimensions)


def parse_dimension_arg(dim):
    return dim


def main():
    in_file, out_file, dimensions = parse_args()
    graph = cypher_to_graph(in_file)
    graph_to_ascii(graph, dimensions, out_file)


if __name__ == '__main__':
    main()
