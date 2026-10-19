#include <stdio.h>

#define MAX_SIZE 1000

#define ESCAPE_SENTINEL -2

// STATUS
#define FAILED 1

// BOOLEAN
#define TRUE 1
#define FALSE 0

void clear(char[MAX_SIZE]);
char lastChar(char[MAX_SIZE], int);

/*
 * Syntax errors:
 *
 * - Unclosed brackets in the code.
 * - Unclosed strings or character constant.
 */

int main() {
    char lastC = 0;
    char c;

    
    int inComment = 0;
    int inSC = 0;
    int inCC = 0;

    char delimiters[MAX_SIZE];
    clear(delimiters);
    int delimitersIndex = 0;

    while ((c = getchar()) != EOF) {
        if (c == '/') {
            // If in comment and star was the last character, it is the end of a comment. 
            if ((inComment == TRUE) && (lastC == '*')) {
                inComment = FALSE;
            }

            lastC = c;
        } else if (c == '*') {
            // If not in comment and slash was the last character, it is the start of a comment.
            if ((inComment == FALSE) && (inSC == FALSE) && (inCC == FALSE) && (lastC == '/')) {
                inComment = TRUE;
            }

            lastC = c;
        } else if (c == '{') {
            // Update delimiters and code.
            if ((inComment == FALSE) && (inSC == FALSE) && (inCC == FALSE)) {
                delimiters[delimitersIndex++] = c;
            }

            lastC = c;
        } else if (c == '}') {
            // If not in comment, string or character constant, add to code normally.
            if ((inComment == TRUE) || (inSC == TRUE) || (inCC == TRUE)) {
                lastC = c;
                continue;
            }

            if (delimitersIndex > 0) {
                // If the last open braces was not { then its an error, return 1.
                if (lastChar(delimiters, delimitersIndex) != '{') {
                    printf("Expected closing '}', got '%c'\n", c);
                    return FAILED;
                }

                // Update delimiters and code.
                delimiters[--delimitersIndex] = 0;
                lastC = c;
            } else {
                printf("closing braces %c found with no delimiter left\n", c);
                return FAILED;
            }
        } else if (c == '[') {
            // Update delimiters and code.
            if ((inComment == FALSE) && (inSC == FALSE) && (inCC == FALSE)) {
                delimiters[delimitersIndex++] = c;
            }

            lastC = c;
        } else if (c == ']') {
            // If not in comment, string or character constant, add to code normally.
            if ((inComment == TRUE) || (inSC == TRUE) || (inCC == TRUE)) {
                lastC = c;
                continue;
            }

            if (delimitersIndex > 0) {
                // If the last open braces was not [ then its an error, return 1.
                if (lastChar(delimiters, delimitersIndex) != '[') {
                    printf("Expected closing ']', got '%c'\n", c);
                    return FAILED;
                }

                // Update delimiters and code.
                delimiters[--delimitersIndex] = 0;
                lastC = c;
            } else {
                printf("closing braces %c found with no delimiter left\n", c);
                return FAILED;
            }
        } else if (c == '(') {
            // Update delimiters and code.
            if ((inComment == FALSE) && (inSC == FALSE) && (inCC == FALSE)) {
                delimiters[delimitersIndex++] = c;
            }

            lastC = c;
        } else if (c == ')') {
            // If not in comment, string or character constant, add to code normally.
            if ((inComment == TRUE) || (inSC == TRUE) || (inCC == TRUE)) {
                lastC = c;
                continue;
            }

            if (delimitersIndex > 0) {
                // If the last open braces was not ( then its an error, return 1.
                if (lastChar(delimiters, delimitersIndex) != '(') {
                    printf("Expected closing ')', got '%c'\n", c);
                    return FAILED;
                }

                // Update delimiters and code.
                delimiters[--delimitersIndex] = 0;
                lastC = c;
            } else {
                printf("closing braces %c found with no delimiter left\n", c);
                return FAILED;
            }
        } else if (c == '"') {
            // If in comment, just add the char and continue.
            if (inComment == TRUE) {
                lastC = c;
                continue;
            }

            // If in char constant and the last char was an escape, just add the text and continue.
            if (((inCC == TRUE) || (inSC == TRUE)) && (lastC == '\\')) {
                lastC = c;
                continue;
            }
            
            // Set string constant to opp of current state.
            if (inSC == TRUE) inSC = FALSE;
            else inSC = TRUE;

            // Add to code.
            lastC = c;
        } else if (c == '\'') {
            // If in comment, just add the char and continue.
            if (inComment == TRUE) {
                lastC = c;
                continue;
            }

            // If in string constant and the last char was an escape, just add the text and continue.
            if (((inCC == TRUE) || (inSC == TRUE)) && (lastC == '\\')) {
                lastC = c;
                continue;
            }

            // Set string constant to opp of current state.
            if (inCC == TRUE) inCC = FALSE;
            else inCC = TRUE;

            // Add to code.
            lastC = c;
        } else if (c == '\\') {
            if (lastC == '\\') {
                lastC = ESCAPE_SENTINEL;
                continue;
            }

            // Add to code.
            lastC = c;
        } else {
            // Add to code.
            lastC = c;
        }
    }

    // If after reading the text and some states are not finished, revert with errors.
    int cache = delimitersIndex;
    while (cache > 0) {
        printf("Expected closing value for '%c'\n", delimiters[--cache]);
    }

    // If inComment, inSC or inCC is true, print the error
    if (inCC == TRUE) printf("At least 1 character constant value not closed\n");
    if (inSC == TRUE) printf("At least 1 string constant value not closed\n");
    if (inComment == TRUE) printf("At least 1 comment opening not closed\n");


    if ((inComment + inCC + inSC + delimitersIndex) > 0) {
        return FAILED;
    }

    return 0;
}

char lastChar(char code[MAX_SIZE], int currentIndex) {
    return code[currentIndex - 1];
}

void clear(char code[MAX_SIZE]) {
    int i = 0;
    while (i < MAX_SIZE) {
        code[i++] = 0;
    }
}