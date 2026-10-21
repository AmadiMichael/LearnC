#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER '0'
#define HELPER '1'

#define MAX_STACK_SIZE 100
#define MAX_OP_SIZE 100

void clear(double[26]);
void push(double);
double pop(void);
int getop(char[MAX_OP_SIZE]);
int getLine(char[], int);
void writenum(char[MAX_OP_SIZE], int);
int handlehelpers(char, char, char, char[MAX_OP_SIZE], int);

void peek(void);
void dup(void);
void swap(void);
void empty(void);


double var[26];
int lastLetterIndex = 'a';
double lastPrintedNumber = 0;

char line[MAX_OP_SIZE];
int lastLinePointer = 0;

int main() {
    clear(var);

    char s[MAX_OP_SIZE];

    int i = getLine(line, MAX_OP_SIZE);
    if (i == 0) {
        return 0;
    }

    int type;
    while(1) {
        type = getop(s);

        switch(type) {
            case NUMBER: {
                double v = atof(s);
                push(v);
                break;
            }

            case HELPER: {
                if (s[0] == 's') {
                    push(sin(pop()));
                } else if (s[0] == 'e') {
                    push(exp(pop()));
                } else if (s[0] == 'p') {
                    double op2 = pop();
                    push(pow(pop(), op2));
                } else {
                    printf("unknown helper\n");
                } 

                break;
            }

            case '+': {
                push(pop() + pop());
                break;
            }

            case '*': {
                push(pop() * pop());
                break;
            }

            case '-': {
                double op2 = pop();
                push(pop() - op2);
                break;
            }

            case '/': {
                double op2 = pop();
                if (op2 == 0.0) {
                    printf("cannot divide by 0\n");
                    break;
                }
                push(pop() / op2);
                break;
            }

            case '%': {
                double op2 = pop();
                if (op2 == 0.0) {
                    printf("cannot modulo by 0\n");
                    break;
                }
                push(fmod(pop(), op2));
                break;
            }

            case '\n': case '\0': {
                double ans = pop();
                printf("%.8g\n", ans);

                lastPrintedNumber = ans;

                int i = getLine(line, MAX_OP_SIZE);
                lastLinePointer = 0;
                if (i == 0) {
                    return 0;
                }

                break;
            }

            case 'P' : {
                peek();
                break;
            }

            case 'D': {
                dup();
                break;
            }

            case 'S': {
                swap();
                break;
            }

            case 'C': {
                empty();
                break;
            }

            case 'a'...'z': {
                push(var[type - 'a']);
                lastLetterIndex = type;
                break;
            }

            case '=': {
                pop();
                double num = pop();
                push(num);

                int index = lastLetterIndex - 'a';

                var[index] = num;
                break;
            }

            case '_': {
                push(lastPrintedNumber);
                break;
            }

            default: {
                printf("unknown instruction\n");
                break;
            }
        }
    }
}

double stack[MAX_STACK_SIZE];
int stackPointer = 0;

void push(double v) {
    if (stackPointer >= MAX_STACK_SIZE) {
        printf("stack overflow, can't push %f\n", v);
        return;
    }
    stack[stackPointer++] = v;
}

double pop(void) {
    if (stackPointer == 0) {
        printf("stack underflow, can't pop\n");
        return 0.0;
    }
    double v = stack[--stackPointer];
    return v;
}

void peek(void) {
    if (stackPointer > 0) {
        lastPrintedNumber = stack[stackPointer - 1];
        printf("%.8g\n", lastPrintedNumber);
    }
}

void dup(void) {
    if (stackPointer > 0) {
        push(stack[stackPointer - 1]);
    }
}

void swap(void) {
    if (stackPointer > 1) {
        double a = stack[stackPointer - 1];
        stack[stackPointer - 1] = stack[stackPointer - 2];
        stack[stackPointer - 2] = a;
    }
}

void empty(void) {
    stackPointer = 0;
}


int getop(char s[MAX_OP_SIZE]) {
    int sIndex = 0;
    int c;

    // Get the first non space character if any.
    while (((c = line[lastLinePointer++]) != EOF) && ((c == ' ') || (c == '\t')));

    if (c == '-' || c == '.') {
        int d = line[lastLinePointer++];

        if (!isdigit(d) && (d != '.')) {
            lastLinePointer--;
            return c;
        }

        s[sIndex++] = c;
        s[sIndex++] = d;
        writenum(s, sIndex);
        return NUMBER;
    } else if (isdigit(c)) {
        s[sIndex++] =  c; 
        writenum(s, sIndex);
        return NUMBER;
    } else {
        if (c == 'p') {
            return handlehelpers(c, 'o', 'w', s, sIndex);
        } else if (c == 'e') {
            return handlehelpers(c, 'x', 'p', s, sIndex);
        } else if (c == 's') {
            return handlehelpers(c, 'i', 'n', s, sIndex);
        }

        return c;
    }
}

int handlehelpers(char c, char expA, char expB, char s[MAX_OP_SIZE], int sIndex) {
    int a = line[lastLinePointer];
    int b = line[lastLinePointer + 1];
    int ccc = line[lastLinePointer + 2];

    if ((a == expA && b == expB) && ((ccc == ' ') || (ccc == '\t') || (ccc == '\n') || (ccc == EOF) || (ccc == '\0'))) {
        s[sIndex++] = c;
        s[sIndex++] = a;
        s[sIndex++] = b;

        lastLinePointer++;
        lastLinePointer++;

        return HELPER;
    } else {
        return c;
    }
}

void writenum(char s[MAX_OP_SIZE], int sIndex) {
    int d;
    while(((d = line[lastLinePointer++]) != EOF) && (isdigit(d) || d == '.')) {
        s[sIndex++] = d;
    }
    s[sIndex] = '\0';

    lastLinePointer--;
}

int getLine(char s[], int lim) {
    int c, i;

    for (i = 0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; ++i)
        s[i] = c;
    if (c == '\n') {
        s[i] = c;
        ++i;
    }
    s[i] = '\0';
    return i;
}

void clear(double v[26]) {
    int i = 0;
    while(i < 26) {
        v[i++] = 0.0;
    }
}