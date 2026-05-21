#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/genes_environment_plasticity_panel.csv\n", argv[0]);
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

    int development_col = -1, embedded_stress_col = -1, embedded_support_col = -1, care_col = -1, stress_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) development_col = col;
        if (strcmp(token, "embedded_stress") == 0) embedded_stress_col = col;
        if (strcmp(token, "embedded_support") == 0) embedded_support_col = col;
        if (strcmp(token, "current_care") == 0) care_col = col;
        if (strcmp(token, "current_stress") == 0) stress_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (development_col < 0 || embedded_stress_col < 0 || embedded_support_col < 0 || care_col < 0 || stress_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double development_sum = 0.0, embedded_stress_sum = 0.0, embedded_support_sum = 0.0, care_sum = 0.0, stress_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double development = 0.0, embedded_stress = 0.0, embedded_support = 0.0, care = 0.0, stress = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == development_col) development = atof(field);
            if (current_col == embedded_stress_col) embedded_stress = atof(field);
            if (current_col == embedded_support_col) embedded_support = atof(field);
            if (current_col == care_col) care = atof(field);
            if (current_col == stress_col) stress = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        development_sum += development;
        embedded_stress_sum += embedded_stress;
        embedded_support_sum += embedded_support;
        care_sum += care;
        stress_sum += stress;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", development_sum / count);
    printf("Mean embedded_stress: %.4f\n", embedded_stress_sum / count);
    printf("Mean embedded_support: %.4f\n", embedded_support_sum / count);
    printf("Mean current_care: %.4f\n", care_sum / count);
    printf("Mean current_stress: %.4f\n", stress_sum / count);
    return 0;
}
