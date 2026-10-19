"""Readable test failure reports: visible whitespace, rulers, short notes."""

import sys
import textwrap
from expand import expand_tabs


SPACE = "·"
TAB = "⇥"
NL = "↵"


def _tty():
    return sys.stdout.isatty()


def _c(code, text):
    if not _tty():
        return text
    return "\033[{}m{}\033[0m".format(code, text)


def visible_char(ch):
    o = ord(ch)
    if ch == " ":
        return SPACE
    if ch == "\t":
        return TAB
    if ch == "\n":
        return NL
    if ch == "\r":
        return "␍"
    if o < 32 or o == 127:
        return "\\x{:02x}".format(o)
    if o > 126:
        return "\\u{:04x}".format(o)
    return ch


def visible(text):
    return "".join(visible_char(ch) for ch in text)


def _split_lines(text):
    if text == "":
        return [""]
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
        ended = True
    else:
        ended = False
    out = []
    for i, line in enumerate(lines):
        last = i == len(lines) - 1
        out.append(line + ("\n" if (not last or ended) else ""))
    if not out:
        out = [""]
    return out


def _ruler(width, tabstop, gutter):
    if width < 1:
        width = tabstop
    marks = []
    for col in range(1, width + 1):
        marks.append("|" if col % tabstop == 0 else ".")
    # column-number header aligned to tab stops
    header = [" "] * width
    for col in range(tabstop, width + 1, tabstop):
        lab = str(col)
        start = col - len(lab)
        if start < 0:
            start = 0
        for i, ch in enumerate(lab):
            if start + i < width:
                header[start + i] = ch
    pad = " " * gutter
    return pad + "".join(header) + "\n" + pad + "".join(marks)


def _gutter_width(nlines):
    return max(3, len(str(nlines))) + 3  # "NN | "


def format_block(title, text, tabstop=8, show_ruler=False):
    out = [_c("1", title)]
    if text == "":
        gw = _gutter_width(1)
        if show_ruler:
            out.append(_c("2", _ruler(tabstop, tabstop, gw).rstrip("\n")))
        out.append(_c("2", "{:>{w}d} | ".format(1, w=gw - 3)) + _c("2", "(empty)"))
        return "\n".join(out)

    lines = _split_lines(text)
    gw = _gutter_width(len(lines))
    if show_ruler:
        width = 0
        for line in lines:
            width = max(width, len(expand_tabs(line.replace("\n", ""), tabstop)))
        width = max(width, tabstop)
        out.append(_c("2", _ruler(width, tabstop, gw).rstrip("\n")))
    for i, line in enumerate(lines, 1):
        prefix = "{:>{w}d} | ".format(i, w=gw - 3)
        out.append(_c("2", prefix) + visible(line))
    return "\n".join(out)


def _first_diff(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            line = a[:i].count("\n") + 1
            col = i - (a.rfind("\n", 0, i) + 1) + 1
            return i, line, col
    if len(a) != len(b):
        i = n
        line = a[:i].count("\n") + 1 if a else (b[:i].count("\n") + 1 if b else 1)
        src = a if len(a) > len(b) else b
        col = i - (src.rfind("\n", 0, i) + 1) + 1
        return i, line, col
    return None


def _extract_after_label(text, label):
    key = label
    idx = text.find(key)
    if idx < 0:
        return None
    return text[idx + len(key) :]


def notes_for_stdio(got, wanted=None):
    notes = []
    labels = []
    for lab in ("Input:", "Detabed:", "Detabbed:", "Output:", "Folded:"):
        if lab in got:
            labels.append(lab.rstrip(":"))
    if labels:
        notes.append(
            "stdout includes prompt text ({}) — these tests pipe a file on stdin "
            "and compare stdout to the converted text only.".format(
                ", ".join(labels)
            )
        )
    weird = [ch for ch in got if (ord(ch) < 32 and ch not in "\n\t\r") or ord(ch) > 126]
    if weird:
        notes.append(
            "stdout contains non-text bytes. A missing '\\0' at the end of a "
            "buffer, or reading after a failed fgets, can cause this."
        )
    if "\t" in got and wanted is not None and "\t" not in wanted:
        notes.append("stdout still contains tab characters.")
    if wanted is not None:
        payload = None
        for lab in ("Detabed: ", "Detabbed: ", "Output: "):
            payload = _extract_after_label(got, lab)
            if payload is not None:
                break
        if payload is not None and payload != wanted and payload.lstrip("\n") != wanted:
            notes.append(
                "after stripping the labels, the converted text still does not match."
            )
    return notes


def mismatch(title, got, wanted, tabstop=8, notes=None):
    parts = [_c("1", title)]
    extra = list(notes or [])
    extra.extend(n for n in notes_for_stdio(got, wanted) if n not in extra)
    if extra:
        parts.append("")
        for n in extra:
            wrapped = textwrap.wrap(
                "• " + n,
                width=88,
                subsequent_indent="  ",
            )
            parts.extend(wrapped)
    diff = _first_diff(wanted, got)
    prompted = any("prompt text" in n for n in extra)
    if diff and not prompted:
        _, line, col = diff
        parts.append("")
        parts.append(
            "first difference at line {}, column {} of the byte stream "
            "(1-based).".format(line, col)
        )
    parts.append("")
    parts.append(format_block("wanted", wanted, tabstop=tabstop, show_ruler=True))
    parts.append("")
    parts.append(format_block("got", got, tabstop=tabstop, show_ruler=False))

    payload = None
    for lab in ("Detabed: ", "Detabbed: ", "Output: "):
        payload = _extract_after_label(got, lab)
        if payload is not None:
            break
    if payload is not None and payload != wanted:
        parts.append("")
        parts.append(
            format_block(
                "got, after the last prompt label",
                payload,
                tabstop=tabstop,
                show_ruler=True,
            )
        )

    parts.append("")
    parts.append(_c("2", "legend:  {} space   {} tab   {} newline".format(SPACE, TAB, NL)))
    return "\n".join(parts)
