#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/aging_adaptation_later_life_panel.csv\n", argv[0]);
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

    int adjustment_col = -1, fit_col = -1, support_col = -1, health_col = -1, adaptation_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "adjustment_score") == 0) adjustment_col = col;
        if (strcmp(token, "functional_fit") == 0) fit_col = col;
        if (strcmp(token, "current_support") == 0) support_col = col;
        if (strcmp(token, "current_health") == 0) health_col = col;
        if (strcmp(token, "current_adaptation") == 0) adaptation_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (adjustment_col < 0 || fit_col < 0 || support_col < 0 || health_col < 0 || adaptation_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double adjustment_sum = 0.0, fit_sum = 0.0, support_sum = 0.0, health_sum = 0.0, adaptation_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double adjustment = 0.0, fit = 0.0, support = 0.0, health = 0.0, adaptation = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == adjustment_col) adjustment = atof(field);
            if (current_col == fit_col) fit = atof(field);
            if (current_col == support_col) support = atof(field);
            if (current_col == health_col) health = atof(field);
            if (current_col == adaptation_col) adaptation = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        adjustment_sum += adjustment;
        fit_sum += fit;
        support_sum += support;
        health_sum += health;
        adaptation_sum += adaptation;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean adjustment_score: %.4f\n", adjustment_sum / count);
    printf("Mean functional_fit: %.4f\n", fit_sum / count);
    printf("Mean current_support: %.4f\n", support_sum / count);
    printf("Mean current_health: %.4f\n", health_sum / count);
    printf("Mean current_adaptation: %.4f\n", adaptation_sum / count);
    return 0;
}
