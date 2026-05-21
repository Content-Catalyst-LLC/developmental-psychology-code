#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/schooling_development_panel.csv\n", argv[0]);
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

    int development_col = -1, connectedness_col = -1, teacher_col = -1, peer_col = -1, stress_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) development_col = col;
        if (strcmp(token, "connectedness_score") == 0) connectedness_col = col;
        if (strcmp(token, "current_teacher") == 0) teacher_col = col;
        if (strcmp(token, "current_peer") == 0) peer_col = col;
        if (strcmp(token, "current_stress") == 0) stress_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (development_col < 0 || connectedness_col < 0 || teacher_col < 0 || peer_col < 0 || stress_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double development_sum = 0.0, connectedness_sum = 0.0, teacher_sum = 0.0, peer_sum = 0.0, stress_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double development = 0.0, connectedness = 0.0, teacher = 0.0, peer = 0.0, stress = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == development_col) development = atof(field);
            if (current_col == connectedness_col) connectedness = atof(field);
            if (current_col == teacher_col) teacher = atof(field);
            if (current_col == peer_col) peer = atof(field);
            if (current_col == stress_col) stress = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        development_sum += development;
        connectedness_sum += connectedness;
        teacher_sum += teacher;
        peer_sum += peer;
        stress_sum += stress;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", development_sum / count);
    printf("Mean connectedness_score: %.4f\n", connectedness_sum / count);
    printf("Mean current_teacher: %.4f\n", teacher_sum / count);
    printf("Mean current_peer: %.4f\n", peer_sum / count);
    printf("Mean current_stress: %.4f\n", stress_sum / count);
    return 0;
}
