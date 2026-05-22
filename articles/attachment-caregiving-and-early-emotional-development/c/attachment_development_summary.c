#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/attachment_development_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1, care=-1, repair=-1, stress=-1, context=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"regulation_score")) score=col; if(!strcmp(tok,"current_care")) care=col; if(!strcmp(tok,"current_repair")) repair=col; if(!strcmp(tok,"current_stress")) stress=col; if(!strcmp(tok,"caregiving_support_context")) context=col; tok=strtok(NULL,","); col++; }
  long n=0; double s1=0,s2=0,s3=0,s4=0,s5=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); while(f){ if(c==score) s1+=atof(f); if(c==care) s2+=atof(f); if(c==repair) s3+=atof(f); if(c==stress) s4+=atof(f); if(c==context) s5+=atof(f); f=strtok(NULL,","); c++; } n++; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean regulation_score: %.4f\nMean current_care: %.4f\nMean current_repair: %.4f\nMean current_stress: %.4f\nMean caregiving_support_context: %.4f\n", n, s1/n, s2/n, s3/n, s4/n, s5/n);
  return 0;
}
