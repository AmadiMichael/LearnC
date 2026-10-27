#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double stack[100];
int nextStackPtr = 0;

void push(double);
double pop();

int main(int argc, char *argv[]) {
    int i = 1;
    while(i < argc) {
        switch (*argv[i]) {
            case '+': {
                if (!strcmp(argv[i], "+")) {
                    double ans = pop() + pop();
                    push(ans);
                } else {
                    push(atof(argv[i]));
                }

                break;
            }

            case '*': {
                double ans = pop() * pop();
                push(ans);
                break;
            }
            
            case '-': {
                if (!strcmp(argv[i], "-")) {
                    double a = pop();
                    double ans = pop() - a;
                    push(ans);
                } else {
                    push(atof(argv[i]));
                }

                break;
            }
            
            case '/': {
                double a = pop();
                double ans = pop() / a;
                push(ans);
                break;
            }

            default: {
                push(atof(argv[i]));
                break;
            }
        }

        ++i;
    }

    printf("%.8g\n", pop());

    return 0;
}

void push(double n) {
    stack[nextStackPtr++] = n;
}

double pop() {
    return stack[--nextStackPtr];
}