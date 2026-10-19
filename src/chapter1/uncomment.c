#include <stdio.h>

#define MAX_SIZE 1000
#define TRUE 1
#define FALSE 0

void clear(char[MAX_SIZE]);

int main() {
    int c, codeIndex;
    char code[MAX_SIZE];
    clear(code);

    int inQuote = FALSE;
    int inSQ = FALSE;
    int seenEsc = FALSE;
    int commentStart = FALSE;
    int seenSlash = FALSE;
    int seenStar = FALSE;
    codeIndex = 0;

    while ((c = getchar()) != EOF) {
        if (inQuote == FALSE) {
            if (c == '*') {
                if (commentStart == TRUE) {
                    seenStar = TRUE;
                } else {
                    if (seenSlash == TRUE) {
                        commentStart = TRUE;
                        seenSlash = FALSE;
                    } else {
                        code[codeIndex++] = c;
                    }
                }
            } else if (c == '/') {
                if (inSQ == TRUE) {
                    code[codeIndex++] = c;
                } else {
                    if (commentStart == TRUE) {
                        if (seenStar == TRUE) {
                            commentStart = FALSE;
                            seenStar = FALSE;
                            code[codeIndex++] = '\n';
                        } else {
                            continue;
                        }
                    } else {
                        seenSlash = TRUE;
                    }
                }
            } else if (c == '"') {
                if (commentStart == TRUE) {
                    seenSlash = FALSE;
                    seenStar = FALSE;
                } else {
                    if (inSQ == FALSE) inQuote = TRUE;

                    if (seenSlash == TRUE) {
                        code[codeIndex++] = '/';
                        seenSlash = FALSE;
                    }
                    if (seenStar == TRUE) {
                        code[codeIndex++] = '*';
                        seenStar = FALSE;
                    }
                    
                    code[codeIndex++] = c;
                }
            } else if (c == '\'') {
                if (commentStart == FALSE) {
                    if (seenSlash == TRUE) {
                        code[codeIndex++] = '/';
                        seenSlash = FALSE;
                    }
                    if (seenStar == TRUE) {
                        code[codeIndex++] = '*';
                        seenStar = FALSE;
                    }

                    if (inSQ == TRUE) {
                        if (seenEsc == FALSE) inSQ = FALSE;
                        else seenEsc = FALSE;

                        code[codeIndex++] = c;
                    } else {
                        if (commentStart == FALSE) inSQ = TRUE;
                        code[codeIndex++] = c;
                    }
                }
            } else if (c == '\\') {
                if (commentStart == FALSE) {
                    if (seenEsc == TRUE) seenEsc = FALSE;
                    else {
                        if (inSQ == TRUE) seenEsc = TRUE;
                    }

                    if (seenSlash == TRUE) {
                        code[codeIndex++] = '/';
                        seenSlash = FALSE;
                    }
                    if (seenStar == TRUE) {
                        code[codeIndex++] = '*';
                        seenStar = FALSE;
                    }

                    code[codeIndex++] = c;
                }
            } else {
                if (commentStart == TRUE) {
                    seenSlash = FALSE;
                    seenStar = FALSE;
                } else {
                    if (seenSlash == TRUE) {
                        code[codeIndex++] = '/';
                        seenSlash = FALSE;
                    }
                    if (seenStar == TRUE) {
                        code[codeIndex++] = '*';
                        seenStar = FALSE;
                    }

                    code[codeIndex++] = c;
                }
            }
        } else {
            if (c == '"') {
                if (seenEsc == FALSE) {
                    inQuote = FALSE;
                } else {
                    seenEsc = FALSE;
                }
            } else if (c == '\\') {
                if (seenEsc == TRUE) seenEsc = FALSE;
                else seenEsc = TRUE;
            } else {
                if (seenEsc == TRUE) seenEsc = FALSE;
            }

            code[codeIndex++] = c;
        }
    }

    int i = 0;
    while (i < codeIndex) {
        int c = code[i++];
        putchar(c);
    }
}

void clear(char c[MAX_SIZE]) {
    int i = 0;
    while (i < MAX_SIZE) {
        c[i++] = 0;
    }
}