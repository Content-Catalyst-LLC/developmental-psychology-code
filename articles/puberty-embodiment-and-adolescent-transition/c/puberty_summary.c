#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384
int main(int argc, char *argv[]) {
  if (argc < 2) { fprintf(stderr, "usage: %s data/puberty_embodiment_panel.csv\n", argv[0]); return 1; }
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 1; }
  char line[MAX_LINE]; fgets(line, sizeof(line), fp);
  int score=-1,protective=-1,stigma=-1,body=-1,peer=-1,col=0;
  char *tok=strtok(line,",");
  while(tok){ tok[strcspn(tok,"\r\n")]=0; if(!strcmp(tok,"adjustment_score")) score=col; if(!strcmp(tok,"protective_context")) protective=col; if(!strcmp(tok,"current_stigma")) stigma=col; if(!strcmp(tok,"current_body_concern")) body=col; if(!strcmp(tok,"current_peer_comparison")) peer=col; tok=strtok(NULL,","); col++; }
  long n=0; double ss=0,cc=0,xx=0,bb=0,pp=0;
  while(fgets(line,sizeof(line),fp)){ int c=0; char *f=strtok(line,","); double a=0,d=0,x=0,b=0,p=0; while(f){ if(c==score)a=atof(f); if(c==protective)d=atof(f); if(c==stigma)x=atof(f); if(c==body)b=atof(f); if(c==peer)p=atof(f); f=strtok(NULL,","); c++; } n++; ss+=a; cc+=d; xx+=x; bb+=b; pp+=p; }
  fclose(fp);
  printf("Rows analyzed: %ld\nMean adjustment_score: %.4f\nMean protective_context: %.4f\nMean current_stigma: %.4f\nMean current_body_concern: %.4f\nMean current_peer_comparison: %.4f\n", n, ss/n, cc/n, xx/n, bb/n, pp/n);
  return 0;
}
