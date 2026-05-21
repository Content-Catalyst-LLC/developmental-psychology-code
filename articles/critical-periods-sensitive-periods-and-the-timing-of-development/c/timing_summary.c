#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384
#define MAX_COLUMNS 256

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/developmental_timing_panel.csv\n", argv[0]);
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

    int critical_col = -1;
    int sensitive_col = -1;
    int col = 0;
    char *token = strtok(line, ",");

    while (token != NULL && col < MAX_COLUMNS) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "critical_outcome") == 0) {
            critical_col = col;
        }
        if (strcmp(token, "sensitive_outcome") == 0) {
            sensitive_col = col;
        }
        token = strtok(NULL, ",");
        col++;
    }

    if (critical_col < 0 || sensitive_col < 0) {
        fprintf(stderr, "Required outcome columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double critical_sum = 0.0;
    double sensitive_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == critical_col) {
                critical_sum += atof(field);
            }
            if (current_col == sensitive_col) {
                sensitive_sum += atof(field);
            }
            field = strtok(NULL, ",");
            current_col++;
        }
        count++;
    }

    fclose(fp);

    if (count == 0) {
        fprintf(stderr, "No data rows found\n");
        return 1;
    }

    printf("Rows analyzed: %ld\n", count);
    printf("Mean critical_outcome: %.4f\n", critical_sum / count);
    printf("Mean sensitive_outcome: %.4f\n", sensitive_sum / count);

    return 0;
}
