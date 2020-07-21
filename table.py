class Table:
    def __init__(self, column_label, column_property, column_related_labels, row_label, row_property, row_related_labels):
        self.column = (column_label, column_property)
        self.column_related_labels = column_related_labels
        self.row = (row_label, row_property)
        self.row_related_labels = row_related_labels


def construct_tables(cmd_line_arg):
    tables = []
    for table in [table[1:].split("-") for table in cmd_line_arg.strip().split(")")][:-1]:
        row_info = table[0].split(":")
        row_identifiers = row_info[0]
        row_related = [] if len(row_info) == 1 else row_info[1].split(",")

        column_info = table[1].split(":")
        column_identifiers = column_info[0]
        column_related = [] if len(column_info) == 1 else column_info[1].split(",")

        tables.append(Table(
            column_label=column_identifiers.split(",")[0],
            column_property=column_identifiers.split(",")[1],
            column_related_labels=column_related,
            row_label=row_identifiers.split(",")[0],
            row_property=row_identifiers.split(",")[1],
            row_related_labels=row_related,
        ))

    return tables