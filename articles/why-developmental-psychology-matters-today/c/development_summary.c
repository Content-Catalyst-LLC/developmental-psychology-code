#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 8192
#define MAX_COLUMNS 128

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/developmental_panel.csv\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        perror("Unable to open CSV file");
        return 1;
    }

    char line[MAX_LINE];

    if (!fgets(line, sizeof(line), fp)) {
        fprintf(stderr, "CSV is empty\n");
        fclose(fp);
        return 1;
    }

    int score_col = -1;
    int col = 0;
    char *token = strtok(line, ",");

    while (token != NULL && col < MAX_COLUMNS) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) {
            score_col = col;
            break;
        }
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0) {
        fprintf(stderr, "development_score column not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) {
                sum += atof(field);
                count++;
                break;
            }
            field = strtok(NULL, ",");
            current_col++;
        }
    }

    fclose(fp);

    if (count == 0) {
        fprintf(stderr, "No data rows found\n");
        return 1;
    }

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", sum / count);

    return 0;
}
