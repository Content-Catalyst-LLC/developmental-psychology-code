#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> values;
    std::stringstream ss(line);
    std::string item;
    while (std::getline(ss, item, ',')) values.push_back(item);
    return values;
}

int find_column(const std::vector<std::string>& header, const std::string& name) {
    for (size_t i = 0; i < header.size(); ++i) {
        if (header[i] == name) return static_cast<int>(i);
    }
    return -1;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: psychopathology_summary data/developmental_psychopathology_panel.csv\n";
        return 1;
    }

    std::ifstream file(argv[1]);
    if (!file.is_open()) {
        std::cerr << "Unable to open CSV file\n";
        return 1;
    }

    std::string line;
    std::getline(file, line);
    auto header = split_csv_line(line);

    int score_col = find_column(header, "adaptation_score");
    int risk_col = find_column(header, "current_risk");
    int support_col = find_column(header, "current_support");

    long count = 0;
    double score_sum = 0.0, risk_sum = 0.0, support_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= score_col || (int)values.size() <= risk_col || (int)values.size() <= support_col) continue;
        score_sum += std::stod(values[score_col]);
        risk_sum += std::stod(values[risk_col]);
        support_sum += std::stod(values[support_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean adaptation_score: " << score_sum / count << "\n";
    std::cout << "Mean current_risk: " << risk_sum / count << "\n";
    std::cout << "Mean current_support: " << support_sum / count << "\n";
    return 0;
}
