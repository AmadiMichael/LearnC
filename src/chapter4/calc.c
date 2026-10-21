#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER '0'
#define HELPER '1'

#define MAX_STACK_SIZE 100
#define MAX_BUF_SIZE 100
#define MAX_OP_SIZE 100

void clear(double[26]);
void push(double);
double pop(void);
int getop(char[MAX_OP_SIZE]);
int getch(void);
void ungetch(int);
void writenum(char[MAX_OP_SIZE], int);
int handlehelpers(char, char, char, char[MAX_OP_SIZE], int);

void peek(void);
void dup(void);
void swap(void);
void empty(void);


double var[26];
int lastLetterIndex = 'a';
double lastPrintedNumber = 0;

int main() {
    clear(var);

    char s[MAX_OP_SIZE];

    int type;

    while((type = getop(s)) != EOF) {
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

            case '\n': {
                double ans = pop();
                printf("%.8g\n", ans);

                lastPrintedNumber = ans;
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
    while (((c = getch()) != EOF) && ((c == ' ') || (c == '\t')));

    if (c == '-' || c == '.') {
        int d = getch();

        if (!isdigit(d) && (d != '.')) {
            ungetch(d);
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
    int a = getch();
    int b = getch();
    int ccc = getch();

    if ((a == expA && b == expB) && ((ccc == ' ') || (ccc == '\t') || (ccc == '\n') || (ccc == EOF))) {
        s[sIndex++] = c;
        s[sIndex++] = a;
        s[sIndex++] = b;

        ungetch(ccc);

        return HELPER;
    } else {
        ungetch(ccc);
        ungetch(b);
        ungetch(a);

        return c;
    }
}

void writenum(char s[MAX_OP_SIZE], int sIndex) {
    int d;
    while(((d = getch()) != EOF) && (isdigit(d) || d == '.')) {
        s[sIndex++] = d;
    }
    s[sIndex] = '\0';

    ungetch(d);
}


int buf[MAX_BUF_SIZE];
int bufNextPointer = 0;

int getch() {
    if (bufNextPointer == 0) {
        int a = getchar();
        return a;
    } else {
        return buf[--bufNextPointer];
    }
}

void ungetch(int c) {
    if (bufNextPointer >= MAX_BUF_SIZE) {
        printf("Buffer full\n");
    } else {
        buf[bufNextPointer++] = c;
    }
}

void clear(double v[26]) {
    int i = 0;
    while(i < 26) {
        v[i++] = 0.0;
    }
}