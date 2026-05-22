#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/regulation_development_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1, context=-1, sleep=-1, stress=-1, intervention=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"regulation_score")) score=col; if(!strcmp(tok,"regulatory_support_context")) context=col; if(!strcmp(tok,"current_sleep")) sleep=col; if(!strcmp(tok,"acute_stress")) stress=col; if(!strcmp(tok,"intervention_exposure")) intervention=col; tok=strtok(NULL,","); col++; }
  long n=0; double s1=0,s2=0,s3=0,s4=0,s5=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); while(f){ if(c==score) s1+=atof(f); if(c==context) s2+=atof(f); if(c==sleep) s3+=atof(f); if(c==stress) s4+=atof(f); if(c==intervention) s5+=atof(f); f=strtok(NULL,","); c++; } n++; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean regulation_score: %.4f\nMean regulatory_support_context: %.4f\nMean current_sleep: %.4f\nMean acute_stress: %.4f\nMean intervention_exposure: %.4f\n", n, s1/n, s2/n, s3/n, s4/n, s5/n);
  return 0;
}
