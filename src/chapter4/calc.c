#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define NUMBER '0'
#define MAX_STACK_SIZE 100
#define MAX_BUF_SIZE 100
#define MAX_OP_SIZE 100

void push(double);
double pop(void);
int getop(char[MAX_OP_SIZE]);
int getch(void);
void ungetch(int);
void writenum(char[MAX_OP_SIZE], int);

int main() {
    char s[MAX_OP_SIZE];

    int type;

    while((type = getop(s)) != EOF) {
        switch(type) {
            case NUMBER: {
                double v = atof(s);
                push(v);
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


int getop(char s[]) {
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


char buf[MAX_BUF_SIZE];
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