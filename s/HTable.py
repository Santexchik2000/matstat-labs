from IPython.display import HTML, display


def I(x):
    return x


class HTMLRenderable:
    _classes = None
    _attrs = None
    _content = None
    _css = None

    def __init__(self):
        self._classes = []
        self._attrs = {}
        self._content = ""
        self._css = {}

    def add_class(self, *classnames):
        for classname in classnames:
            self._classes.append(classname)
        return self

    def tag(self):
        return "span"

    def attrs(self):
        return self._attrs

    def content(self):
        return self._content

    def classes(self):
        return self._classes

    def css(self):
        return self._css

    def render(self):
        tag = self.tag()
        attrs = self.attrs()
        classes = self.classes()
        content = self.content()
        styles = self.css()

        if len(classes):
            attrs["class"] = " ".join(classes)

        if len(styles):
            style_values = [
                "{prop}: {value};".format(prop=prop, value=styles[prop]) for prop in styles
            ]
            attrs["style"] = "".join(style_values)

        attrs_string = ""
        if len(attrs):
            attrs_string = " {all}".format(all=" ".join([
                "{name}=\"{value}\"".format(name=name, value=attrs[name]) for name in attrs
            ]))

        return "<{tag}{attrs}>{content}</{tag}>".format(tag=tag, attrs=attrs_string, content=content)

    def show(self):
        display(HTML(self.render()))


class Cell(HTMLRenderable):
    _colspan = 1
    _rowspan = 1
    _is_head = False
    _content = '&nbsp;'
    _hidden = False
    row = None

    def __init__(self, rowspan=1, colspan=1, is_head=False):
        super(Cell, self).__init__()
        self._rowspan = rowspan
        self._colspan = colspan
        self._is_head = is_head

    def span(self, rowspan=1, colspan=1):
        self._colspan = colspan
        self._rowspan = rowspan
        self.row.table.span(cell=self, rowspan=rowspan, colspan=colspan)
        return self

    def head(self, is_head):
        self._is_head = is_head
        return self

    def fill(self, content):
        self._content = content
        return self

    def hide(self, hidden=True):
        self._hidden = hidden
        return self

    def tag(self):
        return "th" if self._is_head else "td"

    def attrs(self):
        result = super(Cell, self).attrs()

        if self._rowspan > 1:
            result["rowspan"] = self._rowspan

        if self._colspan > 1:
            result["colspan"] = self._colspan

        return result

    def content(self):
        return self._content

    def render(self):
        if self._hidden:
            return ""
        return super(Cell, self).render()


class TableRow(HTMLRenderable):
    cells = None
    table = None
    is_head = False

    def __init__(self, cells=None, table=None):
        super(TableRow, self).__init__()
        if cells is None:
            self.cells = []
        else:
            self.cells = cells

        self.table = table

        for cell in cells:
            cell.row = self

    def tag(self):
        return "tr"

    def content(self):
        return "".join(cell.render() for cell in self.cells)


class HTable(HTMLRenderable):
    _head = None
    _rows = None

    def __init__(self, rows, cols, head_rows=0):
        super(HTable, self).__init__()
        self._rows = []
        self._head = []

        for i in range(rows):
            cells = [Cell() for j in range(cols)]
            row = TableRow(cells=cells, table=self)
            self._rows.append(row)

        for i in range(head_rows):
            cells = [Cell(is_head=True) for j in range(cols)]
            row = TableRow(cells=cells, table=self)
            row.is_head = True
            self._head.append(row)

    def span(self, cell, rowspan, colspan):
        row_object = cell.row
        col = row_object.cells.index(cell)
        l = self._head if row_object.is_head else self._rows
        row = l.index(row_object)
        for c in range(colspan):
            for r in range(rowspan):
                if c == 0 and r == 0:
                    continue
                self.at(row=r + row, col=c + col).hide()

    def map_row(self, row, f, head=False, limits=None):
        l = self._head if head else self._rows
        row_object = l[row]
        if limits is None:
            limits = (0, len(row_object.cells))
        return [
            f(cell) for cell in row_object.cells[ limits[0]:limits[1] ]
        ]

    def map_col(self, col, f, head=False, limits=None):
        result = []
        l = self._head if head else self._rows
        if limits is None:
            limits = (0, len(l))
        for i in range(limits[0], limits[1]):
            row = l[i]
            cell = row.cells[col]
            result.append(f(cell))
        return result

    def at(self, row, col):
        return self._rows[row].cells[col]

    def fill(self, row=None, col=None, content=None, head=False):
        if (row is None and col is None) or (row is not None and col is not None):
            raise ValueError("You should specify either a col or a row")

        if content is None:
            return

        cells = None
        if row is not None:
            cells = self.map_row(row=row, f=I, head=head)

        if col is not None:
            cells = self.map_col(col=col, f=I, head=head)

        for i in range(len(content)):
            if content[i] is not None:
                cells[i].fill(content[i])

    def tag(self):
        return "table"

    def classes(self):
        result = super(HTable, self).classes()
        result.append("htable")
        return result

    def attrs(self):
        result = super(HTable, self).attrs()
        result["width"] = "100%"
        return result

    def content(self):
        head = ""
        body = ""
        if len(self._head):
            head = "<thead>{}</thead>".format(
                "".join(row.render() for row in self._head)
            )

        if len(self._rows):
            body = "<tbody>{}</tbody>".format(
                "".join(row.render() for row in self._rows)
            )

        return head + body
