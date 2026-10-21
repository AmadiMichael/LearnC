"""Source checks for the recursive itoa (4-12) and reverse (4-13)."""

from check_getop import function_bodies
from pretty import mismatch

_PRINTS = {"printf", "putchar", "puts", "sprintf", "snprintf", "fprintf"}


def _callees(tokens):
    names = []
    for i, (kind, val) in enumerate(tokens):
        if kind == "ident" and i + 1 < len(tokens) and tokens[i + 1] == ("punct", "("):
            names.append(val)
    return names


def _has_recursion(start, bodies):
    def walk(name, stack):
        if name in stack:
            return True
        if name not in bodies:
            return False
        stack.append(name)
        for callee in _callees(bodies[name]):
            if walk(callee, stack):
                return True
        stack.pop()
        return False

    return walk(start, [])


def _calls_print(start, bodies):
    seen = set()

    def walk(name):
        if name in seen or name not in bodies:
            return False
        seen.add(name)
        for callee in _callees(bodies[name]):
            if callee in _PRINTS or walk(callee):
                return True
        return False

    return walk(start)


def _check_recursive(src, name, job):
    bodies, _duplicate = function_bodies(src)
    if name not in bodies:
        return False, "the exercise asks for a function named {}.".format(name)
    if not _has_recursion(name, bodies):
        return False, "{} must do its work by calling a recursive routine.".format(name)
    if _calls_print(name, bodies):
        return False, job
    return True, ""


def check_itoa_source(src):
    return _check_recursive(
        src,
        "itoa",
        "itoa writes the digits into s. Print s from main.",
    )


def check_reverse_source(src):
    return _check_recursive(
        src,
        "reverse",
        "reverse s in place. Print s from main.",
    )


def check(got, wanted):
    if got == wanted:
        return True, ""
    return False, mismatch(
        "stdout is not the reversed string.",
        got=got,
        wanted=wanted,
        tabstop=8,
        notes=[
            "the newline that ends stdin is not part of s.",
            "print the reversed characters, then a newline.",
        ],
    )
