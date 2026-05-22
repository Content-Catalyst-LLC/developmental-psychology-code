#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/play_development_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1, pretend=-1, social=-1, outdoor=-1, context=-1, restriction=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"development_score")) score=col; if(!strcmp(tok,"current_pretend")) pretend=col; if(!strcmp(tok,"current_social_play")) social=col; if(!strcmp(tok,"current_outdoor")) outdoor=col; if(!strcmp(tok,"play_support_context")) context=col; if(!strcmp(tok,"play_restriction")) restriction=col; tok=strtok(NULL,","); col++; }
  long n=0; double s1=0,s2=0,s3=0,s4=0,s5=0,s6=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); while(f){ if(c==score) s1+=atof(f); if(c==pretend) s2+=atof(f); if(c==social) s3+=atof(f); if(c==outdoor) s4+=atof(f); if(c==context) s5+=atof(f); if(c==restriction) s6+=atof(f); f=strtok(NULL,","); c++; } n++; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean development_score: %.4f\nMean current_pretend: %.4f\nMean current_social_play: %.4f\nMean current_outdoor: %.4f\nMean play_support_context: %.4f\nMean play_restriction: %.4f\n", n, s1/n, s2/n, s3/n, s4/n, s5/n, s6/n);
  return 0;
}
