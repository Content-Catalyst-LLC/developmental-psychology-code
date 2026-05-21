#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/gender_sexual_development_panel.csv\n", argv[0]);
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

    int adjustment_col = -1, protective_col = -1, stigma_col = -1, family_col = -1, consent_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "adjustment_score") == 0) adjustment_col = col;
        if (strcmp(token, "protective_context") == 0) protective_col = col;
        if (strcmp(token, "current_stigma") == 0) stigma_col = col;
        if (strcmp(token, "current_family_support") == 0) family_col = col;
        if (strcmp(token, "current_consent_knowledge") == 0) consent_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (adjustment_col < 0 || protective_col < 0 || stigma_col < 0 || family_col < 0 || consent_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double adjustment_sum = 0.0, protective_sum = 0.0, stigma_sum = 0.0, family_sum = 0.0, consent_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double adjustment = 0.0, protective = 0.0, stigma = 0.0, family = 0.0, consent = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == adjustment_col) adjustment = atof(field);
            if (current_col == protective_col) protective = atof(field);
            if (current_col == stigma_col) stigma = atof(field);
            if (current_col == family_col) family = atof(field);
            if (current_col == consent_col) consent = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        adjustment_sum += adjustment;
        protective_sum += protective;
        stigma_sum += stigma;
        family_sum += family;
        consent_sum += consent;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean adjustment_score: %.4f\n", adjustment_sum / count);
    printf("Mean protective_context: %.4f\n", protective_sum / count);
    printf("Mean current_stigma: %.4f\n", stigma_sum / count);
    printf("Mean current_family_support: %.4f\n", family_sum / count);
    printf("Mean current_consent_knowledge: %.4f\n", consent_sum / count);
    return 0;
}
