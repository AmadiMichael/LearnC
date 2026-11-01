#include <stdio.h>
#include <stdlib.h>

#define TAB_SIZE 8

int nextTabStop(int, int, char *[]);

int main(int argc, char *argv[]) {
  int s, outIndex, col, i;

  s = col = 0;

  while (((s = getchar()) != EOF)) {
    if (s == '\t') {
      int k = nextTabStop(col, argc, argv);
      for (; col < k; ++col) {
        putchar(' ');
      }
    } else {
      if (s == '\n') {
        col = 0;
        i = argc == 1 ? 0 : 1;
      } else {
        ++col;
      }

      putchar(s);
    }
  }
}

int nextTabStop(int col, int argc, char *argv[]) {
  if (argc > 1) {
    char **first = argv;

    if (**(first + 1) == '-') {
      int m, n;

      // Get m.
      char *mstart = *(first + 1);
      m = atoi(mstart + 1);

      // Get n.
      char *nstart = *(first + 2);
      n = atoi(nstart + 1);

      if (col < m) {
        return m;
      } else {
        return col + (n - ((col - m) % n));
      }
    }

    int next;
    while((*(++first) != NULL)) {
      next = atoi(*first);
      if (next > col) break;
    }
    return next;
  } else {
    return col + (TAB_SIZE - (col % TAB_SIZE));
  }
}