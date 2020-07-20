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
                get_cell_content(graph, row, row_i, row_label, row_property, col, col_i, col_label, col_property)
                for col_i, col in enumerate([None] + columns)
            ]
            for row_i, row in enumerate([None] + rows)
        ]

        append_to_file(matrix, out_file)


def get_cell_content(graph, row_node, row_index, row_label, row_property,
                     column_node, column_index, column_label, column_property):
    if row_index == 0 and column_index == 0:
        return f"{row_label}/{column_label}"

    if row_index == 0:
        main_property = column_node.properties[column_property]
        remaining_properties = ', '.join([f"{p}:{v}" for p, v in column_node.properties.items() if p != column_property])
        return f"{main_property} ({remaining_properties})"

    if column_index == 0:
        main_property = row_node.properties[row_property]
        remaining_properties = ', '.join([f"{p}:{v}" for p, v in row_node.properties.items() if p != column_property])
        return f"{main_property} ({remaining_properties})"

    return ''.join([e.name for e in graph.get_edges_for(row_node, column_node)])


def append_to_file(matrix, out_file):
    open(out_file, 'w').close()

    width, height = len(matrix[0]), len(matrix)
    cols_max_size = [max([len(cell) for cell in [matrix[i][j] for i in range(height)]]) for j in range(width)]

    delimiter_row = f'|{"|".join(["-" * (col_size + 2) for col_size in cols_max_size])}|\n'
    matrix_string = "\n"

    for row in matrix:
        matrix_string += delimiter_row
        for col_index, cell in enumerate(row):
            if cell == "":
                cell = "X"
            left_padding = " " * ((cols_max_size[col_index] - len(cell)) // 2 + 1)
            right_padding = left_padding if (cols_max_size[col_index] - len(cell)) % 2 == 0 else left_padding + " "
            matrix_string += f"|{left_padding}{cell}{right_padding}"
        matrix_string += "|\n"

    matrix_string += delimiter_row + "\n"

    with open(out_file, "a") as myfile:
        myfile.write(matrix_string)
