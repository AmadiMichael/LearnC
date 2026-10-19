#include <stdio.h>

#define MAX_EXPECTED_WORD 100
#define WRAP 20
#define FALSE 0
#define TRUE 1
#define TAB_FILLER -2
#define TAB_SIZE 8

void clear(char[MAX_EXPECTED_WORD]);
void print(char[MAX_EXPECTED_WORD]);
void printDelayed(char[MAX_EXPECTED_WORD]);

int main() {
    char line[MAX_EXPECTED_WORD];
    char temp[MAX_EXPECTED_WORD];
    clear(line);

    int lineIndex, tempIndex, c, wfs;
    lineIndex = tempIndex = 0;
    wfs = FALSE;

    while((c = getchar()) != EOF) {
        if (c == '\n') {
            print(line);
            clear(temp);
            lineIndex = 0;
            tempIndex = 0;
            wfs = FALSE;
        } else if (c == ' ') {
            if (lineIndex >= WRAP) {
                print(line);
                clear(temp);
                lineIndex = 0;
                tempIndex = 0;
            } else {
                clear(temp);
                tempIndex = 0;
                line[lineIndex++] = c;
            }

            wfs = FALSE;
        } else if (c == '\t') {
            // Calculate next stop and add fillers.
            int next_tab_stop = ((lineIndex / TAB_SIZE) + 1) * TAB_SIZE;

            if (next_tab_stop >= WRAP) {
                print(line);
                clear(temp);
                lineIndex = 0;
                tempIndex = 0;
            } else {
                // Add tab to the line.
                line[lineIndex++] = c;

                // Fill with tab fillers.
                while (lineIndex < next_tab_stop) {
                    line[lineIndex++] = TAB_FILLER;
                }
                
                clear(temp);
                tempIndex = 0;
            }

            wfs = FALSE;
        } else {
            if (lineIndex >= WRAP) {
                if (wfs == FALSE) {
                    // Clear all text up until the last space or tab.
                    // They should already have been cached in temp. 
                    char x;
                    int i = lineIndex - 1;
                    while ((i >= 0) && ((x = line[i]) != ' ') && (x != '\t') && (x != TAB_FILLER)) {
                        line[i--] = 0;
                    }
                    
                    // Print line. Print ignores space and tab if its the last consecutive chars.
                    print(line);

                    // copy temp into line. (Line should have been cleared by print at this point).
                    i = 0;
                    while (i < tempIndex) {
                        line[i] = temp[i];
                        ++i;
                    }
                    
                    // Reset temp.
                    clear(temp);

                    // Set the correct line index.
                    if (tempIndex > 0) lineIndex = tempIndex;
                    else lineIndex = 0;

                    // Reset temp index.
                    tempIndex = 0;

                    // Set word from start to true.
                    wfs = TRUE;
                }

                // Add the word to the list.
                line[lineIndex++] = c;
            } else {
                if (lineIndex == 0) wfs = TRUE;

                if (wfs == FALSE) {
                    temp[tempIndex++] = c;
                }

                line[lineIndex++] = c;
            }
        }
    }

    // If EOF is hit without a new line, print the current line.
    if (lineIndex > 0) print(line);
}


void print(char line[MAX_EXPECTED_WORD]) {
    char delayed[MAX_EXPECTED_WORD];
    clear(delayed);

    int c, i, dc;
    c = i = dc = 0;

    while((i < MAX_EXPECTED_WORD) && (c = line[i++]) != 0) {
        if (c == ' ' || c == '\t') {
            delayed[dc++] = c;
        } else {
            if (c == TAB_FILLER) continue;

            printDelayed(delayed);
            dc = 0;

            putchar(c);
        }
    }

    putchar('\n');

    clear(line);
    clear(delayed);
}

void printDelayed(char delayed[MAX_EXPECTED_WORD]) {
    int c, i;
    c = i = 0;

    while((i < MAX_EXPECTED_WORD) && (c = delayed[i++]) != 0) {
        putchar(c);
    }

    clear(delayed);
}


void clear(char line[MAX_EXPECTED_WORD]) {
    int i = 0;
    while (i < MAX_EXPECTED_WORD) {
        line[i++] = 0; 
    }
}