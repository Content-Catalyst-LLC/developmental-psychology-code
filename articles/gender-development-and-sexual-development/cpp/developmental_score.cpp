#include <iostream>

// Toy developmental functioning model.
// Compile with: g++ cpp/developmental_score.cpp -o outputs/developmental_score

int main() {
    double biological = 0.70;
    double caregiving = 0.80;
    double opportunity = 0.65;
    double self_regulation = 0.60;
    double resilience = 0.70;
    double risk = 0.30;

    double score =
        0.15 * biological +
        0.20 * caregiving +
        0.18 * opportunity +
        0.18 * self_regulation +
        0.16 * resilience -
        0.20 * risk;

    std::cout << "Developmental score: " << score << "\n";
    return 0;
}
