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
        std::cerr << "Usage: prenatal_development_summary data/prenatal_development_foundations_panel.csv\n";
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

    int outcome_col = find_column(header, "early_outcome");
    int care_col = find_column(header, "effective_care");
    int risk_col = find_column(header, "developmental_risk");
    int gestation_col = find_column(header, "gestational_weeks");
    int health_col = find_column(header, "maternal_health");

    long count = 0;
    double outcome_sum = 0.0, care_sum = 0.0, risk_sum = 0.0, gestation_sum = 0.0, health_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= outcome_col || (int)values.size() <= care_col || (int)values.size() <= risk_col || (int)values.size() <= gestation_col || (int)values.size() <= health_col) continue;
        outcome_sum += std::stod(values[outcome_col]);
        care_sum += std::stod(values[care_col]);
        risk_sum += std::stod(values[risk_col]);
        gestation_sum += std::stod(values[gestation_col]);
        health_sum += std::stod(values[health_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean early_outcome: " << outcome_sum / count << "\n";
    std::cout << "Mean effective_care: " << care_sum / count << "\n";
    std::cout << "Mean developmental_risk: " << risk_sum / count << "\n";
    std::cout << "Mean gestational_weeks: " << gestation_sum / count << "\n";
    std::cout << "Mean maternal_health: " << health_sum / count << "\n";
    return 0;
}
