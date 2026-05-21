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
    std::cerr<<"usage: history_summary data/developmental_psychology_history_panel.csv\n";
    return 1;
  }

  std::ifstream file(argv[1]);
  std::string line;
  std::getline(file,line);
  auto h=split(line);

  int b=idx(h,"broadening_index"), l=idx(h,"lifespan_index"), e=idx(h,"ecological_systems_index"), c=idx(h,"critique_index");
  long n=0;
  double sb=0,sl=0,se=0,sc=0;

  while(std::getline(file,line)){
    auto v=split(line);
    sb+=std::stod(v[b]);
    sl+=std::stod(v[l]);
    se+=std::stod(v[e]);
    sc+=std::stod(v[c]);
    n++;
  }

  std::cout<<"Rows analyzed: "<<n<<"\n";
  std::cout<<"Mean broadening_index: "<<sb/n<<"\n";
  std::cout<<"Mean lifespan_index: "<<sl/n<<"\n";
  std::cout<<"Mean ecological_systems_index: "<<se/n<<"\n";
  std::cout<<"Mean critique_index: "<<sc/n<<"\n";
  return 0;
}
