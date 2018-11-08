from IPython.display import HTML, display


def tr_html(cells):
    return "<tr>{}</tr>".format(
        "".join(["<td>{}</td>".format(cell) for cell in cells])
    )


def table_html(headers, rows):
    tbl = """<table width="100%">
    <thead>{header}</thead>
    <tbody>{body}</tbody>
    </table>"""
    header_html = tr_html(headers)
    body_html = "".join([tr_html(row) for row in rows])
    return tbl.format(header=header_html, body=body_html)


def table(headers, rows):
    display(HTML(table_html(headers, rows)))


def printf(string, *args, **kwargs):
    wrapped = "<p>{}</p>".format(string)
    display(HTML(
        wrapped.format(*args, **kwargs)
    ))
