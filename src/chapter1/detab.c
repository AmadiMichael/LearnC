#include <stdio.h>

#define TAB_SIZE 8

int remTab(int);

int main() {
  int s, outIndex, col;

  s = col = 0;
  while (((s = getchar()) != EOF)) {
    if (s == '\t') {
      int k = remTab(col);
      for (int j = 0; j < k; ++j) { 
        putchar(' ');
      }
      col += k;
    } else {
      if (s == '\n') col = 0;
      else ++col;

      putchar(s);
    }
  }
}

int remTab(int x) {
  return TAB_SIZE - (x % TAB_SIZE);
}