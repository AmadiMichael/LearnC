#include <limits.h>
#include <stdio.h>

#include "swap.h"

typedef struct {
    int n;
    double x;
} Pair;

int main(void) {
    int a = 1, b = 2;
    swap(int, a, b);
    printf("int %d %d\n", a, b);

    int c = -5, d = 0;
    swap(int, c, d);
    printf("neg %d %d\n", c, d);

    int e = 7, f = 7;
    swap(int, e, f);
    printf("same %d %d\n", e, f);

    int g = 3, h = 9;
    swap(int, g, h);
    swap(int, g, h);
    printf("twice %d %d\n", g, h);

    int arr[2] = {4, 8};
    swap(int, arr[0], arr[1]);
    printf("array %d %d\n", arr[0], arr[1]);

    int p = 1, q = 2, r = 3;
    swap(int, p, q);
    swap(int, q, r);
    printf("chain %d %d %d\n", p, q, r);

    char ca = 'A', cb = 'Z';
    swap(char, ca, cb);
    printf("char %c %c\n", ca, cb);

    double da = 1.25, db = -3.5;
    swap(double, da, db);
    printf("double %.8g %.8g\n", da, db);

    float fa = 0.5f, fb = 8.0f;
    swap(float, fa, fb);
    printf("float %.8g %.8g\n", fa, fb);

    long la = 100000L, lb = -100000L;
    swap(long, la, lb);
    printf("long %ld %ld\n", la, lb);

    unsigned ua = 42u, ub = 99u;
    swap(unsigned, ua, ub);
    printf("unsigned %u %u\n", ua, ub);

    int va = 10, vb = 20;
    int *pa = &va, *pb = &vb;
    swap(int *, pa, pb);
    printf("ptr %d %d\n", *pa, *pb);

    Pair s1 = {1, 2.5};
    Pair s2 = {3, 4.5};
    swap(Pair, s1, s2);
    printf("struct %d %.8g %d %.8g\n", s1.n, s1.x, s2.n, s2.x);

    int lo = INT_MIN, hi = INT_MAX;
    swap(int, lo, hi);
    if (lo == INT_MAX && hi == INT_MIN)
        printf("limits ok\n");
    else
        printf("limits %d %d\n", lo, hi);

    return 0;
}
