#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/prenatal_development_foundations_panel.csv\n", argv[0]);
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

    int outcome_col = -1, care_col = -1, risk_col = -1, gestation_col = -1, health_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "early_outcome") == 0) outcome_col = col;
        if (strcmp(token, "effective_care") == 0) care_col = col;
        if (strcmp(token, "developmental_risk") == 0) risk_col = col;
        if (strcmp(token, "gestational_weeks") == 0) gestation_col = col;
        if (strcmp(token, "maternal_health") == 0) health_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (outcome_col < 0 || care_col < 0 || risk_col < 0 || gestation_col < 0 || health_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double outcome_sum = 0.0, care_sum = 0.0, risk_sum = 0.0, gestation_sum = 0.0, health_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double outcome = 0.0, care = 0.0, risk = 0.0, gestation = 0.0, health = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == outcome_col) outcome = atof(field);
            if (current_col == care_col) care = atof(field);
            if (current_col == risk_col) risk = atof(field);
            if (current_col == gestation_col) gestation = atof(field);
            if (current_col == health_col) health = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        outcome_sum += outcome;
        care_sum += care;
        risk_sum += risk;
        gestation_sum += gestation;
        health_sum += health;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean early_outcome: %.4f\n", outcome_sum / count);
    printf("Mean effective_care: %.4f\n", care_sum / count);
    printf("Mean developmental_risk: %.4f\n", risk_sum / count);
    printf("Mean gestational_weeks: %.4f\n", gestation_sum / count);
    printf("Mean maternal_health: %.4f\n", health_sum / count);
    return 0;
}
