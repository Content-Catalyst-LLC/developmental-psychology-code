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
        std::cerr << "Usage: plasticity_summary data/genes_environment_plasticity_panel.csv\n";
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

    int development_col = find_column(header, "development_score");
    int stress_col = find_column(header, "embedded_stress");
    int support_col = find_column(header, "embedded_support");
    int care_col = find_column(header, "current_care");
    int current_stress_col = find_column(header, "current_stress");

    long count = 0;
    double development_sum = 0.0, stress_sum = 0.0, support_sum = 0.0, care_sum = 0.0, current_stress_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= development_col || (int)values.size() <= stress_col || (int)values.size() <= support_col || (int)values.size() <= care_col || (int)values.size() <= current_stress_col) continue;
        development_sum += std::stod(values[development_col]);
        stress_sum += std::stod(values[stress_col]);
        support_sum += std::stod(values[support_col]);
        care_sum += std::stod(values[care_col]);
        current_stress_sum += std::stod(values[current_stress_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << development_sum / count << "\n";
    std::cout << "Mean embedded_stress: " << stress_sum / count << "\n";
    std::cout << "Mean embedded_support: " << support_sum / count << "\n";
    std::cout << "Mean current_care: " << care_sum / count << "\n";
    std::cout << "Mean current_stress: " << current_stress_sum / count << "\n";
    return 0;
}
