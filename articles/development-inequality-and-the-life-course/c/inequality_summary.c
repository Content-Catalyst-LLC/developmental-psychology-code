#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 16384

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s data/life_course_inequality_panel.csv\n", argv[0]);
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

    int score_col = -1, resources_col = -1, burden_col = -1, col = 0;
    char *token = strtok(line, ",");

    while (token != NULL) {
        token[strcspn(token, "\r\n")] = 0;
        if (strcmp(token, "development_score") == 0) score_col = col;
        if (strcmp(token, "current_resources") == 0) resources_col = col;
        if (strcmp(token, "current_burden") == 0) burden_col = col;
        token = strtok(NULL, ",");
        col++;
    }

    if (score_col < 0 || resources_col < 0 || burden_col < 0) {
        fprintf(stderr, "Required columns not found\n");
        fclose(fp);
        return 1;
    }

    long count = 0;
    double score_sum = 0.0, resources_sum = 0.0, burden_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        int current_col = 0;
        double score = 0.0, resources = 0.0, burden = 0.0;
        char *field = strtok(line, ",");

        while (field != NULL) {
            if (current_col == score_col) score = atof(field);
            if (current_col == resources_col) resources = atof(field);
            if (current_col == burden_col) burden = atof(field);
            field = strtok(NULL, ",");
            current_col++;
        }

        count++;
        score_sum += score;
        resources_sum += resources;
        burden_sum += burden;
    }

    fclose(fp);

    printf("Rows analyzed: %ld\n", count);
    printf("Mean development_score: %.4f\n", score_sum / count);
    printf("Mean current_resources: %.4f\n", resources_sum / count);
    printf("Mean current_burden: %.4f\n", burden_sum / count);
    return 0;
}
