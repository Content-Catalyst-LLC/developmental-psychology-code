#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> values;
    std::stringstream ss(line);
    std::string item;

    while (std::getline(ss, item, ',')) {
        values.push_back(item);
    }

    return values;
}

int find_column(const std::vector<std::string>& header, const std::string& name) {
    for (size_t i = 0; i < header.size(); ++i) {
        if (header[i] == name) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: timing_summary data/developmental_timing_panel.csv\n";
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
    int critical_col = find_column(header, "critical_outcome");
    int sensitive_col = find_column(header, "sensitive_outcome");
    int multi_col = find_column(header, "multi_window_outcome");

    if (critical_col < 0 || sensitive_col < 0 || multi_col < 0) {
        std::cerr << "Required outcome columns not found\n";
        return 1;
    }

    long count = 0;
    double critical_sum = 0.0;
    double sensitive_sum = 0.0;
    double multi_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);

        if (
            static_cast<int>(values.size()) <= critical_col ||
            static_cast<int>(values.size()) <= sensitive_col ||
            static_cast<int>(values.size()) <= multi_col
        ) {
            continue;
        }

        critical_sum += std::stod(values[critical_col]);
        sensitive_sum += std::stod(values[sensitive_col]);
        multi_sum += std::stod(values[multi_col]);
        count += 1;
    }

    if (count == 0) {
        std::cerr << "No valid rows found\n";
        return 1;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean critical_outcome: " << critical_sum / count << "\n";
    std::cout << "Mean sensitive_outcome: " << sensitive_sum / count << "\n";
    std::cout << "Mean multi_window_outcome: " << multi_sum / count << "\n";

    return 0;
}
