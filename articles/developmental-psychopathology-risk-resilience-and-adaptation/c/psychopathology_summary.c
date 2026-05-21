#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/developmental_psychopathology_panel.csv\n", argv[0]);
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

    int score_col = -1, risk_col = -1, support_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "adaptation_score") == 0) score_col = col;
        if (strcmp(token, "current_risk") == 0) risk_col = col;
        if (strcmp(token, "current_support") == 0) support_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || risk_col < 0 || support_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0, risk_sum = 0.0, support_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double score = 0.0, risk = 0.0, support = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) score = atof(field);
            if (current_col == risk_col) risk = atof(field);
            if (current_col == support_col) support = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        score_sum += score;
        risk_sum += risk;
        support_sum += support;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean adaptation_score: %.4f\n", score_sum / count);
    printf("Mean current_risk: %.4f\n", risk_sum / count);
    printf("Mean current_support: %.4f\n", support_sum / count);
    return 0;
}
