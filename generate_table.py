#!/usr/bin/env python

import sys
import argparse
from table import construct_tables
from cypher_to_graph import cypher_to_graph
from graph_to_ascii import graph_to_ascii


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', type=str, required=True,
        help='The input file containing cypher statements (one cypher statement per line)'
    )
    parser.add_argument('-o', '--output', type=str, default="out", required=False,
                        help='The output file in which the resulting ascii table will be written')
    parser.add_argument('-d', '--dimensions', nargs='+', required=True,
                        help='List of dimensions used for building the matrices; each matrix should respect the format: ' \
                             '"(LabelUsedForColumns,propertyUsedForColumnsHeader - LabelUsedForRows,propertyUsedForRowsHeader)"; ' \
                             'Matrices should be provided with no character between them in the input\n' \
                             'e. g.: for building 2 matrices, customers-products and users-products: ' \
                             '-d "(Customer,customerId-Product,docId)(User,userId-Product,docId)"')
    parser.add_argument('-p', '--properties', action="store_true", required=False,
                        help='If passed, lists all properties of the node in the table header')
    args = parser.parse_args()

    return args.input, args.output, construct_tables(args.dimensions[0]), args.properties


def main():
    in_file, out_file, tables, show_properties = parse_args()
    print(show_properties)
    graph = cypher_to_graph(in_file)
    graph_to_ascii(graph, tables, out_file, ' '.join(sys.argv), show_properties)


if __name__ == '__main__':
    main()
