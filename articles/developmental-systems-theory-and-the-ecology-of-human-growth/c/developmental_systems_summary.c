#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/developmental_systems_panel.csv\n", argv[0]);
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

    int development_col = -1, support_col = -1, stress_col = -1, family_col = -1, peer_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) development_col = col;
        if (strcmp(token, "ecological_support") == 0) support_col = col;
        if (strcmp(token, "ecological_stress") == 0) stress_col = col;
        if (strcmp(token, "current_family") == 0) family_col = col;
        if (strcmp(token, "current_peer") == 0) peer_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (development_col < 0 || support_col < 0 || stress_col < 0 || family_col < 0 || peer_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double development_sum = 0.0, support_sum = 0.0, stress_sum = 0.0, family_sum = 0.0, peer_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double development = 0.0, support = 0.0, stress = 0.0, family = 0.0, peer = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == development_col) development = atof(field);
            if (current_col == support_col) support = atof(field);
            if (current_col == stress_col) stress = atof(field);
            if (current_col == family_col) family = atof(field);
            if (current_col == peer_col) peer = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        development_sum += development;
        support_sum += support;
        stress_sum += stress;
        family_sum += family;
        peer_sum += peer;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", development_sum / count);
    printf("Mean ecological_support: %.4f\n", support_sum / count);
    printf("Mean ecological_stress: %.4f\n", stress_sum / count);
    printf("Mean current_family: %.4f\n", family_sum / count);
    printf("Mean current_peer: %.4f\n", peer_sum / count);
    return 0;
}
