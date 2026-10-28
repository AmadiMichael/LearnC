"""Detab and entab with an explicit list of tab stops.

Column 1 is the first column on the line. A stop at 4 means a tab reaches
column 4. With no stops, tabs are every 8 columns.
"""

from pretty import mismatch

DEFAULT = 8


def stops_for(tokens):
    """Turn command-line arguments into the stops the checker uses.

    A column list stays a list. -m +n is every n columns starting at column m.
    +n alone starts at column n. -m alone repeats every 8 columns.
    """
    if not tokens:
        return []
    if any(tok[:1] in "+-" for tok in tokens):
        origin = step = None
        for tok in tokens:
            if tok.startswith("+"):
                step = int(tok[1:])
            elif tok.startswith("-"):
                origin = int(tok[1:])
        if step is None:
            step = DEFAULT
        if origin is None:
            origin = step
        return ("every", origin, step)
    return [int(tok) for tok in tokens]


def next_stop(col, stops):
    """col is how many columns are already filled. The next stop is greater than col."""
    if isinstance(stops, tuple):
        _, origin, step = stops
        if col < origin:
            return origin
        return origin + step * (((col - origin) // step) + 1)
    nxt = None
    for stop in stops:
        if stop > col and (nxt is None or stop < nxt):
            nxt = stop
    if nxt is not None:
        return nxt
    return ((col // DEFAULT) + 1) * DEFAULT


def expand(text, stops):
    out = []
    col = 0
    for ch in text:
        if ch == "\t":
            stop = next_stop(col, stops)
            out.append(" " * (stop - col))
            col = stop
        elif ch == "\n":
            out.append(ch)
            col = 0
        else:
            out.append(ch)
            col += 1
    return "".join(out)


def describe(stops):
    if not stops:
        return "tab stops every 8 columns"
    if isinstance(stops, tuple):
        _, origin, step = stops
        return "tab stops every {} columns, starting at column {}".format(step, origin)
    cols = ", ".join(str(stop) for stop in sorted(set(stops)))
    return "tab stops at column " + cols


def check_detab(original, result, stops):
    expected = expand(original, stops)
    if result == expected:
        return True, ""
    notes = [describe(stops) + "."]
    notes.append("a tab is replaced by spaces out to the next stop. A newline resets the column.")
    if "\t" in result:
        notes.append("stdout still contains a tab character.")
    return False, mismatch(
        "stdout is not the detabbed text.",
        got=result,
        wanted=expected,
        tabstop=DEFAULT,
        notes=notes,
    )


def _space_run_ok(output, stops):
    col = 0
    i = 0
    n = len(output)
    while i < n:
        ch = output[i]
        if ch == "\n":
            col = 0
            i += 1
            continue
        if ch == "\t":
            col = next_stop(col, stops)
            i += 1
            continue
        if ch != " ":
            col += 1
            i += 1
            continue
        start = col
        j = i
        while j < n and output[j] == " ":
            j += 1
            col += 1
        run = j - i
        dist = next_stop(start, stops) - start
        if dist >= 2 and run >= dist:
            return (
                False,
                "output still has a run of spaces that a tab could replace "
                "(same appearance, fewer characters)",
            )
        i = j
    return True, ""


def check_entab(original, result, stops):
    expanded_in = expand(original, stops)
    expanded_out = expand(result, stops)
    where = describe(stops) + "."
    if expanded_in != expanded_out:
        return False, mismatch(
            "displayed text does not match.",
            got=expanded_out,
            wanted=expanded_in,
            tabstop=DEFAULT,
            notes=[
                where,
                "tabs and spaces must land on the same columns as the input.",
                "a newline resets the column.",
            ],
        )
    ok, msg = _space_run_ok(result, stops)
    if not ok:
        return False, msg + " " + where
    return True, ""
