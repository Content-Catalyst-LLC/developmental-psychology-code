#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/lifespan_baltes_panel.csv\n", argv[0]);
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

    int development_col = -1, gains_col = -1, losses_col = -1, soc_col = -1, support_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) development_col = col;
        if (strcmp(token, "gains") == 0) gains_col = col;
        if (strcmp(token, "losses") == 0) losses_col = col;
        if (strcmp(token, "soc_index") == 0) soc_col = col;
        if (strcmp(token, "current_support") == 0) support_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (development_col < 0 || gains_col < 0 || losses_col < 0 || soc_col < 0 || support_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double development_sum = 0.0, gains_sum = 0.0, losses_sum = 0.0, soc_sum = 0.0, support_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double development = 0.0, gains = 0.0, losses = 0.0, soc = 0.0, support = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == development_col) development = atof(field);
            if (current_col == gains_col) gains = atof(field);
            if (current_col == losses_col) losses = atof(field);
            if (current_col == soc_col) soc = atof(field);
            if (current_col == support_col) support = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        development_sum += development;
        gains_sum += gains;
        losses_sum += losses;
        soc_sum += soc;
        support_sum += support;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", development_sum / count);
    printf("Mean gains: %.4f\n", gains_sum / count);
    printf("Mean losses: %.4f\n", losses_sum / count);
    printf("Mean soc_index: %.4f\n", soc_sum / count);
    printf("Mean current_support: %.4f\n", support_sum / count);
    return 0;
}
