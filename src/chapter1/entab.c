#include <stdio.h>
#include <stdlib.h>

#define TAB_SIZE 8

void write(int, int, int, char *[]);
void write_c(char, int);
int nextTabStop(int col, int argc, char *argv[]);

int main(int argc, char *argv[]) {
    // Get each char of text via getchar() and write it to stdout via putchar().
    int c, col, s, i;

    s = col = 0;
    while ((c = getchar()) != EOF) {
        if (c == '\t') {
            write(s, col, argc, argv);
            s = 0;

            // If tab, go to the next tab stop.
            col = nextTabStop(col, argc, argv);
            putchar('\t');
            continue;
        }

        if (c == '\n') {
            write(s, col, argc, argv);
            s = 0;

            putchar('\n');
            col = 0;
            i = argc == 1 ? 0 : 1;
            continue;
        }

        if (c == ' ') ++s;
        else {
            write(s, col, argc, argv);
            s = 0;

            putchar(c);
        }

        ++col;
    }

    write(s, col, argc, argv);
}

void write(int s, int col, int argc, char *argv[]) {
    if (s <= 1) {
        write_c(' ', s);
        return;
    }

    int lastStop = col - s;
    while (s > 0) {
        // Get next tab stop.
        int nextstop = nextTabStop(col - s, argc, argv);

        if (col < nextstop) {
            write_c(' ', s);
            return;
        } else {
            if (nextstop - lastStop == 0) {
                write_c(' ', s);
                return;
            }

            write_c('\t', 1);
            s -= (nextstop - lastStop);
            lastStop = nextstop;
        }
    }
}

void write_c(char c, int i) {
    while (i > 0) {
        putchar(c);
        --i;
    }
}

int nextTabStop(int col, int argc, char *argv[]) {
    if (argc > 1) {
      int next;
      int i = 1;
      while((i < argc) && (next = atoi(argv[i++])) <= col);
    //   printf("%d\n", next);
  
      return next;
    } else {
      return col + (TAB_SIZE - (col % TAB_SIZE));
    }
}