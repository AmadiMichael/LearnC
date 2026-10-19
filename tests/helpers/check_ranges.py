"""Check 2-1 range output against this machine's limits.h / float.h values."""

import math
import os
import subprocess
import tempfile

INTEGER_TYPES = (
    "signed_char",
    "unsigned_char",
    "short",
    "unsigned_short",
    "int",
    "unsigned_int",
    "long",
    "unsigned_long",
)

FLOAT_TYPES = ("float", "double", "long_double")

SOURCES = ("header", "computed")

TYPE_ALIASES = {
    "signed_char": "signed_char",
    "signed char": "signed_char",
    "schar": "signed_char",
    "unsigned_char": "unsigned_char",
    "unsigned char": "unsigned_char",
    "uchar": "unsigned_char",
    "short": "short",
    "signed_short": "short",
    "signed short": "short",
    "short int": "short",
    "signed short int": "short",
    "unsigned_short": "unsigned_short",
    "unsigned short": "unsigned_short",
    "unsigned short int": "unsigned_short",
    "int": "int",
    "signed_int": "int",
    "signed int": "int",
    "unsigned_int": "unsigned_int",
    "unsigned int": "unsigned_int",
    "uint": "unsigned_int",
    "long": "long",
    "signed_long": "long",
    "signed long": "long",
    "long int": "long",
    "signed long int": "long",
    "unsigned_long": "unsigned_long",
    "unsigned long": "unsigned_long",
    "unsigned long int": "unsigned_long",
    "float": "float",
    "double": "double",
    "long_double": "long_double",
    "long double": "long_double",
}

SOURCE_ALIASES = {
    "header": "header",
    "headers": "header",
    "computed": "computed",
    "computation": "computed",
    "compute": "computed",
}

_PROBE_C = r"""
#include <stdio.h>
#include <limits.h>
#include <float.h>

int main(void)
{
    printf("signed_char %d %d\n", (int)SCHAR_MIN, (int)SCHAR_MAX);
    printf("unsigned_char %u %u\n", 0u, (unsigned)UCHAR_MAX);
    printf("short %d %d\n", (int)SHRT_MIN, (int)SHRT_MAX);
    printf("unsigned_short %u %u\n", 0u, (unsigned)USHRT_MAX);
    printf("int %d %d\n", INT_MIN, INT_MAX);
    printf("unsigned_int %u %u\n", 0u, UINT_MAX);
    printf("long %ld %ld\n", LONG_MIN, LONG_MAX);
    printf("unsigned_long %lu %lu\n", 0UL, ULONG_MAX);
    printf("float_max %.12e\n", (double)FLT_MAX);
    printf("float_min_pos %.12e\n", (double)FLT_MIN);
    printf("double_max %.16e\n", DBL_MAX);
    printf("double_min_pos %.16e\n", DBL_MIN);
    printf("long_double_max %.18Le\n", LDBL_MAX);
    printf("long_double_min_pos %.18Le\n", LDBL_MIN);
    return 0;
}
"""

_expected_cache = None


def _strip_suffix(token):
    t = token.strip().rstrip(",")
    while t and t[-1] in "uUlLfF":
        head = t[:-1]
        if not head or head in "+-":
            break
        t = head
    return t


def parse_number(token):
    t = _strip_suffix(token)
    if not t:
        return None
    try:
        if t.lower().startswith(("0x", "-0x", "+0x")):
            return int(t, 16)
        if any(c in t.lower() for c in ".e"):
            return float(t)
        return int(t, 10)
    except ValueError:
        try:
            return float(t)
        except ValueError:
            return None


def normalize_type(name):
    return TYPE_ALIASES.get(" ".join(name.lower().split()))


def parse_output(text):
    """
    Lines: SOURCE TYPE MIN MAX
    Extra lines are ignored. Returns dict[source][type] = (min, max).
    """
    found = {src: {} for src in SOURCES}
    for raw in text.splitlines():
        parts = raw.split()
        if len(parts) < 4:
            continue
        source = SOURCE_ALIASES.get(parts[0].lower().rstrip(":"))
        if source is None:
            continue
        lo = parse_number(parts[-2])
        hi = parse_number(parts[-1])
        if lo is None or hi is None:
            continue
        typ = normalize_type(" ".join(parts[1:-2]))
        if typ is None:
            continue
        found[source][typ] = (lo, hi)
    return found


