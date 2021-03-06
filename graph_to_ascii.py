import yaml


def graph_to_ascii(graph, tables, out_file, ran_command, show_properties):
    content = f"/**\nThese tables were generated by running the command:\n{ran_command}\n\n"

    for table in tables:
        row_label, row_property = table.row[0], table.row[1]
        col_label, col_property = table.column[0], table.column[1]

        columns = [node for node in graph.nodes if node.has_label(col_label)]
        columns = sorted(columns, key=lambda n: n.properties[col_property], reverse=False)

        rows = [node for node in graph.nodes if node.has_label(row_label)]
        rows = sorted(rows, key=lambda n: n.properties[row_property], reverse=False)

        matrix = [
            [
                get_cell_content(table, graph, row, row_i, row_label, row_property, col, col_i, col_label, col_property,
                                 show_properties)
                for col_i, col in enumerate([None] + columns)
            ]
            for row_i, row in enumerate([None] + rows)
        ]

        content += get_matrix_string(matrix)

    content = content.replace("\n", "\n* ") + "\n*/"

    with open(out_file, "w") as out:
        out.write(content)


def get_cell_content(table, graph, row_node, row_index, row_label, row_property,
                     column_node, column_index, column_label, column_property, show_properties):
    if row_index == 0 and column_index == 0:
        return f"{row_property}/{column_property}"

    if row_index == 0:
        main_property = column_node.properties[column_property]
        remaining_properties = [f"{p}:{v}" for p, v in column_node.properties.items() if p != column_property]
        remaining_properties = f" ({', '.join(remaining_properties)})" \
            if len(remaining_properties) > 0 and show_properties \
            else ""

        remaining_labels = ')('.join([l for l in column_node.labels if l != column_label])
        if remaining_labels != "":
            remaining_labels = f"[{remaining_labels}]"

        if len(table.column_related_labels) > 0:
            related_nodes = graph.get_labeled_related_nodes_for(column_node, table.column_related_labels)
            related_nodes = f' ({", ".join(related_nodes)})' if len(related_nodes) > 0 else ""
        else:
            related_nodes = ""

        return f"{main_property}{remaining_labels}{related_nodes}{remaining_properties}"

    if column_index == 0:
        main_property = row_node.properties[row_property]
        remaining_properties = [f"{p}:{v}" for p, v in row_node.properties.items() if p != row_property]
        remaining_properties = f" ({', '.join(remaining_properties)})" \
            if len(remaining_properties) > 0 and show_properties \
            else ""

        remaining_labels = ')('.join([l for l in row_node.labels if l != row_label])
        if remaining_labels != "":
            remaining_labels = f"[{remaining_labels}]"

        if len(table.row_related_labels) > 0:
            related_nodes = graph.get_labeled_related_nodes_for(row_node, table.row_related_labels)
            related_nodes = f' ({", ".join(related_nodes)})' if len(related_nodes) > 0 else ""
        else:
            related_nodes = ""

        return f"{main_property}{remaining_labels}{related_nodes}{remaining_properties}"

    return ','.join([
        e.get_representation()
        for e in graph.get_edges_for(row_node, column_node)
    ])


def get_matrix_string(matrix):
    matrix, legend = convert_aliases(matrix)
    content = f"{get_written_legend(legend)}\n\n"

    width, height = len(matrix[0]), len(matrix)
    cols_max_size = [max([len(cell) for cell in [matrix[i][j] for i in range(height)]]) for j in range(width)]

    delimiter_row = f'|{"+".join(["-" * (col_size + 2) for col_size in cols_max_size])}|\n'

    for row in matrix:
        content += delimiter_row
        for col_index, cell in enumerate(row):
            if cell == "":
                cell = " "
            left_padding = " " * ((cols_max_size[col_index] - len(cell)) // 2 + 1)
            right_padding = left_padding if (cols_max_size[col_index] - len(cell)) % 2 == 0 else left_padding + " "
            content += f"|{left_padding}{cell}{right_padding}"
        content += "|\n"

    return content + delimiter_row + "\n"


def convert_aliases(matrix):
    with open("aliases.yaml", 'r') as stream:
        aliases = yaml.safe_load(stream)

    legend = {}
    parsed_matrix = [["" for _ in row] for row in matrix]
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            for prop, alias in aliases["Property"].items():
                if cell.find(f"{prop}:") > -1:
                    legend[alias] = prop
                    cell = cell.replace(f"{prop}:", f"{alias}:")

            for label, alias in aliases["Label"].items():
                if cell.find(f"[{label}]") > -1:
                    legend[alias] = label
                    cell = cell.replace(f"[{label}]", f"[{alias}]")

            for rel, alias in aliases["Relationship"].items():
                if cell.find(f"{rel}") > -1:
                    legend[alias] = rel
                    cell = cell.replace(f"{rel}", f"{alias}")

            parsed_matrix[i][j] = cell

    return parsed_matrix, legend


def get_written_legend(legend):
    return "\n".join([f"{symbol} - {meaning}" for symbol, meaning in legend.items()])
