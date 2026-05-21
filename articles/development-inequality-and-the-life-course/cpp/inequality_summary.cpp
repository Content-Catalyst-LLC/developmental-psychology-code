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
    for (size_t i = 0; i < header.size(); ++i) if (header[i] == name) return static_cast<int>(i);
    return -1;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: inequality_summary data/life_course_inequality_panel.csv\n";
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
    int resources_col = find_column(header, "current_resources");
    int burden_col = find_column(header, "current_burden");

    if (score_col < 0 || resources_col < 0 || burden_col < 0) {
        std::cerr << "Required columns not found\n";
        return 1;
    }

    long count = 0;
    double score_sum = 0.0, resources_sum = 0.0, burden_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= score_col || (int)values.size() <= resources_col || (int)values.size() <= burden_col) continue;
        score_sum += std::stod(values[score_col]);
        resources_sum += std::stod(values[resources_col]);
        burden_sum += std::stod(values[burden_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << score_sum / count << "\n";
    std::cout << "Mean current_resources: " << resources_sum / count << "\n";
    std::cout << "Mean current_burden: " << burden_sum / count << "\n";
    return 0;
}
