#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/nature_nurture_development_panel.csv\n", argv[0]);
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

    int score_col = -1, protective_col = -1, support_col = -1, stress_col = -1, sensitivity_col = -1, risk_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) score_col = col;
        if (strcmp(token, "protective_context") == 0) protective_col = col;
        if (strcmp(token, "caregiver_support") == 0) support_col = col;
        if (strcmp(token, "acute_stress") == 0) stress_col = col;
        if (strcmp(token, "biological_sensitivity") == 0) sensitivity_col = col;
        if (strcmp(token, "structural_risk") == 0) risk_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || protective_col < 0 || support_col < 0 || stress_col < 0 || sensitivity_col < 0 || risk_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0, protective_sum = 0.0, support_sum = 0.0, stress_sum = 0.0, sensitivity_sum = 0.0, risk_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double score = 0.0, protective = 0.0, support = 0.0, stress = 0.0, sensitivity = 0.0, risk = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) score = atof(field);
            if (current_col == protective_col) protective = atof(field);
            if (current_col == support_col) support = atof(field);
            if (current_col == stress_col) stress = atof(field);
            if (current_col == sensitivity_col) sensitivity = atof(field);
            if (current_col == risk_col) risk = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        score_sum += score;
        protective_sum += protective;
        support_sum += support;
        stress_sum += stress;
        sensitivity_sum += sensitivity;
        risk_sum += risk;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", score_sum / count);
    printf("Mean protective_context: %.4f\n", protective_sum / count);
    printf("Mean caregiver_support: %.4f\n", support_sum / count);
    printf("Mean acute_stress: %.4f\n", stress_sum / count);
    printf("Mean biological_sensitivity: %.4f\n", sensitivity_sum / count);
    printf("Mean structural_risk: %.4f\n", risk_sum / count);
    return 0;
}
