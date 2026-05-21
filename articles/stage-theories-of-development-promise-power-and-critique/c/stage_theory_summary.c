#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/stage_theory_development_panel.csv\n", argv[0]);
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

    int score_col = -1, readiness_col = -1, support_col = -1, stress_col = -1, logistic_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) score_col = col;
        if (strcmp(token, "transition_readiness") == 0) readiness_col = col;
        if (strcmp(token, "current_support") == 0) support_col = col;
        if (strcmp(token, "chronic_stress") == 0) stress_col = col;
        if (strcmp(token, "logistic_transition") == 0) logistic_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || readiness_col < 0 || support_col < 0 || stress_col < 0 || logistic_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0, readiness_sum = 0.0, support_sum = 0.0, stress_sum = 0.0, logistic_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double score = 0.0, readiness = 0.0, support = 0.0, stress = 0.0, logistic = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) score = atof(field);
            if (current_col == readiness_col) readiness = atof(field);
            if (current_col == support_col) support = atof(field);
            if (current_col == stress_col) stress = atof(field);
            if (current_col == logistic_col) logistic = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        score_sum += score;
        readiness_sum += readiness;
        support_sum += support;
        stress_sum += stress;
        logistic_sum += logistic;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", score_sum / count);
    printf("Mean transition_readiness: %.4f\n", readiness_sum / count);
    printf("Mean current_support: %.4f\n", support_sum / count);
    printf("Mean chronic_stress: %.4f\n", stress_sum / count);
    printf("Mean logistic_transition: %.4f\n", logistic_sum / count);
    return 0;
}
