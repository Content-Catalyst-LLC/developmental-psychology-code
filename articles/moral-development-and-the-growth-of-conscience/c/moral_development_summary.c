#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/moral_development_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int conscience=-1, action=-1, context=-1, exclusion=-1, pressure=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"conscience_score")) conscience=col; if(!strcmp(tok,"moral_action_score")) action=col; if(!strcmp(tok,"moral_support_context")) context=col; if(!strcmp(tok,"current_exclusion")) exclusion=col; if(!strcmp(tok,"peer_pressure")) pressure=col; tok=strtok(NULL,","); col++; }
  long n=0; double s1=0,s2=0,s3=0,s4=0,s5=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); while(f){ if(c==conscience) s1+=atof(f); if(c==action) s2+=atof(f); if(c==context) s3+=atof(f); if(c==exclusion) s4+=atof(f); if(c==pressure) s5+=atof(f); f=strtok(NULL,","); c++; } n++; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean conscience_score: %.4f\nMean moral_action_score: %.4f\nMean moral_support_context: %.4f\nMean current_exclusion: %.4f\nMean peer_pressure: %.4f\n", n, s1/n, s2/n, s3/n, s4/n, s5/n);
  return 0;
}
