#include <stdio.h>

#define SIZE 1000

void getLine(char l[SIZE]);
double atof(char s[SIZE]);
double negExp(int d);
double powOf10(int a);
int processB(char b[SIZE], int bi, int isNeg);

enum STAGE {
    START,
    EXP
};

int main() {
    char s[SIZE];
    getLine(s);

    double f = atof(s);

    printf("%.8g\n", f);
}

double atof(char s[SIZE]) {
    double ans = 0;
    char b[SIZE];
    int bi = 0;
    int bProcessed = 0;

    enum STAGE stage = START;
    int isNeg = 0;
    int isExpNeg = 0;
    int decPlace = 0;

    int i = 0;
    int c = 0;

    while((c = s[i++]) != '\0') {
        switch(c) {
            case '+': case '-': {
                if (c == '-') {
                    if (stage == START) {
                        isNeg = 1;
                    } else {
                        isExpNeg = 1;
                    }
                }
                break;
            }

            case '.': {
                // Process b.
                ans += processB(b, bi, isNeg);
                bProcessed = 1;

                decPlace = 1;
                break;
            }

            case 'e': case 'E': {
                // Process b if not done yet.
                if (bProcessed == 0) {
                    ans += processB(b, bi, isNeg);
                    bProcessed = 1;
                }

                stage = EXP;
                bi = 0;
                bProcessed = 0;
                break;
            }

            default: {
                if (stage == START) {
                    // If before the dec point, 
                    // store and then only process the numbers only after the decimal point is seen
                    // or after the loop.
                    if (decPlace) {
                        // Assume all inputs not covered by case are numbers.
                        int num = c - '0';

                        if (isNeg) {
                            ans -= (negExp(decPlace) * num);
                        } else {
                            ans += (negExp(decPlace) * num);
                        }
                        decPlace++;
                    } else {
                        b[bi++] = c;
                    }
                } else {
                    b[bi++] = c;
                }
                break;
            }
        }
    }

    if (bProcessed == 0) {
        if (stage == START) {
            ans += processB(b, bi, isNeg);
            bProcessed = 1;
        } else {
            int num = processB(b, bi, 0);
            if (isExpNeg) {
                ans *= negExp(num);
            } else {
                ans *= powOf10(num);
            }
            bProcessed = 1;
        }
    }

    return ans;
}

int processB(char b[SIZE], int bi, int isNeg) {
    int ans = 0;

    int j = 0;
    while (bi > 0) {
        ans += (powOf10(--bi) * (b[j++] - '0'));
    }

    if (isNeg) ans = -ans;

    return ans;
}

double powOf10(int a) {
    double ans = 1;

    while (a > 0) {
        ans *= 10;
        a--;
    }

    return ans;
}

double negExp(int d) {
    return (double) 1 / powOf10(d);
}

void getLine(char l[SIZE]) {
    int i = 0;
    int c = 0;

    while(((c = getchar()) != EOF) && (c != '\n')) {
        if (c != ' ') l[i++] = c;
    }
    l[i++] = '\0';
}