#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "usage: %s data/developmental_psychology_history_panel.csv\n", argv[0]);
    return 1;
  }

  FILE *fp = fopen(argv[1], "r");
  if (!fp) { perror("open"); return 1; }

  char line[MAX_LINE];
  fgets(line, sizeof(line), fp);

  int b=-1,l=-1,e=-1,c=-1,col=0;
  char *tok=strtok(line,",");
  while(tok){
    tok[strcspn(tok,"\r\n")]=0;
    if(!strcmp(tok,"broadening_index")) b=col;
    if(!strcmp(tok,"lifespan_index")) l=col;
    if(!strcmp(tok,"ecological_systems_index")) e=col;
    if(!strcmp(tok,"critique_index")) c=col;
    tok=strtok(NULL,",");
    col++;
  }

  long n=0;
  double sb=0,sl=0,se=0,sc=0;

  while(fgets(line,sizeof(line),fp)){
    int cc=0;
    char *f=strtok(line,",");
    double vb=0,vl=0,ve=0,vc=0;
    while(f){
      if(cc==b) vb=atof(f);
      if(cc==l) vl=atof(f);
      if(cc==e) ve=atof(f);
      if(cc==c) vc=atof(f);
      f=strtok(NULL,",");
      cc++;
    }
    n++;
    sb+=vb; sl+=vl; se+=ve; sc+=vc;
  }

  fclose(fp);
  printf("Rows analyzed: %ld\n", n);
  printf("Mean broadening_index: %.4f\n", sb/n);
  printf("Mean lifespan_index: %.4f\n", sl/n);
  printf("Mean ecological_systems_index: %.4f\n", se/n);
  printf("Mean critique_index: %.4f\n", sc/n);
  return 0;
}
