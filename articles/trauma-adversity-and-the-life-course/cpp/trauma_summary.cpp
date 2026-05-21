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
        std::cerr << "Usage: trauma_summary data/trauma_life_course_panel.csv\n";
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
    int adversity_col = find_column(header, "current_adversity");
    int support_col = find_column(header, "current_support");

    if (score_col < 0 || adversity_col < 0 || support_col < 0) {
        std::cerr << "Required columns not found\n";
        return 1;
    }

    long count = 0;
    double score_sum = 0.0;
    double adversity_sum = 0.0;
    double support_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);

        if (
            static_cast<int>(values.size()) <= score_col ||
            static_cast<int>(values.size()) <= adversity_col ||
            static_cast<int>(values.size()) <= support_col
        ) {
            continue;
        }

        score_sum += std::stod(values[score_col]);
        adversity_sum += std::stod(values[adversity_col]);
        support_sum += std::stod(values[support_col]);
        count += 1;
    }

    if (count == 0) {
        std::cerr << "No valid rows found\n";
        return 1;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean adaptation_score: " << score_sum / count << "\n";
    std::cout << "Mean current_adversity: " << adversity_sum / count << "\n";
    std::cout << "Mean current_support: " << support_sum / count << "\n";

    return 0;
}
