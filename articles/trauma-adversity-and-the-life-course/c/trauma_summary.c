#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384
#define MAX_COLUMNS 256

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/trauma_life_course_panel.csv\n", argv[0]);
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
    int adversity_col = -1;
    int support_col = -1;
    int col = 0;
    char *token = strtok(line, ",");

    while (token != NULL && col < MAX_COLUMNS) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "adaptation_score") == 0) score_col = col;
        if (strcmp(token, "current_adversity") == 0) adversity_col = col;
        if (strcmp(token, "current_support") == 0) support_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || adversity_col < 0 || support_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0;
    double adversity_sum = 0.0;
    double support_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double score = 0.0;
        double adversity = 0.0;
        double support = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) score = atof(field);
            if (current_col == adversity_col) adversity = atof(field);
            if (current_col == support_col) support = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        score_sum += score;
        adversity_sum += adversity;
        support_sum += support;
    }

    fclose(fp);

    if (count == 0) {
        fprintf(stderr, "No data rows found\n");
        return 1;
    }

    printf("Rows analyzed: %ld\n", count);
    printf("Mean adaptation_score: %.4f\n", score_sum / count);
    printf("Mean current_adversity: %.4f\n", adversity_sum / count);
    printf("Mean current_support: %.4f\n", support_sum / count);

    return 0;
}
