#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384
#define MAX_COLUMNS 256

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/developmental_design_panel.csv\n", argv[0]);
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
    int observed_col = -1;
    int col = 0;
    char *token = strtok(line, ",");

    while (token != NULL && col < MAX_COLUMNS) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) {
            score_col = col;
        }
        if (strcmp(token, "observed") == 0) {
            observed_col = col;
        }
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || observed_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        int observed = 0;
        double score = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == observed_col) {
                observed = atoi(field);
            }
            if (current_col == score_col) {
                score = atof(field);
            }
            field = strtok(NULL, ",");
            current_col++;
        }

        if (observed == 1) {
            count++;
            score_sum += score;
        }
    }

    fclose(fp);

    if (count == 0) {
        fprintf(stderr, "No observed rows found\n");
        return 1;
    }

    printf("Observed rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", score_sum / count);

    return 0;
}
