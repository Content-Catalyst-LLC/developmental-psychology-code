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
        std::cerr << "Usage: wisdom_meaning_summary data/wisdom_meaning_later_life_panel.csv\n";
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

    int meaning_col = find_column(header, "meaning_score");
    int wisdom_col = find_column(header, "wisdom_index");
    int connection_col = find_column(header, "current_connection");
    int reflection_col = find_column(header, "current_reflection");
    int health_col = find_column(header, "current_health");

    long count = 0;
    double meaning_sum = 0.0, wisdom_sum = 0.0, connection_sum = 0.0, reflection_sum = 0.0, health_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= meaning_col || (int)values.size() <= wisdom_col || (int)values.size() <= connection_col || (int)values.size() <= reflection_col || (int)values.size() <= health_col) continue;
        meaning_sum += std::stod(values[meaning_col]);
        wisdom_sum += std::stod(values[wisdom_col]);
        connection_sum += std::stod(values[connection_col]);
        reflection_sum += std::stod(values[reflection_col]);
        health_sum += std::stod(values[health_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean meaning_score: " << meaning_sum / count << "\n";
    std::cout << "Mean wisdom_index: " << wisdom_sum / count << "\n";
    std::cout << "Mean current_connection: " << connection_sum / count << "\n";
    std::cout << "Mean current_reflection: " << reflection_sum / count << "\n";
    std::cout << "Mean current_health: " << health_sum / count << "\n";
    return 0;
}
