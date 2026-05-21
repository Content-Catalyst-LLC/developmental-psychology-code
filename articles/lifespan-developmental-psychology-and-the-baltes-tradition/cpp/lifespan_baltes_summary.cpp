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
        std::cerr << "Usage: lifespan_baltes_summary data/lifespan_baltes_panel.csv\n";
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
    int gains_col = find_column(header, "gains");
    int losses_col = find_column(header, "losses");
    int soc_col = find_column(header, "soc_index");
    int support_col = find_column(header, "current_support");

    long count = 0;
    double development_sum = 0.0, gains_sum = 0.0, losses_sum = 0.0, soc_sum = 0.0, support_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= development_col || (int)values.size() <= gains_col || (int)values.size() <= losses_col || (int)values.size() <= soc_col || (int)values.size() <= support_col) continue;
        development_sum += std::stod(values[development_col]);
        gains_sum += std::stod(values[gains_col]);
        losses_sum += std::stod(values[losses_col]);
        soc_sum += std::stod(values[soc_col]);
        support_sum += std::stod(values[support_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << development_sum / count << "\n";
    std::cout << "Mean gains: " << gains_sum / count << "\n";
    std::cout << "Mean losses: " << losses_sum / count << "\n";
    std::cout << "Mean soc_index: " << soc_sum / count << "\n";
    std::cout << "Mean current_support: " << support_sum / count << "\n";
    return 0;
}
