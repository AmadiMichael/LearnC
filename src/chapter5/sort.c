#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAXLINES 5000 /* max #lines to be sorted */
#define MAXLEN 1000
#define ALLOCSIZE 10000

char *lineptr[MAXLINES]; /* pointers to text lines */

struct Options {
    int numeric; /* 1 if numeric sort */
    int decreasing; /* 1 if sort in decreasing order */
    int fold; /* 1 if upper and lower case should be the same */
};

void inputprocessor(int, char *[], struct Options *);
int readlines(char *lineptr[], char *, int nlines);
void writelines(char *lineptr[], int nlines);
void qsort(void *lineptr[], int left, int right, struct Options);
int numcmp(const char *, const char *);
int getLine(char *, int);
double atof(const char *);
void toLowercase(char *, char *);

struct Options opt;

/* sort input lines */
int main(int argc, char *argv[])
{
    int nlines;      /* number of input lines read */

    inputprocessor(argc, argv, &opt);

    char line[MAXLEN * MAXLINES];
    if ((nlines = readlines(lineptr, line, MAXLINES)) >= 0) {
        qsort((void **)lineptr, 0, nlines - 1, opt);
        writelines(lineptr, nlines);
        return 0;
    } else {
        printf("input too big to sort\n");
        return 1;
    }
}

void inputprocessor(int argc, char *argv[], struct Options *opt) {
    int i = 1;
    while(i < argc) {
        if (strcmp(argv[i], "-n") == 0) {
            opt->numeric = 1;
        } else if (strcmp(argv[i], "-r") == 0) {
            opt->decreasing = 1;
        } else if (strcmp(argv[i], "-f") == 0) {
            opt->fold = 1;
        }

        ++i;
    }
}

/* qsort: sort v[left]...v[right] into increasing order */
void qsort(void *v[], int left, int right, struct Options opt)
{
    int (*comp)(const char *, const char *) = opt.numeric ? numcmp : strcmp;
    int i, last;
    void swap(void *v[], int, int);

    if (left >= right) { /* do nothing if array contains */
        return;        /* fewer than two elements */
    }

    swap(v, left, (left + right) / 2);
    last = left;
    for (i = left + 1; i <= right; i++) {
        char line1[MAXLEN];
        char line2[MAXLEN];

        toLowercase(v[i], line1);
        toLowercase(v[left], line2);

        int r = (*comp)(opt.fold ? &line1 : v[i], opt.fold ? &line2 : v[left]);
        if ((r < 0 && opt.decreasing == 0) || (r > 0 && opt.decreasing)) {
            swap(v, ++last, i);
        }
    }
    swap(v, left, last);
    qsort(v, left, last - 1, opt);
    qsort(v, last + 1, right, opt);
}

void toLowercase(char *s, char *l) {
    int i = 0;
    while (s[i] != '\0') {
        l[i] = tolower(s[i]);
        i++;
    }

    l[i] = '\0';
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
