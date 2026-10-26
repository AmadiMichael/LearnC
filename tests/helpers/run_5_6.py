"""Exercise 5-6: pointer rewrites of the earlier routines."""

import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BIN = os.path.join(ROOT, "bin")
HELPERS = os.path.join(ROOT, "tests", "helpers")
CH5 = os.path.join(ROOT, "tests", "chapter5", "5-6")
CH3 = os.path.join(ROOT, "tests", "chapter3")
CH4 = os.path.join(ROOT, "tests", "chapter4")
SRC = os.path.join(ROOT, "src", "chapter5", "5-6")
BOOK = os.path.join(ROOT, "src", "chapter4", "4-11")

sys.path.insert(0, HELPERS)
from check_ptr import check_pointer, check_text  # noqa: E402
from check_itoa import check as check_itoa  # noqa: E402
from check_itob import check as check_itob  # noqa: E402
from check_itob import format_base as format_itob  # noqa: E402
from check_itoaw import check as check_itoaw  # noqa: E402
from check_itoaw import format_padded as format_itoaw  # noqa: E402
from check_recur import check as check_reverse  # noqa: E402
from check_getop import check as check_bookcalc  # noqa: E402
from check_ranges import load_expected  # noqa: E402

PARTS = (
    "getline",
    "atoi",
    "itoa",
    "itob",
    "itoaw",
    "reverse",
    "strindex",
    "getop",
)

TIMEOUT = 5


def say(ok, name, detail=""):
    if sys.stdout.isatty():
        tag = "\033[32mPASS\033[0m" if ok else "\033[31mFAIL\033[0m"
    else:
        tag = "PASS" if ok else "FAIL"
    print("{}  {}".format(tag, name))
    if detail:
        for line in detail.splitlines():
            print("      {}".format(line) if line else "")
    return ok