def _as_int(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _close(got, wanted):
    if wanted == 0:
        return math.isclose(got, wanted, abs_tol=1e-12)
    return math.isclose(got, wanted, rel_tol=1e-5, abs_tol=0.0)


def load_expected(gcc="gcc"):
    global _expected_cache
    if _expected_cache is not None:
        return _expected_cache

    tmp = tempfile.mkdtemp(prefix="learnc-2-1-")
    src = os.path.join(tmp, "probe.c")
    out = os.path.join(tmp, "probe")
    with open(src, "w", encoding="utf-8") as f:
        f.write(_PROBE_C)
    proc = subprocess.run(
        [gcc, "-std=c99", src, "-o", out],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError("failed to build limits probe:\n{}".format(err))
    run = subprocess.run(
        [out],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    expected = {"int": {}, "float": {}}
    for line in run.stdout.decode("utf-8").splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[0] in INTEGER_TYPES:
            expected["int"][parts[0]] = (int(parts[1]), int(parts[2]))
        elif len(parts) == 2 and parts[0].endswith("_max"):
            key = parts[0][: -len("_max")]
            expected["float"].setdefault(key, {})["max"] = float(parts[1])
        elif len(parts) == 2 and parts[0].endswith("_min_pos"):
            key = parts[0][: -len("_min_pos")]
            expected["float"].setdefault(key, {})["min_pos"] = float(parts[1])
    _expected_cache = expected
    return expected


def _fmt(value):
    if isinstance(value, float):
        return "{:.6e}".format(value)
    return str(value)


def check_integers(found, expected, source, types=None):
    missing = []
    wrong = []
    if types is None:
        types = INTEGER_TYPES
    for typ in types:
        want_lo, want_hi = expected["int"][typ]
        if typ not in found[source]:
            missing.append(typ)
            continue
        got_lo, got_hi = found[source][typ]
        glo = _as_int(got_lo)
        ghi = _as_int(got_hi)
        if glo != want_lo or ghi != want_hi:
            wrong.append(
                "{}: wanted {} {}  got {} {}".format(
                    typ, want_lo, want_hi, _fmt(got_lo), _fmt(got_hi)
                )
            )
    bits = []
    if missing:
        bits.append("missing {} line(s) for: {}".format(source, ", ".join(missing)))
    if wrong:
        bits.append("wrong {} values:".format(source))
        bits.extend("  " + w for w in wrong)
    if bits:
        return False, "\n".join(bits)
    return True, ""


def check_floats(found, expected, source, types=None):
    missing = []
    wrong = []
    if types is None:
        types = FLOAT_TYPES
    for typ in types:
        spec = expected["float"][typ]
        if typ not in found[source]:
            missing.append(typ)
            continue
        got_lo, got_hi = found[source][typ]
        try:
            glo = float(got_lo)
            ghi = float(got_hi)
        except (TypeError, ValueError):
            wrong.append("{}: could not read min/max as floating values".format(typ))
            continue
        max_ok = _close(ghi, spec["max"])
        min_ok = _close(glo, -spec["max"]) or _close(glo, spec["min_pos"])
        if not (min_ok and max_ok):
            wrong.append(
                "{}: wanted min -{m} or {p}, max {m}  got {lo} {hi}".format(
                    typ,
                    m=_fmt(spec["max"]),
                    p=_fmt(spec["min_pos"]),
                    lo=_fmt(glo),
                    hi=_fmt(ghi),
                )
            )
    bits = []
    if missing:
        bits.append("missing {} line(s) for: {}".format(source, ", ".join(missing)))
    if wrong:
        bits.append("wrong {} values:".format(source))
        bits.extend("  " + w for w in wrong)
    if bits:
        return False, "\n".join(bits)
    return True, ""
