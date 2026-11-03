#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAXLINES 5000 /* max #lines to be sorted */
#define MAXLEN 1000
#define ALLOCSIZE 10000
#define MAXOPTS 10

char *lineptr[MAXLINES]; /* pointers to text lines */

struct Options {
    int field; /* field number to sort using the other opt */
    int numeric; /* 1 if numeric sort */
    int decreasing; /* 1 if sort in decreasing order */
    int fold; /* 1 if upper and lower case should be the same */
    int dirorder; /* 1 if comparisons should only be on alphabets, letters and blanks */
};

void inputprocessor(int, char *[]);
int readlines(char *lineptr[], char *, int nlines);
void writelines(char *lineptr[], int nlines);
void qsort(void *lineptr[], int left, int right);
int numcmp(const char *, const char *);
int getLine(char *, int);
double atof(const char *);
int atoi(const char *);
void toLowercase(char *);
void dirorderstring(char *line);
int fieldcmp(char *left, char *right);

struct Options opt[MAXOPTS];
int optindex = -1;

/* sort input lines */
int main(int argc, char *argv[])
{
    int nlines;      /* number of input lines read */

    inputprocessor(argc, argv);

    char line[MAXLEN * MAXLINES];
    if ((nlines = readlines(lineptr, line, MAXLINES)) >= 0) {
        qsort((void **)lineptr, 0, nlines - 1);
        writelines(lineptr, nlines);
        return 0;
    } else {
        printf("input too big to sort\n");
        return 1;
    }
}

void inputprocessor(int argc, char *argv[]) {
    int i = 1;

    while(i < argc) {
        if (strcmp(argv[i], "-n") == 0) {
            if (i == 1) optindex = 0;
            (opt + optindex)->numeric = 1;
        } else if (strcmp(argv[i], "-r") == 0) {
            if (i == 1) optindex = 0;
            (opt + optindex)->decreasing = 1;
        } else if (strcmp(argv[i], "-f") == 0) {
            if (i == 1) optindex = 0;
            (opt + optindex)->fold = 1;
        } else if (strcmp(argv[i], "-d") == 0) {
            if (i == 1) optindex = 0;
            (opt + optindex)->dirorder = 1;
        } else {
            (opt + ++optindex)->field = atoi(argv[i]);
        }

        ++i;
    }
}

/* qsort: sort v[left]...v[right] into increasing order */
void qsort(void *v[], int left, int right)
{
    int i, last;
    void swap(void *v[], int, int);

    if (left >= right) { /* do nothing if array contains */
        return;        /* fewer than two elements */
    }

    swap(v, left, (left + right) / 2);
    last = left;
    for (i = left + 1; i <= right; i++) {
        char rightline[MAXLEN];
        char leftline[MAXLEN];
        int r;

        strcpy(&rightline[0], v[i]);
        strcpy(&leftline[0], v[left]);

        if (opt[0].field != 0) {
            r = fieldcmp(leftline, rightline);
        } else {
            int (*comp) (const char *, const char *) = opt->numeric ? numcmp : strcmp;

            if (opt->fold) {
                toLowercase(rightline);
                toLowercase(leftline);
            }

            if (opt->dirorder) {
                dirorderstring(rightline);
                dirorderstring(leftline);
            }

            r = (*comp)(&rightline[0], &leftline[0]);

            if ((r < 0 && opt->decreasing == 0) || (r > 0 && opt->decreasing)) {
                r = 1;
            } else {
                r = 0;
            }
        }

        if (r) {
            swap(v, ++last, i);
        }
    }

    swap(v, left, last);
    qsort(v, left, last - 1);
    qsort(v, last + 1, right);
}

int fieldcmp(char *left, char *right) {
    // Split into fields.
    char *leftfields[MAXOPTS];
    char *rightfields[MAXOPTS];

    int i = 0;
    int j = 0;

    leftfields[i++] = strtok(left, " ");
    while((leftfields[i++] = strtok(NULL, " ")) != NULL);

    rightfields[j++] = strtok(right, " ");
    while ((rightfields[j++] = strtok(NULL, " ")) != NULL);

    i = 0;
    while (i <= optindex) {
        int fieldIndex = (opt + i)->field - 1;
        int (*comp) (const char *, const char *) = (opt + i)->numeric ? numcmp : strcmp;

        if ((opt + i)->fold) {
            toLowercase(rightfields[fieldIndex]);
            toLowercase(leftfields[fieldIndex]);
        }

        if ((opt + i)->dirorder) {
            dirorderstring(rightfields[fieldIndex]);
            dirorderstring(leftfields[fieldIndex]);
        }

        int r = (*comp)(rightfields[fieldIndex], leftfields[fieldIndex]);

        if (r == 0) {
            i++;
            continue;
        }

        if ((r < 0 && (opt + i)->decreasing == 0) || (r > 0 && (opt + i)->decreasing)) {
            return 1;
        }
        return 0;
    }

    return 0;
}

void dirorderstring(char *line) {
    int i = 0;
    int j = 0;
    int c = 0;
    while((c = line[i++]) != '\0') {
        if ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == ' ') {
            line[j++] = c;
        }
    }
    line[j] = '\0';
}

void toLowercase(char *s) {
    int i = 0;
    while (s[i] != '\0') {
        s[i] = tolower(s[i]);
        i++;
    }

    s[i] = '\0';
}

/* numcmp: compare s1 and s2 numerically */
int numcmp(const char *s1, const char *s2)
{
    double v1, v2;

    v1 = atof(s1);
    v2 = atof(s2);
    if (v1 < v2) {
        return -1;
    } else if (v1 > v2) {
        return 1;
    } else {
        return 0;
    }
}

void swap(void *v[], int i, int j)
{
    void *temp;

    temp = v[i];
    v[i] = v[j];
    v[j] = temp;
}

int readlines(char *lineptr[], char *line, int maxlines)
{
    int len, nlines;

    nlines = 0;
    while ((len = getLine(line, MAXLEN)) > 0) {
        if (nlines >= maxlines) {
            return -1;
        } else {
            *(line + len - 1) = '\0';
            lineptr[nlines++] = line;
            line = line + len;
        }
    }
    return nlines;
}

void writelines(char *lineptr[], int nlines)
{
    while (nlines-- > 0) {
        printf("%s\n", *lineptr++);
    }
}

int getLine(char s[], int lim)
{
    int c, i;

    for (i = 0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; ++i) {
        s[i] = c;
    }

    if (c == '\n') {
        s[i] = c;
        ++i;
    }

    s[i] = '\0';
    return i;
}
