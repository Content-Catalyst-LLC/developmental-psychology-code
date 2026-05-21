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

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: development_summary data/developmental_panel.csv\n";
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
    int score_col = -1;

    for (size_t i = 0; i < header.size(); ++i) {
        if (header[i] == "development_score") {
            score_col = static_cast<int>(i);
            break;
        }
    }

    if (score_col < 0) {
        std::cerr << "development_score column not found\n";
        return 1;
    }

    long count = 0;
    double sum = 0.0;
    double min_score = 1e18;
    double max_score = -1e18;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);

        if (static_cast<int>(values.size()) <= score_col) {
            continue;
        }

        double score = std::stod(values[score_col]);
        sum += score;
        count += 1;

        if (score < min_score) {
            min_score = score;
        }

        if (score > max_score) {
            max_score = score;
        }
    }

    if (count == 0) {
        std::cerr << "No valid rows found\n";
        return 1;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << sum / count << "\n";
    std::cout << "Minimum development_score: " << min_score << "\n";
    std::cout << "Maximum development_score: " << max_score << "\n";

    return 0;
}
