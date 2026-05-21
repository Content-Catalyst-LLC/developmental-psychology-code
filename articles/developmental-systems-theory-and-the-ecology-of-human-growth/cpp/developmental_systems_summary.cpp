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
        std::cerr << "Usage: developmental_systems_summary data/developmental_systems_panel.csv\n";
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
    int support_col = find_column(header, "ecological_support");
    int stress_col = find_column(header, "ecological_stress");
    int family_col = find_column(header, "current_family");
    int peer_col = find_column(header, "current_peer");

    long count = 0;
    double development_sum = 0.0, support_sum = 0.0, stress_sum = 0.0, family_sum = 0.0, peer_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= development_col || (int)values.size() <= support_col || (int)values.size() <= stress_col || (int)values.size() <= family_col || (int)values.size() <= peer_col) continue;
        development_sum += std::stod(values[development_col]);
        support_sum += std::stod(values[support_col]);
        stress_sum += std::stod(values[stress_col]);
        family_sum += std::stod(values[family_col]);
        peer_sum += std::stod(values[peer_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << development_sum / count << "\n";
    std::cout << "Mean ecological_support: " << support_sum / count << "\n";
    std::cout << "Mean ecological_stress: " << stress_sum / count << "\n";
    std::cout << "Mean current_family: " << family_sum / count << "\n";
    std::cout << "Mean current_peer: " << peer_sum / count << "\n";
    return 0;
}
