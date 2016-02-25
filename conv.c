#include <stdio.h>

#define StartMask 1 << 0
#define AMask     1 << 1
#define BMask     1 << 2
#define XMask     1 << 3
#define YMask     1 << 4
#define ZMask     1 << 5
#define UpMask    1 << 6
#define DownMask  1 << 7

int main(int argc, char* argv[]) {
    FILE* file = fopen("conv.dtm", "w");

    // skip header
    for (int i = 0; i < 0x100; i++) {
        fputc(getchar(), file);
    }

    // skip ready, go
    for (int i = 0; i < 123 * 32; i++) {
        fputc(getchar(), file);
    }

    const char* blank = "\0\0\0\0";
    char initseq[] = {StartMask, UpMask, YMask|DownMask, StartMask};
    char seq[] = {StartMask, XMask|DownMask, XMask|DownMask, XMask|DownMask, XMask|DownMask, StartMask};

    char c;
    int count = 0;
    while ((c = getchar()) != EOF) {
        fputc(c, file);
        count++;
        if (!(count % 32)) {
            char* ptr;
            for (int i = 0; i < 6; i++) {
                fputc(seq[i], file);
                for (int bit = 1; bit < 4; bit++) fputc('\0', file);
                for (int bit = 4; bit < 8; bit++) fputc('', file);

                for (int port = 2; port <= 4; port++) fputs(blank, file);
            }
        }
    }

    return 0;
}
