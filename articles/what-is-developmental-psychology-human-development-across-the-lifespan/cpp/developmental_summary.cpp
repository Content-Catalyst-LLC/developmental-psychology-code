#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string& s){
  std::vector<std::string> v;
  std::stringstream ss(s);
  std::string x;
  while(std::getline(ss,x,',')) v.push_back(x);
  return v;
}

int idx(const std::vector<std::string>& h, const std::string& n){
  for(size_t i=0;i<h.size();++i) if(h[i]==n) return (int)i;
  return -1;
}

int main(int argc,char* argv[]){
  if(argc<2){
    std::cerr<<"usage: developmental_summary data/developmental_lifespan_panel.csv\n";
    return 1;
  }

  std::ifstream file(argv[1]);
  std::string line;
  std::getline(file,line);
  auto h=split(line);

  int score=idx(h,"development_score"), protective=idx(h,"protective_context"), support=idx(h,"current_support"), stress=idx(h,"acute_stress"), intervention=idx(h,"intervention");

  long n=0;
  double score_sum=0, protective_sum=0, support_sum=0, stress_sum=0, intervention_sum=0;

  while(std::getline(file,line)){
    auto v=split(line);
    score_sum+=std::stod(v[score]);
    protective_sum+=std::stod(v[protective]);
    support_sum+=std::stod(v[support]);
    stress_sum+=std::stod(v[stress]);
    intervention_sum+=std::stod(v[intervention]);
    n++;
  }

  std::cout<<"Rows analyzed: "<<n<<"\n";
  std::cout<<"Mean development_score: "<<score_sum/n<<"\n";
  std::cout<<"Mean protective_context: "<<protective_sum/n<<"\n";
  std::cout<<"Mean current_support: "<<support_sum/n<<"\n";
  std::cout<<"Mean acute_stress: "<<stress_sum/n<<"\n";
  std::cout<<"Mean intervention: "<<intervention_sum/n<<"\n";
  return 0;
}
