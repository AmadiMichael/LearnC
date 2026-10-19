#include <stdio.h>

#define SIZE 100

int readInt(int *i);
void clear(int v[SIZE]);
int binsearch(int x, int n, int v[SIZE]);

int main() {
    // Declare the variables.
    int x = 0;
    int n = 0;
    int v[SIZE];
    clear(v);

    // Read inputs.
    int o = readInt(&x);
    if (o) return o;
    o = readInt(&n);
    if (o) return o;

    // Loop n times to get the array of values.
    int i = 0;
    while (i < n) {
        o = readInt(&v[i++]);
        if (o) return o;
    }

    // Binary search and print return value.
    int index = binsearch(x, n, v);
    printf("%d\n", index);
    return 0;
}

int binsearch(int x, int n, int v[SIZE]) {
    // Binary search.
    int low = 0;
    int high = n - 1;
    int mid = (low + high) / 2;

    while (low < high) {
        if (v[mid] >= x) {
            high = mid;
        } else {
            low = mid + 1;
        }
        mid = (low + high) / 2;
    }

    // Only check mid if the array length is > 0.
    if (n > 0 && v[mid] == x) {
        return mid;
    } else {
        // Return -1 if not found.
        return -1;
    }
}

int readInt(int *i) {
    int o = scanf("%d", i);
    if (o == 0 || o == EOF) {
        printf("Error reading int\n");
        return 1;
    }

    return 0;
}

void clear(int v[SIZE]) {
    int i = 0;
    while (i < SIZE) {
        v[i++] = 0;
    }
}