#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
std::vector<std::string> split(const std::string& s){ std::vector<std::string> v; std::stringstream ss(s); std::string x; while(std::getline(ss,x,',')) v.push_back(x); return v; }
int idx(const std::vector<std::string>& h, const std::string& n){ for(size_t i=0;i<h.size();++i) if(h[i]==n) return (int)i; return -1; }
int main(int argc,char* argv[]){
  if(argc<2){ std::cerr<<"usage: brain_development_summary data/brain_development_panel.csv\n"; return 1; }
  std::ifstream file(argv[1]); std::string line; std::getline(file,line); auto h=split(line);
  std::vector<int> cols={idx(h,"neural_state"),idx(h,"developmental_outcome"),idx(h,"acute_stress"),idx(h,"developmental_support_context")};
  std::vector<std::string> names={"neural_state","developmental_outcome","acute_stress","developmental_support_context"};
  std::vector<double> sums(cols.size(),0.0); long n=0;
  while(std::getline(file,line)){ auto v=split(line); for(size_t j=0;j<cols.size();++j) sums[j]+=std::stod(v[cols[j]]); n++; }
  std::cout<<"Rows analyzed: "<<n<<"\n"; for(size_t j=0;j<names.size();++j) std::cout<<"Mean "<<names[j]<<": "<<sums[j]/n<<"\n"; return 0;
}
