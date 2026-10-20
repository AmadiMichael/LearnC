#!/usr/bin/env python3
"""Compile and run K&R chapter 1–4 programs against the tests."""

import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BIN = os.path.join(ROOT, "bin")
TESTS = os.path.join(ROOT, "tests", "chapter1")
TESTS_CH2 = os.path.join(ROOT, "tests", "chapter2")
TESTS_CH3 = os.path.join(ROOT, "tests", "chapter3")
TESTS_CH4 = os.path.join(ROOT, "tests", "chapter4")
HELPERS = os.path.join(ROOT, "tests", "helpers")

TABSTOP = 8
FOLD_COL = 20
GETLINE_LIM = 8
TIMEOUT = 5

sys.path.insert(0, HELPERS)
from check_detab import check as check_detab  # noqa: E402
from check_entab import check as check_entab  # noqa: E402
from check_fold import check_golden, check_long_word  # noqa: E402
from check_and_or import check as check_and_or  # noqa: E402
from check_getline import check as check_getline  # noqa: E402
from check_htoi import check as check_htoi  # noqa: E402
from check_squeeze import check as check_squeeze  # noqa: E402
from check_any import check as check_any  # noqa: E402
from check_bits import check as check_bits  # noqa: E402
from check_bitcount import check as check_bitcount  # noqa: E402
from check_lower import check as check_lower  # noqa: E402
from check_lower import check_source as check_lower_source  # noqa: E402
from check_binsearch import check as check_binsearch
from check_escape import check as check_escape
from check_escape import check_source as check_escape_source  # noqa: E402
from check_expand import check as check_expand
from check_expand import check_source as check_expand_source  # noqa: E402
from check_itoa import check as check_itoa
from check_itoa import check_source as check_itoa_source  # noqa: E402
from check_itob import check as check_itob
from check_itob import check_source as check_itob_source  # noqa: E402
from check_itob import format_base as format_itob  # noqa: E402
from check_itoaw import check as check_itoaw
from check_itoaw import check_source as check_itoaw_source  # noqa: E402
from check_itoaw import format_padded as format_itoaw  # noqa: E402
from check_strindex import check as check_strindex
from check_strindex import check_source as check_strindex_source  # noqa: E402
from check_atof import check as check_atof
from check_atof import check_source as check_atof_source  # noqa: E402
from check_calc import check as check_calc
from check_ungets import check as check_ungets
from check_ungets import check_source as check_ungets_source  # noqa: E402
from check_getch import check as check_getch
from check_getch import check_source_getch as check_getch_source  # noqa: E402
from check_getch import check_source_getline as check_getline_source  # noqa: E402
from check_ranges import (  # noqa: E402
    FLOAT_TYPES,
    INTEGER_TYPES,
    check_floats,
    check_integers,
    load_expected,
    normalize_type,
    parse_output,
)


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


def compile_prog(src_name, bin_name, chapter="chapter1", defines=None):
    src = os.path.join(ROOT, "src", chapter, src_name)
    out = os.path.join(BIN, bin_name)
    if not os.path.isfile(src):
        extra = (
            " (stdin to stdout)"
            if chapter == "chapter1" or src_name in (
                "getline.c",
                "htoi.c",
                "squeeze.c",
                "any.c",
                "setbits.c",
                "invert.c",
                "rightrot.c",
                "bitcount.c",
                "lower.c",
                "binsearch.c",
                "escape.c",
                "expand.c",
                "itoa.c",
                "itob.c",
                "itoaw.c",
                "strindex.c",
                "atof.c",
                "calc.c",
                "ungets.c",
                "getch1.c",
                "getcheof.c",
                "calcline.c",
            )
            else ""
        )
        return None, "missing {} — write your program there{}".format(
            os.path.relpath(src, ROOT),
            extra,
        )
    os.makedirs(BIN, exist_ok=True)
    cmd = [
        "gcc",
        "-std=c99",
        "-Wall",
        "-Wextra",
    ]
    if chapter == "chapter1":
        cmd.extend(
            [
                "-DTABSTOP={}".format(TABSTOP),
                "-DFOLD_COL={}".format(FOLD_COL),
            ]
        )
    if defines:
        for name, value in defines.items():
            cmd.append("-D{}={}".format(name, value))
    cmd.extend([src, "-o", out])
    if src_name in ("atof.c", "calc.c", "calcline.c"):
        cmd.append("-lm")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        return None, "compile failed:\n{}".format(err)
    return out, ""


