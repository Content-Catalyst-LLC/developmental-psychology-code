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
        std::cerr << "Usage: design_summary data/developmental_design_panel.csv\n";
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
    int score_col = find_column(header, "development_score");
    int observed_col = find_column(header, "observed");
    int age_col = find_column(header, "age");

    if (score_col < 0 || observed_col < 0 || age_col < 0) {
        std::cerr << "Required columns not found\n";
        return 1;
    }

    long count = 0;
    double score_sum = 0.0;
    double age_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);

        if (
            static_cast<int>(values.size()) <= score_col ||
            static_cast<int>(values.size()) <= observed_col ||
            static_cast<int>(values.size()) <= age_col
        ) {
            continue;
        }

        int observed = std::stoi(values[observed_col]);
        if (observed != 1) {
            continue;
        }

        score_sum += std::stod(values[score_col]);
        age_sum += std::stod(values[age_col]);
        count += 1;
    }

    if (count == 0) {
        std::cerr << "No observed rows found\n";
        return 1;
    }

    std::cout << "Observed rows analyzed: " << count << "\n";
    std::cout << "Mean age: " << age_sum / count << "\n";
    std::cout << "Mean development_score: " << score_sum / count << "\n";

    return 0;
}
