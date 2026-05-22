#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
std::vector<std::string> split(const std::string& s){ std::vector<std::string> v; std::stringstream ss(s); std::string x; while(std::getline(ss,x,',')) v.push_back(x); return v; }
int idx(const std::vector<std::string>& h, const std::string& n){ for(size_t i=0;i<h.size();++i) if(h[i]==n) return (int)i; return -1; }
int main(int argc,char* argv[]){
  if(argc<2){ std::cerr<<"usage: puberty_summary data/puberty_embodiment_panel.csv\n"; return 1; }
  std::ifstream file(argv[1]); std::string line; std::getline(file,line); auto h=split(line);
  int s=idx(h,"adjustment_score"), c=idx(h,"protective_context"), x=idx(h,"current_stigma"), b=idx(h,"current_body_concern"), p=idx(h,"current_peer_comparison");
  long n=0; double ss=0,cc=0,xx=0,bb=0,pp=0;
  while(std::getline(file,line)){ auto v=split(line); ss+=std::stod(v[s]); cc+=std::stod(v[c]); xx+=std::stod(v[x]); bb+=std::stod(v[b]); pp+=std::stod(v[p]); n++; }
  std::cout<<"Rows analyzed: "<<n<<"\nMean adjustment_score: "<<ss/n<<"\nMean protective_context: "<<cc/n<<"\nMean current_stigma: "<<xx/n<<"\nMean current_body_concern: "<<bb/n<<"\nMean current_peer_comparison: "<<pp/n<<"\n";
  return 0;
}
