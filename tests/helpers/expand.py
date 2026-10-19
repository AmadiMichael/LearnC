"""Display-column helpers for tests. Not part of the exercises."""


def expand_tabs(text, tabstop):
    out = []
    col = 0
    for ch in text:
        if ch == "\t":
            spaces = tabstop - (col % tabstop)
            out.append(" " * spaces)
            col += spaces
        elif ch == "\n":
            out.append(ch)
            col = 0
        else:
            out.append(ch)
            if ch != "\r":
                col += 1
    return "".join(out)


def display_length(line, tabstop):
    """Length of one line in columns (no newline in line)."""
    return len(expand_tabs(line, tabstop).split("\n", 1)[0])
