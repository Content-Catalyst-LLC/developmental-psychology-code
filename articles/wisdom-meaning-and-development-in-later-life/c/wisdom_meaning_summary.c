#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/wisdom_meaning_later_life_panel.csv\n", argv[0]);
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

    int meaning_col = -1, wisdom_col = -1, connection_col = -1, reflection_col = -1, health_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "meaning_score") == 0) meaning_col = col;
        if (strcmp(token, "wisdom_index") == 0) wisdom_col = col;
        if (strcmp(token, "current_connection") == 0) connection_col = col;
        if (strcmp(token, "current_reflection") == 0) reflection_col = col;
        if (strcmp(token, "current_health") == 0) health_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (meaning_col < 0 || wisdom_col < 0 || connection_col < 0 || reflection_col < 0 || health_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double meaning_sum = 0.0, wisdom_sum = 0.0, connection_sum = 0.0, reflection_sum = 0.0, health_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double meaning = 0.0, wisdom = 0.0, connection = 0.0, reflection = 0.0, health = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == meaning_col) meaning = atof(field);
            if (current_col == wisdom_col) wisdom = atof(field);
            if (current_col == connection_col) connection = atof(field);
            if (current_col == reflection_col) reflection = atof(field);
            if (current_col == health_col) health = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        meaning_sum += meaning;
        wisdom_sum += wisdom;
        connection_sum += connection;
        reflection_sum += reflection;
        health_sum += health;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean meaning_score: %.4f\n", meaning_sum / count);
    printf("Mean wisdom_index: %.4f\n", wisdom_sum / count);
    printf("Mean current_connection: %.4f\n", connection_sum / count);
    printf("Mean current_reflection: %.4f\n", reflection_sum / count);
    printf("Mean current_health: %.4f\n", health_sum / count);
    return 0;
}
