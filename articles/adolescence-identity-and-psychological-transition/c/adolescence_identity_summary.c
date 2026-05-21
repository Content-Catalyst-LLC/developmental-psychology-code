#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/adolescence_identity_panel.csv\\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1,support=-1,exclusion=-1,digital=-1,col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\\r\\n")]=0; if(!strcmp(tok,"identity_score")) score=col; if(!strcmp(tok,"support_context")) support=col; if(!strcmp(tok,"current_exclusion")) exclusion=col; if(!strcmp(tok,"digital_stress")) digital=col; tok=strtok(NULL,","); col++; }
  long n=0; double ss=0,cc=0,xx=0,dd=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); double a=0,b=0,x=0,d=0; while(f){ if(c==score)a=atof(f); if(c==support)b=atof(f); if(c==exclusion)x=atof(f); if(c==digital)d=atof(f); f=strtok(NULL,","); c++; } n++; ss+=a; cc+=b; xx+=x; dd+=d; }
  fclose(fp);
  printf("Rows analyzed: %ld\\nMean identity_score: %.4f\\nMean support_context: %.4f\\nMean current_exclusion: %.4f\\nMean digital_stress: %.4f\\n", n, ss/n, cc/n, xx/n, dd/n);
  return 0;
}
