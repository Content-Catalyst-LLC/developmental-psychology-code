#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/disability_neurodivergence_panel.csv\n", argv[0]);
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

    int development_col = -1, participation_col = -1, access_col = -1, barrier_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) development_col = col;
        if (strcmp(token, "participation_score") == 0) participation_col = col;
        if (strcmp(token, "current_access") == 0) access_col = col;
        if (strcmp(token, "current_barrier") == 0) barrier_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (development_col < 0 || participation_col < 0 || access_col < 0 || barrier_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double development_sum = 0.0, participation_sum = 0.0, access_sum = 0.0, barrier_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double development = 0.0, participation = 0.0, access = 0.0, barrier = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == development_col) development = atof(field);
            if (current_col == participation_col) participation = atof(field);
            if (current_col == access_col) access = atof(field);
            if (current_col == barrier_col) barrier = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        development_sum += development;
        participation_sum += participation;
        access_sum += access;
        barrier_sum += barrier;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", development_sum / count);
    printf("Mean participation_score: %.4f\n", participation_sum / count);
    printf("Mean current_access: %.4f\n", access_sum / count);
    printf("Mean current_barrier: %.4f\n", barrier_sum / count);
    return 0;
}