def run_bin(binary, stdin_data, extra_args=None):
    args = [binary]
    if extra_args:
        args.extend(extra_args)
    try:
        proc = subprocess.run(
            args,
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


def read(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def list_files(subdir, suffix):
    folder = os.path.join(TESTS, subdir)
    names = sorted(n for n in os.listdir(folder) if n.endswith(suffix))
    return [os.path.join(folder, n) for n in names]


def test_detab():
    print("\n== 1-20 detab  (tab stops every {} columns) ==".format(TABSTOP))
    binary, msg = compile_prog("detab.c", "detab")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    passed = failed = 0
    for path in list_files("1-20", ".in"):
        name = os.path.basename(path)
        data = read(path)
        rc, out, err, run_err = run_bin(binary, data)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_detab(data, out, TABSTOP)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def test_entab():
    print("\n== 1-21 entab  (tab stops every {} columns) ==".format(TABSTOP))
    binary, msg = compile_prog("entab.c", "entab")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    passed = failed = 0
    for path in list_files("1-21", ".in"):
        name = os.path.basename(path)
        data = read(path)
        rc, out, err, run_err = run_bin(binary, data)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_entab(data, out, TABSTOP)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def test_fold():
    print("\n== 1-22 fold  (column {}) ==".format(FOLD_COL))
    binary, msg = compile_prog("fold.c", "fold")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    passed = failed = 0
    folder = os.path.join(TESTS, "1-22")
    cases = sorted(
        n[: -len(".in")]
        for n in os.listdir(folder)
        if n.endswith(".in")
    )
    for case in cases:
        name = case
        inp = read(os.path.join(folder, case + ".in"))
        golden_path = os.path.join(folder, case + ".out")
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        if os.path.isfile(golden_path):
            ok, detail = check_golden(out, read(golden_path))
        else:
            ok, detail = check_long_word(inp, out, FOLD_COL, TABSTOP)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def _lines(path):
    if not os.path.isfile(path):
        return []
    return [ln.rstrip("\n") for ln in read(path).splitlines() if ln.strip()]


def test_uncomment():
    print("\n== 1-23 uncomment ==")
    binary, msg = compile_prog("uncomment.c", "uncomment")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    passed = failed = 0
    folder = os.path.join(TESTS, "1-23")
    cases = sorted(
        n[: -len(".in.c")]
        for n in os.listdir(folder)
        if n.endswith(".in.c")
    )
    for case in cases:
        inp = read(os.path.join(folder, case + ".in.c"))
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, case, run_err)
            continue
        if rc != 0:
            failed += not say(False, case, "exit {} stderr={!r}".format(rc, err))
            continue
        missing = [s for s in _lines(os.path.join(folder, case + ".keep")) if s not in out]
        present = [s for s in _lines(os.path.join(folder, case + ".drop")) if s in out]
        if missing or present:
            bits = []
            if missing:
                bits.append("missing required text:")
                bits.extend("  • {!r}".format(s) for s in missing)
            if present:
                bits.append("still contains text that should be gone:")
                bits.extend("  • {!r}".format(s) for s in present)
            failed += not say(False, case, "\n".join(bits))
        else:
            passed += say(True, case)
    return passed, failed


def test_syntaxcheck():
    print("\n== 1-24 syntaxcheck ==")
    binary, msg = compile_prog("syntaxcheck.c", "syntaxcheck")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    passed = failed = 0
    folder = os.path.join(TESTS, "1-24")
    files = sorted(n for n in os.listdir(folder) if n.endswith(".c"))
    for name in files:
        path = os.path.join(folder, name)
        expect_ok = name.startswith("ok-")
        rc, out, err, run_err = run_bin(binary, read(path))
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if expect_ok:
            if rc == 0:
                passed += say(True, name)
            else:
                failed += not say(
                    False,
                    name,
                    "expected exit 0, got {}\nstdout:\n{}\nstderr:\n{}".format(
                        rc,
                        out if out else "(empty)",
                        err if err else "(empty)",
                    ),
                )
        else:
            if rc != 0:
                passed += say(True, name)
            else:
                failed += not say(
                    False,
                    name,
                    "expected a non-zero exit (an error), got 0",
                )
    return passed, failed


def _range_case(path):
    source = None
    types = []
    for line in read(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if source is None:
            source = line.lower()
            continue
        typ = normalize_type(line)
        if typ:
            types.append(typ)
    return source, types


def test_ranges():
    print("\n== 2-1 ranges  (header values and the same ranges by computation) ==")
    binary, msg = compile_prog("ranges.c", "ranges", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    rc, out, err, run_err = run_bin(binary, "")
    if run_err:
        say(False, "run", run_err)
        return 0, 1
    if rc != 0:
        say(False, "run", "exit {} stderr={!r}".format(rc, err))
        return 0, 1

    try:
        expected = load_expected()
    except RuntimeError as exc:
        say(False, "limits-probe", str(exc))
        return 0, 1

    found = parse_output(out)
    folder = os.path.join(TESTS_CH2, "2-1")
    passed = failed = 0
    for path in sorted(
        os.path.join(folder, n)
        for n in os.listdir(folder)
        if n.endswith(".types")
    ):
        name = os.path.basename(path)[: -len(".types")]
        source, types = _range_case(path)
        ints = [t for t in types if t in INTEGER_TYPES]
        floats = [t for t in types if t in FLOAT_TYPES]
        details = []
        ok = True
        if ints:
            i_ok, i_detail = check_integers(found, expected, source, ints)
            ok = ok and i_ok
            if i_detail:
                details.append(i_detail)
        if floats:
            f_ok, f_detail = check_floats(found, expected, source, floats)
            ok = ok and f_ok
            if f_detail:
                details.append(f_detail)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, "\n".join(details))
    return passed, failed


def _run_getline_dir(binary, folder, prefix=""):
    passed = failed = 0
    names = sorted(n for n in os.listdir(folder) if n.endswith(".in"))
    for name in names:
        case = name[: -len(".in")]
        label = prefix + case
        inp = read(os.path.join(folder, case + ".in"))
        wanted = read(os.path.join(folder, case + ".out"))
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, label, run_err)
            continue
        if rc != 0:
            failed += not say(False, label, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_getline(out, wanted)
        if ok:
            passed += say(True, label)
        else:
            failed += not say(False, label, detail)
    return passed, failed


def test_getline():
    print("\n== 2-2 getline  (book for-loop, no && or ||, LIM={}) ==".format(GETLINE_LIM))
    src = os.path.join(ROOT, "src", "chapter2", "getline.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_and_or(read(src))
        if ok:
            passed += say(True, "no-and-or")
        else:
            failed += not say(False, "no-and-or", detail)
    else:
        say(False, "compile", "missing src/chapter2/getline.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog(
        "getline.c", "getline", chapter="chapter2", defines={"LIM": GETLINE_LIM}
    )
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1

    folder = os.path.join(TESTS_CH2, "2-2")
    p, f = _run_getline_dir(binary, folder)
    passed += p
    failed += f

    extra = [("lim-1", 1), ("lim-2", 2)]
    for sub, lim in extra:
        extra_bin, extra_msg = compile_prog(
            "getline.c",
            "getline-{}".format(sub),
            chapter="chapter2",
            defines={"LIM": lim},
        )
        if extra_bin is None:
            failed += not say(False, "compile-{}".format(sub), extra_msg)
            continue
        p, f = _run_getline_dir(
            extra_bin, os.path.join(folder, sub), prefix="{}:".format(sub)
        )
        passed += p
        failed += f
    return passed, failed


def test_htoi():
    print("\n== 2-3 htoi  (hex string to decimal integer) ==")
    binary, msg = compile_prog("htoi.c", "htoi", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1

    folder = os.path.join(TESTS_CH2, "2-3")
    return _run_inout_dir(binary, folder, check_htoi)


def _run_inout_dir(binary, folder, check_fn):
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


def test_squeeze():
    print("\n== 2-4 squeeze  (delete from s1 every character that occurs in s2) ==")
    binary, msg = compile_prog("squeeze.c", "squeeze", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-4"), check_squeeze)


def test_any():
    print("\n== 2-5 any  (first location in s1 of a character from s2) ==")
    binary, msg = compile_prog("any.c", "any", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-5"), check_any)


def test_setbits():
    print("\n== 2-6 setbits  (copy n bits of y into x at position p) ==")
    binary, msg = compile_prog("setbits.c", "setbits", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-6"), check_bits)


def test_invert():
    print("\n== 2-7 invert  (flip n bits of x beginning at position p) ==")
    binary, msg = compile_prog("invert.c", "invert", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-7"), check_bits)


def test_rightrot():
    print("\n== 2-8 rightrot  (rotate unsigned x right by n bits) ==")
    binary, msg = compile_prog("rightrot.c", "rightrot", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-8"), check_bits)


def test_bitcount():
    print("\n== 2-9 bitcount  (number of 1-bits in unsigned x) ==")
    binary, msg = compile_prog("bitcount.c", "bitcount", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-9"), check_bitcount)


def test_lower():
    print("\n== 2-10 lower  (A-Z to a-z with ?: instead of if-else) ==")
    src = os.path.join(ROOT, "src", "chapter2", "lower.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_lower_source(read(src))
        if ok:
            passed += say(True, "uses-conditional")
        else:
            failed += not say(False, "uses-conditional", detail)
    else:
        say(False, "compile", "missing src/chapter2/lower.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("lower.c", "lower", chapter="chapter2")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH2, "2-10"), check_lower)
    return passed + p, failed + f


def test_binsearch():
    print("\n== 3-1 binsearch  (find x in a sorted array; one test in the loop) ==")
    binary, msg = compile_prog("binsearch.c", "binsearch", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return 0, 1
    return _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-1"), check_binsearch)


def test_escape():
    print("\n== 3-2 escape  (visible \\t / \\n and back; use a switch) ==")
    src = os.path.join(ROOT, "src", "chapter3", "escape.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_escape_source(read(src))
        if ok:
            passed += say(True, "uses-switch")
        else:
            failed += not say(False, "uses-switch", detail)
    else:
        say(False, "compile", "missing src/chapter3/escape.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("escape.c", "escape", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-2"), check_escape)
    return passed + p, failed + f


def test_expand():
    print("\n== 3-3 expand  (a-z, A-Z, 0-9 shorthand into the full list) ==")
    src = os.path.join(ROOT, "src", "chapter3", "expand.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_expand_source(read(src))
        if ok:
            passed += say(True, "has-expand")
        else:
            failed += not say(False, "has-expand", detail)
    else:
        say(False, "compile", "missing src/chapter3/expand.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("expand.c", "expand", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-3"), check_expand)
    return passed + p, failed + f


def test_itoa():
    print("\n== 3-4 itoa  (int to digits; must work for the most negative int) ==")
    src = os.path.join(ROOT, "src", "chapter3", "itoa.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_itoa_source(read(src))
        if ok:
            passed += say(True, "has-itoa")
        else:
            failed += not say(False, "has-itoa", detail)
    else:
        say(False, "compile", "missing src/chapter3/itoa.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("itoa.c", "itoa", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1

    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-4"), check_itoa)
    passed += p
    failed += f

    try:
        expected = load_expected()
    except RuntimeError as exc:
        failed += not say(False, "limits-probe", str(exc))
        return passed, failed
    lo, hi = expected["int"]["int"]
    extras = (
        ("int-min", lo),
        ("int-max", hi),
        ("int-min-plus-one", lo + 1),
        ("int-max-minus-one", hi - 1),
    )
    for name, n in extras:
        inp = "{}\n".format(n)
        wanted = "{}\n".format(n)
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_itoa(out, wanted)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def test_itob():
    print("\n== 3-5 itob  (int to digits in base b; hex uses a-f) ==")
    src = os.path.join(ROOT, "src", "chapter3", "itob.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_itob_source(read(src))
        if ok:
            passed += say(True, "has-itob")
        else:
            failed += not say(False, "has-itob", detail)
    else:
        say(False, "compile", "missing src/chapter3/itob.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("itob.c", "itob", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1

    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-5"), check_itob)
    passed += p
    failed += f

    try:
        expected = load_expected()
    except RuntimeError as exc:
        failed += not say(False, "limits-probe", str(exc))
        return passed, failed
    lo, hi = expected["int"]["int"]
    extras = (
        ("int-min-10", lo, 10),
        ("int-max-10", hi, 10),
        ("int-min-16", lo, 16),
        ("int-max-16", hi, 16),
        ("int-min-2", lo, 2),
        ("int-max-2", hi, 2),
    )
    for name, n, b in extras:
        inp = "{}\n{}\n".format(n, b)
        wanted = "{}\n".format(format_itob(n, b))
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_itob(out, wanted)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def test_itoaw():
    print("\n== 3-6 itoa  (decimal digits, pad left with spaces to width w) ==")
    src = os.path.join(ROOT, "src", "chapter3", "itoaw.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_itoaw_source(read(src))
        if ok:
            passed += say(True, "has-itoa")
        else:
            failed += not say(False, "has-itoa", detail)
    else:
        say(False, "compile", "missing src/chapter3/itoaw.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("itoaw.c", "itoaw", chapter="chapter3")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1

    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH3, "3-6"), check_itoaw)
    passed += p
    failed += f

    try:
        expected = load_expected()
    except RuntimeError as exc:
        failed += not say(False, "limits-probe", str(exc))
        return passed, failed
    lo, hi = expected["int"]["int"]
    extras = (
        ("int-min-wide", lo, 16),
        ("int-min-exact", lo, len(str(lo))),
        ("int-max-wide", hi, 16),
        ("int-min-narrow", lo, 1),
    )
    for name, n, w in extras:
        inp = "{}\n{}\n".format(n, w)
        wanted = "{}\n".format(format_itoaw(n, w))
        rc, out, err, run_err = run_bin(binary, inp)
        if run_err:
            failed += not say(False, name, run_err)
            continue
        if rc != 0:
            failed += not say(False, name, "exit {} stderr={!r}".format(rc, err))
            continue
        ok, detail = check_itoaw(out, wanted)
        if ok:
            passed += say(True, name)
        else:
            failed += not say(False, name, detail)
    return passed, failed


def test_strindex():
    print("\n== 4-1 strindex  (rightmost occurrence of t in s) ==")
    src = os.path.join(ROOT, "src", "chapter4", "strindex.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_strindex_source(read(src))
        if ok:
            passed += say(True, "has-strindex")
        else:
            failed += not say(False, "has-strindex", detail)
    else:
        say(False, "compile", "missing src/chapter4/strindex.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("strindex.c", "strindex", chapter="chapter4")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH4, "4-1"), check_strindex)
    return passed + p, failed + f


def test_atof():
    print("\n== 4-2 atof  (string to double; handle e / E exponents) ==")
    src = os.path.join(ROOT, "src", "chapter4", "atof.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_atof_source(read(src))
        if ok:
            passed += say(True, "has-atof")
        else:
            failed += not say(False, "has-atof", detail)
    else:
        say(False, "compile", "missing src/chapter4/atof.c — write your program there (stdin to stdout)")
        return 0, 1

    binary, msg = compile_prog("atof.c", "atof", chapter="chapter4")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH4, "4-2"), check_atof)
    return passed + p, failed + f


def _named_c(src_name, bin_name, folder, check_fn, source_fn=None, source_label=None):
    src = os.path.join(ROOT, "src", "chapter4", src_name)
    passed = failed = 0
    if source_fn is not None:
        if os.path.isfile(src):
            ok, detail = source_fn(read(src))
            if ok:
                passed += say(True, source_label)
            else:
                failed += not say(False, source_label, detail)
        else:
            say(False, "compile", "missing src/chapter4/{} — write your program there (stdin to stdout)".format(src_name))
            return 0, 1
    binary, msg = compile_prog(src_name, bin_name, chapter="chapter4")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, folder, check_fn)
    return passed + p, failed + f


def test_calc():
    print("\n== 4-3 calc  (RPN: + - * / % and negative numbers) ==")
    return _named_c("calc.c", "calc", os.path.join(TESTS_CH4, "4-3"), check_calc)


def test_calcstack():
    print("\n== 4-4 calc  (P peek, D dup, S swap, C clear) ==")
    return _named_c("calc.c", "calc", os.path.join(TESTS_CH4, "4-4"), check_calc)


def test_calcmath():
    print("\n== 4-5 calc  (sin, exp, pow from math.h) ==")
    return _named_c("calc.c", "calc", os.path.join(TESTS_CH4, "4-5"), check_calc)


def test_calcvar():
    print("\n== 4-6 calc  (a-z variables, = assign, _ last printed) ==")
    return _named_c("calc.c", "calc", os.path.join(TESTS_CH4, "4-6"), check_calc)


def test_ungets():
    print("\n== 4-7 ungets  (push a string back for getch) ==")
    return _named_c(
        "ungets.c",
        "ungets",
        os.path.join(TESTS_CH4, "4-7"),
        check_ungets,
        check_ungets_source,
        "has-ungets",
    )


def test_getch1():
    print("\n== 4-8 getch  (at most one character of pushback) ==")
    return _named_c(
        "getch1.c",
        "getch1",
        os.path.join(TESTS_CH4, "4-8"),
        check_getch,
        check_getch_source,
        "has-getch",
    )


def test_getcheof():
    print("\n== 4-9 getch  (pushed-back EOF stays EOF) ==")
    return _named_c(
        "getcheof.c",
        "getcheof",
        os.path.join(TESTS_CH4, "4-9"),
        check_getch,
        check_getch_source,
        "has-getch",
    )


def test_calcline():
    print("\n== 4-10 calc  (same RPN, read lines with getline; no getch) ==")
    src = os.path.join(ROOT, "src", "chapter4", "calcline.c")
    passed = failed = 0
    if os.path.isfile(src):
        ok, detail = check_getline_source(read(src))
        if ok:
            passed += say(True, "has-getline")
        else:
            failed += not say(False, "has-getline", detail)
    else:
        say(False, "compile", "missing src/chapter4/calcline.c — write your program there (stdin to stdout)")
        return 0, 1
    binary, msg = compile_prog("calcline.c", "calcline", chapter="chapter4")
    if binary is None:
        say(False, "compile", msg)
        return passed, failed + 1
    p, f = _run_inout_dir(binary, os.path.join(TESTS_CH4, "4-3"), check_calc)
    return passed + p, failed + f


def main():
    known = {
        "20", "21", "22", "23", "24",
        "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7", "2-8", "2-9", "2-10",
        "3-1", "3-2", "3-3", "3-4", "3-5", "3-6",
        "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7", "4-8", "4-9", "4-10",
    }
    want = set(sys.argv[1:]) if len(sys.argv) > 1 else set(known)
    unknown = want - known
    if unknown:
        print(
            "Unknown exercise(s): {}. Use 20 21 22 23 24 2-1 2-2 2-3 2-4 2-5 2-6 2-7 2-8 2-9 2-10 3-1 3-2 3-3 3-4 3-5 3-6 4-1 4-2 4-3 4-4 4-5 4-6 4-7 4-8 4-9 4-10.".format(
                ", ".join(sorted(unknown))
            )
        )
        return 2

    print("Interface")
    if want & {"20", "21", "22", "23", "24"}:
        print("  src/chapter1/detab.c        stdin -> stdout")
        print("  src/chapter1/entab.c        stdin -> stdout")
        print("  src/chapter1/fold.c         stdin -> stdout")
        print("  src/chapter1/uncomment.c    stdin -> stdout")
        print("  src/chapter1/syntaxcheck.c  stdin -> stdout/stderr; exit 0 if clean, else non-zero")
        print("  tab stops: {} columns    fold column: {}".format(TABSTOP, FOLD_COL))
    if "2-1" in want:
        print("  src/chapter2/ranges.c       no stdin; stdout, one range per line:")
        print("      header    TYPE  MIN  MAX")
        print("      computed  TYPE  MIN  MAX")
        print("    integer TYPE:  signed_char unsigned_char short unsigned_short")
        print("                   int unsigned_int long unsigned_long")
        print("    float TYPE:    float double long_double")
        print("    float MIN: most-negative finite, or the smallest positive (header MIN)")
    if "2-2" in want:
        print("  src/chapter2/getline.c      stdin -> stdout, one pass of the book's for-loop")
        print("    store at most LIM-1 characters; stop at newline or EOF (do not store them)")
        print("    print only the stored characters — no extra newline, no prompts")
        print("    do not use && or ||  (LIM={} by default; also compiled as 1 and 2)".format(GETLINE_LIM))
    if "2-3" in want:
        print("  src/chapter2/htoi.c         stdin -> stdout")
        print("    one hex string on stdin (optional 0x or 0X; digits 0-9 a-f A-F)")
        print("    print that value as a decimal integer, then a newline; no prompts")
    if "2-4" in want:
        print("  src/chapter2/squeeze.c      stdin -> stdout")
        print("    line 1 is s1, line 2 is s2 (newlines are not part of the strings)")
        print("    print s1 with every character that occurs in s2 deleted, then a newline")
    if "2-5" in want:
        print("  src/chapter2/any.c          stdin -> stdout")
        print("    line 1 is s1, line 2 is s2 (newlines are not part of the strings)")
        print("    print the first 0-based index in s1 of any character from s2, or -1")
    if "2-6" in want:
        print("  src/chapter2/setbits.c      stdin -> stdout")
        print("    lines: x, p, n, y  (decimal). print unsigned result, then a newline")
        print("    same bit positions as getbits: p counts from the right, 0 is the low bit")
    if "2-7" in want:
        print("  src/chapter2/invert.c       stdin -> stdout")
        print("    lines: x, p, n  (decimal). print unsigned result, then a newline")
        print("    same bit positions as getbits")
    if "2-8" in want:
        print("  src/chapter2/rightrot.c     stdin -> stdout")
        print("    lines: x, n  (decimal). print unsigned result, then a newline")
        print("    rotate the bits of unsigned x; unsigned is 32 bits here")
    if "2-9" in want:
        print("  src/chapter2/bitcount.c     stdin -> stdout")
        print("    one unsigned decimal x. print how many 1-bits it has, then a newline")
    if "2-10" in want:
        print("  src/chapter2/lower.c        stdin -> stdout")
        print("    copy stdin to stdout; A-Z become a-z; everything else unchanged")
        print("    rewrite lower with ?:  (not if-else)")
    if "3-1" in want:
        print("  src/chapter3/binsearch.c    stdin -> stdout")
        print("    lines: x, n, then n sorted ints (increasing). print 0-based index or -1")
    if "3-2" in want:
        print("  src/chapter3/escape.c       stdin -> stdout")
        print("    line 1 is the word escape or unescape (that newline is not part of t)")
        print("    the rest of stdin is the string t")
        print("    print only the converted string s — no extra newline, no prompts")
        print("    escape:   a real tab becomes the two characters \\t; a real newline becomes \\n")
        print("    unescape: those two-character sequences become a real tab or newline")
        print("    copy every other character as it is; use a switch")
    if "3-3" in want:
        print("  src/chapter3/expand.c       stdin -> stdout")
        print("    stdin is one line, s1 (that newline is not part of s1; spaces are)")
        print("    print the expanded s2, then a newline; no prompts")
        print("    a-z, A-Z, and 0-9 become every character from the left end through the right")
        print("    both ends must be the same kind, and the left end must not come after the right")
        print("    a-b-c is abc; a leading or trailing - is copied; so is a - that is not a range")
        print("    write a function expand(s1, s2)")
    if "3-4" in want:
        print("  src/chapter3/itoa.c        stdin -> stdout")
        print("    one signed decimal integer n")
        print("    print n as decimal digits (leading - if n is negative), then a newline")
        print("    write a function itoa(n, s); do not call sprintf")
        print("    must work for the most negative int — the book's n = -n does not")
    if "3-5" in want:
        print("  src/chapter3/itob.c        stdin -> stdout")
        print("    lines: n, b  (decimal). n is a signed int; b is the base, 2 through 16")
        print("    print n in base b (leading - if n is negative), then a newline")
        print("    digits 0-9 then a-f for 10-15 (lowercase); no 0x prefix")
        print("    write a function itob(n, s, b); do not call sprintf")
        print("    must work for the most negative int, same as itoa")
    if "3-6" in want:
        print("  src/chapter3/itoaw.c       stdin -> stdout")
        print("    lines: n, w  (decimal). n is a signed int; w is the minimum field width")
        print("    print n as decimal digits, padded with spaces on the left to at least w")
        print("    if the number is already wider than w, print it in full — do not truncate")
        print("    the minus sign counts toward the width; spaces go to the left of it")
        print("    then a newline; no prompts; write itoa(n, s, w); do not call sprintf")
    if "4-1" in want:
        print("  src/chapter4/strindex.c    stdin -> stdout")
        print("    line 1 is s, line 2 is t (newlines are not part of the strings; spaces are)")
        print("    print the 0-based index of the rightmost occurrence of t in s, or -1")
        print("    write a function strindex(s, t); do not call strstr")
    if "4-2" in want:
        print("  src/chapter4/atof.c        stdin -> stdout")
        print("    one number on a line (optional leading spaces, optional + or -)")
        print("    digits, optional fraction, then optional e or E and an optionally signed exponent")
        print("    print that value as a floating-point number, then a newline (%.8g is enough)")
        print("    write a function atof(s) that returns double; do not call the library atof / strtod")
    if "4-3" in want:
        print("  src/chapter4/calc.c        stdin -> stdout  (grow this file for 4-4, 4-5, 4-6)")
        print("    reverse Polish: whitespace-separated tokens, then a newline")
        print("    newline pops and prints the top of the stack (%.8g; a leading tab is fine)")
        print("    operators + - * / %   (2 4 / is 0.5; 7 3 % is 1)")
        print("    a number may start with -: token -2 is negative two; token - by itself is subtract")
        print("    do not pop an empty stack in these tests")
    if "4-4" in want:
        print("  src/chapter4/calc.c        same calculator, extra commands (uppercase, one letter):")
        print("    P  print the top without popping")
        print("    D  duplicate the top")
        print("    S  swap the top two")
        print("    C  clear the stack")
    if "4-5" in want:
        print("  src/chapter4/calc.c        same calculator, extra word commands (math.h is allowed):")
        print("    sin  exp  each pop one argument")
        print("    pow  x y pow means x to the power y  (2 3 pow is 8)")
    if "4-6" in want:
        print("  src/chapter4/calc.c        same calculator, variables:")
        print("    a single letter a-z pushes that variable (starts at 0)")
        print("    =  pops the copy pushed by the name, stores the next value into the most")
        print("       recently named variable, and leaves that value on the stack")
        print("       example: 3 a =   stores 3 in a and leaves 3 on the stack")
        print("    _  pushes the most recently printed value (from newline or P)")
    if "4-7" in want:
        print("  src/chapter4/ungets.c      stdin -> stdout")
        print("    read stdin into a string s, ungets(s), then copy getch() to stdout until EOF")
        print("    output should match the input; write ungets (it may call ungetch)")
    if "4-8" in want:
        print("  src/chapter4/getch1.c      stdin -> stdout")
        print("    copy stdin to stdout using getch/ungetch; only one character of pushback")
        print("    output should match the input")
    if "4-9" in want:
        print("  src/chapter4/getcheof.c    stdin -> stdout")
        print("    copy stdin to stdout with getch; ungetch(EOF) must still yield EOF from getch")
        print("    output should match the input; the program must stop (not loop on EOF)")
        print("    store the pushback in an int, not a char")
    if "4-10" in want:
        print("  src/chapter4/calcline.c    stdin -> stdout")
        print("    same RPN as 4-3, but read a whole line with getline (no getch/ungetch)")
        print("    same print rule: newline / end of line prints the top with %.8g")

    passed = failed = 0
    runners = [
        ("20", test_detab),
        ("21", test_entab),
        ("22", test_fold),
        ("23", test_uncomment),
        ("24", test_syntaxcheck),
        ("2-1", test_ranges),
        ("2-2", test_getline),
        ("2-3", test_htoi),
        ("2-4", test_squeeze),
        ("2-5", test_any),
        ("2-6", test_setbits),
        ("2-7", test_invert),
        ("2-8", test_rightrot),
        ("2-9", test_bitcount),
        ("2-10", test_lower),
        ("3-1", test_binsearch),
        ("3-2", test_escape),
        ("3-3", test_expand),
        ("3-4", test_itoa),
        ("3-5", test_itob),
        ("3-6", test_itoaw),
        ("4-1", test_strindex),
        ("4-2", test_atof),
        ("4-3", test_calc),
        ("4-4", test_calcstack),
        ("4-5", test_calcmath),
        ("4-6", test_calcvar),
        ("4-7", test_ungets),
        ("4-8", test_getch1),
        ("4-9", test_getcheof),
        ("4-10", test_calcline),
    ]
    for key, fn in runners:
        if key in want:
            p, f = fn()
            passed += p
            failed += f

    print("\n{} passed, {} failed".format(passed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
