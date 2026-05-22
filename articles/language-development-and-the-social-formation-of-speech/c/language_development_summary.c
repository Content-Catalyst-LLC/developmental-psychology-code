#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/language_development_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1, interaction=-1, reading=-1, joint=-1, turns=-1, context=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"language_score")) score=col; if(!strcmp(tok,"current_interaction")) interaction=col; if(!strcmp(tok,"current_reading")) reading=col; if(!strcmp(tok,"current_joint_attention")) joint=col; if(!strcmp(tok,"current_turn_taking")) turns=col; if(!strcmp(tok,"language_support_context")) context=col; tok=strtok(NULL,","); col++; }
  long n=0; double s1=0,s2=0,s3=0,s4=0,s5=0,s6=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); while(f){ if(c==score) s1+=atof(f); if(c==interaction) s2+=atof(f); if(c==reading) s3+=atof(f); if(c==joint) s4+=atof(f); if(c==turns) s5+=atof(f); if(c==context) s6+=atof(f); f=strtok(NULL,","); c++; } n++; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean language_score: %.4f\nMean current_interaction: %.4f\nMean current_reading: %.4f\nMean current_joint_attention: %.4f\nMean current_turn_taking: %.4f\nMean language_support_context: %.4f\n", n, s1/n, s2/n, s3/n, s4/n, s5/n, s6/n);
  return 0;
}
