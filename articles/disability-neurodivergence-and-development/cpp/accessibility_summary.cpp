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
        std::cerr << "Usage: accessibility_summary data/disability_neurodivergence_panel.csv\n";
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
    int participation_col = find_column(header, "participation_score");
    int access_col = find_column(header, "current_access");
    int barrier_col = find_column(header, "current_barrier");

    long count = 0;
    double development_sum = 0.0, participation_sum = 0.0, access_sum = 0.0, barrier_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= development_col || (int)values.size() <= participation_col || (int)values.size() <= access_col || (int)values.size() <= barrier_col) continue;
        development_sum += std::stod(values[development_col]);
        participation_sum += std::stod(values[participation_col]);
        access_sum += std::stod(values[access_col]);
        barrier_sum += std::stod(values[barrier_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean development_score: " << development_sum / count << "\n";
    std::cout << "Mean participation_score: " << participation_sum / count << "\n";
    std::cout << "Mean current_access: " << access_sum / count << "\n";
    std::cout << "Mean current_barrier: " << barrier_sum / count << "\n";
    return 0;
}
