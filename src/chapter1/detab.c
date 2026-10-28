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
    int next;
    int i = 1;
    while((i < argc) && (next = atoi(argv[i++])) <= col);

    return next;
  } else {
    return col + (TAB_SIZE - (col % TAB_SIZE));
  }
}