def graph_to_ascii(graph, identifiers, out_file):
    for x_identifier, y_identifier in identifiers:
        row_label, row_property = y_identifier
        col_label, col_property = x_identifier

        columns = [node for node in graph.nodes if node.has_label(col_label)]
        columns = sorted(columns, key=lambda n: n.properties[col_property], reverse=False)

        rows = [node for node in graph.nodes if node.has_label(row_label)]
        rows = sorted(rows, key=lambda n: n.properties[row_property], reverse=False)

        matrix = [
            [
                get_cell_content(graph, row, row_i, row_property, col, col_i, col_label, col_property)
                for col_i, col in enumerate(columns)
            ]
            for row_i, row in enumerate(rows)
        ]

        append_to_file(matrix, out_file)


def get_cell_content(graph, row_node, row_index, row_label, row_property,
                     column_node, column_index, column_label, column_property):
    if row_index == 0 and column_index == 0:
        return f"{row_label}/{column_label}"

    if row_index == 0:
        main_property = column_node.properties[column_property]
        remaining_properties = ', '.join([p for p in column_node.properties if p != main_property])
        return f"{main_property} ({remaining_properties})"

    if column_index == 0:
        main_property = row_node.properties[row_property]
        remaining_properties = ', '.join([p for p in row_node.properties if p != main_property])
        return f"{main_property} ({remaining_properties})"

    return ''.join([e.name for e in graph.get_edges_for(row_node, column_node)])


def append_to_file(matrix, out_file):
    pass
