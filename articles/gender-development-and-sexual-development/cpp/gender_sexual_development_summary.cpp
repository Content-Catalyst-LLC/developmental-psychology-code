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
        std::cerr << "Usage: gender_sexual_development_summary data/gender_sexual_development_panel.csv\n";
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
    int protective_col = find_column(header, "protective_context");
    int stigma_col = find_column(header, "current_stigma");
    int family_col = find_column(header, "current_family_support");
    int consent_col = find_column(header, "current_consent_knowledge");

    long count = 0;
    double adjustment_sum = 0.0, protective_sum = 0.0, stigma_sum = 0.0, family_sum = 0.0, consent_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if ((int)values.size() <= adjustment_col || (int)values.size() <= protective_col || (int)values.size() <= stigma_col || (int)values.size() <= family_col || (int)values.size() <= consent_col) continue;
        adjustment_sum += std::stod(values[adjustment_col]);
        protective_sum += std::stod(values[protective_col]);
        stigma_sum += std::stod(values[stigma_col]);
        family_sum += std::stod(values[family_col]);
        consent_sum += std::stod(values[consent_col]);
        count++;
    }

    std::cout << "Rows analyzed: " << count << "\n";
    std::cout << "Mean adjustment_score: " << adjustment_sum / count << "\n";
    std::cout << "Mean protective_context: " << protective_sum / count << "\n";
    std::cout << "Mean current_stigma: " << stigma_sum / count << "\n";
    std::cout << "Mean current_family_support: " << family_sum / count << "\n";
    std::cout << "Mean current_consent_knowledge: " << consent_sum / count << "\n";
    return 0;
}
