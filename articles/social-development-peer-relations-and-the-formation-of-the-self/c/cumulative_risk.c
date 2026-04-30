#include <stdio.h>

// Toy cumulative-risk adjustment model.
// Compile with: cc c/cumulative_risk.c -o outputs/cumulative_risk

double developmental_functioning(double support, double opportunity, double regulation, double risk) {
    return 0.30 * support + 0.25 * opportunity + 0.25 * regulation - 0.20 * risk;
}

int main(void) {
    double score = developmental_functioning(0.80, 0.70, 0.65, 0.30);
    printf("Developmental functioning score: %.3f\n", score);
    return 0;
}
