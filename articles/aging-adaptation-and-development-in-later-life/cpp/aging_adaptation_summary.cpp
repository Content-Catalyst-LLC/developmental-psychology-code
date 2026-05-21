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
        std::cerr << "Usage: aging_adaptation_summary data/aging_adaptation_later_life_panel.csv\n";
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

    int adjustment_col = find_column(header, "adjustment_score");
    int fit_col = find_column(header, "functional_fit");
    int support_col = find_column(header, "current_support");
    int health_col = find_column(header, "current_health");
    int adaptation_col = find_column(header, "current_adaptation");

    long count = 0;
    double adjustment_sum = 0.0, fit_sum = 0.0, support_sum = 0.0, health_sum = 0.0, adaptation_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= adjustment_col || (int)values.size() <= fit_col || (int)values.size() <= support_col || (int)values.size() <= health_col || (int)values.size() <= adaptation_col) continue;
        adjustment_sum += std::stod(values[adjustment_col]);
        fit_sum += std::stod(values[fit_col]);
        support_sum += std::stod(values[support_col]);
        health_sum += std::stod(values[health_col]);
        adaptation_sum += std::stod(values[adaptation_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean adjustment_score: " << adjustment_sum / count << "\n";
    std::cout << "Mean functional_fit: " << fit_sum / count << "\n";
    std::cout << "Mean current_support: " << support_sum / count << "\n";
    std::cout << "Mean current_health: " << health_sum / count << "\n";
    std::cout << "Mean current_adaptation: " << adaptation_sum / count << "\n";
    return 0;
}