def read(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def run_bin(binary, stdin_data):
    try:
        proc = subprocess.run(
            [binary],
            input=stdin_data.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None, None, None, "program timed out after {}s".format(TIMEOUT)
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    return proc.returncode, out, err, ""


def _gcc(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        return "compile failed:\n{}".format(err)
    return ""


def compile_user(src_name, driver_name, out_name, extras=None, include_dir=None):
    src = os.path.join(SRC, src_name)
    if not os.path.isfile(src):
        return None, "missing src/chapter5/5-6/{} — write the pointer version there".format(src_name)
    os.makedirs(BIN, exist_ok=True)
    user_obj = os.path.join(BIN, out_name + "_user.o")
    out = os.path.join(BIN, out_name)
    cmd = [
        "gcc", "-std=c99", "-Wall", "-Wextra", "-fno-builtin",
        "-Dmain=student_main", "-c", src, "-o", user_obj,
    ]
    if include_dir:
        cmd[1:1] = ["-I", include_dir]
    err = _gcc(cmd)
    if err:
        return None, err
    objs = [user_obj]
    units = [os.path.join(HELPERS, driver_name)] if driver_name else []
    if extras:
        units.extend(extras)
    for i, unit in enumerate(units):
        obj = os.path.join(BIN, "{}_{}.o".format(out_name, i))
        cmd = ["gcc", "-std=c99", "-Wall", "-Wextra", "-fno-builtin", "-c", unit, "-o", obj]
        if include_dir:
            cmd[1:1] = ["-I", include_dir]
        err = _gcc(cmd)
        if err:
            return None, err
        objs.append(obj)
    err = _gcc(["gcc"] + objs + ["-o", out])
    if err:
        return None, err
    return out, ""


def _run_dir(binary, folder, check_fn):
    passed = failed = 0
    names = sorted(n for n in os.listdir(folder) if n.endswith(".in"))
    for name in names:
        case = name[: -len(".in")]
        inp = read(os.path.join(folder, case + ".in"))
        wanted = read(os.path.join(folder, case + ".out"))
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, case, run_err)
            continue
        if rc != 0:
            failed += not say(False, case, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_fn(out, wanted)
        if ok:
            passed += say(True, case)
        else:
            failed += not say(False, case, detail)
    return passed, failed


def _probe(binary, cases, check_fn):
    passed = failed = 0
    for name, inp, wanted in cases:
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_fn(out, wanted)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def _pointer(part, src_name, func, ret, missing):
    src = os.path.join(SRC, src_name)
    if not os.path.isfile(src) or os.path.getsize(src) == 0:
        return 0, 0
    ok, detail = check_pointer(read(src), func, ret, missing)
    if ok:
        return say(True, "pointers"), 0
    return 0, not say(False, "pointers", detail)


def _limits():
    try:
        return load_expected()["int"]["int"]
    except RuntimeError as exc:
        say(False, "limits-probe", str(exc))
        return None


def test_getline():
    print("\n== 5-6 getLine  (chapter 1 getline, pointers) ==")
    passed, failed = _pointer(
        "getline",
        "getline.c",
        "getLine",
        "int",
        "define int getLine(char *s, int lim). Store the line and return its length.",
    )
    binary, msg = compile_user("getline.c", "getline_driver.c", "getline56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(
        binary,
        os.path.join(CH5, "getline"),
        lambda got, wanted: check_text(
            got,
            wanted,
            "getLine did not store the line the way chapter 1 does.",
            [
                "The first line of the test input is lim. getLine reads the rest.",
                "Store at most lim-1 characters. Stop at newline or EOF.",
                "If the newline is the character that stopped the read, store it too.",
                "Write '\\0' after the stored characters and return how many were stored.",
            ],
        ),
    )
    return passed + p, failed + f


def test_atoi():
    print("\n== 5-6 atoi  (chapter 3 atoi, pointers) ==")
    passed, failed = _pointer(
        "atoi",
        "atoi.c",
        "atoi",
        "int",
        "define int atoi(char *s).",
    )
    binary, msg = compile_user("atoi.c", "atoi_driver.c", "atoi56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(
        binary,
        os.path.join(CH5, "atoi"),
        lambda got, wanted: check_text(
            got,
            wanted,
            "atoi did not convert the string.",
            [
                "Skip leading whitespace. An optional + or - follows.",
                "Then read digits. Stop at the first character that is not a digit.",
                "An empty string, a sign alone, or no digits is 0.",
            ],
        ),
    )
    return passed + p, failed + f


def test_itoa():
    print("\n== 5-6 itoa  (chapter 3 itoa, pointers) ==")
    passed, failed = _pointer(
        "itoa",
        "itoa.c",
        "itoa",
        "void",
        "define void itoa(int n, char *s).",
    )
    binary, msg = compile_user("itoa.c", "itoa_driver.c", "itoa56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(binary, os.path.join(CH3, "3-4"), check_itoa)
    passed += p
    failed += f
    limits = _limits()
    if limits is None:
        return passed, failed + 1
    lo, hi = limits
    extras = (
        ("int-min", "{}\n".format(lo), "{}\n".format(lo)),
        ("int-max", "{}\n".format(hi), "{}\n".format(hi)),
        ("int-min-plus-one", "{}\n".format(lo + 1), "{}\n".format(lo + 1)),
        ("int-max-minus-one", "{}\n".format(hi - 1), "{}\n".format(hi - 1)),
    )
    p, f = _probe(binary, extras, check_itoa)
    return passed + p, failed + f


def test_itob():
    print("\n== 5-6 itob  (chapter 3 itob, pointers) ==")
    passed, failed = _pointer(
        "itob",
        "itob.c",
        "itob",
        "void",
        "define void itob(int n, char *s, int b).",
    )
    binary, msg = compile_user("itob.c", "itob_driver.c", "itob56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(binary, os.path.join(CH3, "3-5"), check_itob)
    passed += p
    failed += f
    limits = _limits()
    if limits is None:
        return passed, failed + 1
    lo, hi = limits
    extras = []
    for name, n, b in (
        ("int-min-10", lo, 10),
        ("int-max-10", hi, 10),
        ("int-min-16", lo, 16),
        ("int-max-16", hi, 16),
        ("int-min-2", lo, 2),
        ("int-max-2", hi, 2),
    ):
        extras.append((name, "{}\n{}\n".format(n, b), "{}\n".format(format_itob(n, b))))
    p, f = _probe(binary, extras, check_itob)
    return passed + p, failed + f


def test_itoaw():
    print("\n== 5-6 itoa width  (chapter 3 itoa(n, s, w), pointers) ==")
    passed, failed = _pointer(
        "itoaw",
        "itoaw.c",
        "itoa",
        "void",
        "define void itoa(int n, char *s, int w).",
    )
    binary, msg = compile_user("itoaw.c", "itoaw_driver.c", "itoaw56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(binary, os.path.join(CH3, "3-6"), check_itoaw)
    passed += p
    failed += f
    limits = _limits()
    if limits is None:
        return passed, failed + 1
    lo, hi = limits
    extras = []
    for name, n, w in (
        ("int-min-wide", lo, 16),
        ("int-min-exact", lo, len(str(lo))),
        ("int-max-wide", hi, 16),
        ("int-min-narrow", lo, 1),
    ):
        extras.append((name, "{}\n{}\n".format(n, w), "{}\n".format(format_itoaw(n, w))))
    p, f = _probe(binary, extras, check_itoaw)
    return passed + p, failed + f


def test_reverse():
    print("\n== 5-6 reverse  (chapter 3 reverse, pointers) ==")
    passed, failed = _pointer(
        "reverse",
        "reverse.c",
        "reverse",
        "void",
        "define void reverse(char *s). Reverse s in place.",
    )
    binary, msg = compile_user("reverse.c", "reverse_driver.c", "reverse56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(binary, os.path.join(CH4, "4-13"), check_reverse)
    return passed + p, failed + f


def test_strindex():
    print("\n== 5-6 strindex  (chapter 4 strindex, first match, pointers) ==")
    passed, failed = _pointer(
        "strindex",
        "strindex.c",
        "strindex",
        "int",
        "define int strindex(char *s, char *t).",
    )
    binary, msg = compile_user("strindex.c", "strindex_driver.c", "strindex56")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(
        binary,
        os.path.join(CH5, "strindex"),
        lambda got, wanted: check_text(
            got,
            wanted,
            "strindex did not return the first position of t in s.",
            [
                "Return the index of the first occurrence of t in s, or -1.",
                "An empty t returns -1.",
            ],
        ),
    )
    return passed + p, failed + f


def test_getop():
    print("\n== 5-6 getop  (chapter 4 getop, pointers) ==")
    passed, failed = _pointer(
        "getop",
        "getop.c",
        "getop",
        "int",
        "define int getop(char *s). Include calc.h for NUMBER.",
    )
    extras = [
        os.path.join(BOOK, name)
        for name in ("main.c", "stack.c", "getch.c")
    ]
    binary, msg = compile_user(
        "getop.c",
        None,
        "getop56",
        extras=extras,
        include_dir=BOOK,
    )
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_dir(binary, os.path.join(CH4, "4-11"), check_bookcalc)
    return passed + p, failed + f


RUNNERS = {
    "getline": test_getline,
    "atoi": test_atoi,
    "itoa": test_itoa,
    "itob": test_itob,
    "itoaw": test_itoaw,
    "reverse": test_reverse,
    "strindex": test_strindex,
    "getop": test_getop,
}


def test_5_6(parts=None):
    chosen = list(parts) if parts else list(PARTS)
    passed = failed = 0
    for name in chosen:
        p, f = RUNNERS[name]()
        passed += p
        failed += f
    return passed, failed
