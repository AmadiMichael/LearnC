#include <stdio.h>

#define TAB_SIZE 8

void write(int, int);
void writeTab(int);

int main() {
    // Get each char of text via getchar() and write it to stdout via putchar().
    int c, col, s;

    s = col = 0;
    while ((c = getchar()) != EOF) {
        if (c == '\t') {
            write(s, col);
            s = 0;
            
            // If tab, go to the next tab stop.
            col = ((col + TAB_SIZE) / TAB_SIZE) * TAB_SIZE;
            putchar('\t');
            continue;
        }

        if (c == '\n') {
            write(s, col);
            s = 0;

            putchar('\n');
            col = 0;
            continue;
        }

        if (c == ' ') ++s;
        else {
            write(s, col);
            s = 0;

            putchar(c);
        }

        ++col;
    }

    write(s, col);
}

void write(int s, int col) {
    if (s == 0) return;

    // get to the first tab stop if needed.
    int toNextTab = TAB_SIZE - ((col - s) % TAB_SIZE);
    if (toNextTab <= s) {
        writeTab(1);
        s -= toNextTab;
    }

    int t = s / TAB_SIZE;
    writeTab(t);
    s -= TAB_SIZE * t;

    int bc = s % TAB_SIZE;
    while (bc > 0) {
        putchar(' ');
        --bc;
    }
}

void writeTab(int i) {
    while (i > 0) {
        putchar('\t');
        --i;
    }
}