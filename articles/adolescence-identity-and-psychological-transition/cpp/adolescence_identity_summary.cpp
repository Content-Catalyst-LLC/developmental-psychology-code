#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
std::vector<std::string> split(const std::string& s){ std::vector<std::string> v; std::stringstream ss(s); std::string x; while(std::getline(ss,x,',')) v.push_back(x); return v; }
int idx(const std::vector<std::string>& h, const std::string& n){ for(size_t i=0;i<h.size();++i) if(h[i]==n) return (int)i; return -1; }
int main(int argc,char* argv[]){
  if(argc<2){ std::cerr<<"usage: adolescence_identity_summary data/adolescence_identity_panel.csv\\n"; return 1; }
  std::ifstream file(argv[1]); std::string line; std::getline(file,line); auto h=split(line);
  int s=idx(h,"identity_score"), c=idx(h,"support_context"), x=idx(h,"current_exclusion"), d=idx(h,"digital_stress");
  long n=0; double ss=0,cc=0,xx=0,dd=0;
  while(std::getline(file,line)){ auto v=split(line); ss+=std::stod(v[s]); cc+=std::stod(v[c]); xx+=std::stod(v[x]); dd+=std::stod(v[d]); n++; }
  std::cout<<"Rows analyzed: "<<n<<"\\nMean identity_score: "<<ss/n<<"\\nMean support_context: "<<cc/n<<"\\nMean current_exclusion: "<<xx/n<<"\\nMean digital_stress: "<<dd/n<<"\\n";
  return 0;
}
