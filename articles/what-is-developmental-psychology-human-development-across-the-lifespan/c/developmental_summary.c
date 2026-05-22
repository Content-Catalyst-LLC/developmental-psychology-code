#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 16384

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "usage: %s data/developmental_lifespan_panel.csv\n", argv[0]);
    return 1;
  }

  FILE *fp = fopen(argv[1], "r");
  if (!fp) { perror("open"); return 1; }

  char line[MAX_LINE];
  fgets(line, sizeof(line), fp);

  int score=-1, protective=-1, support=-1, stress=-1, intervention=-1, col=0;
  char *tok=strtok(line,",");
  while(tok){
    tok[strcspn(tok,"\r\n")]=0;
    if(!strcmp(tok,"development_score")) score=col;
    if(!strcmp(tok,"protective_context")) protective=col;
    if(!strcmp(tok,"current_support")) support=col;
    if(!strcmp(tok,"acute_stress")) stress=col;
    if(!strcmp(tok,"intervention")) intervention=col;
    tok=strtok(NULL,",");
    col++;
  }

  long n=0;
  double score_sum=0, protective_sum=0, support_sum=0, stress_sum=0, intervention_sum=0;

  while(fgets(line,sizeof(line),fp)){
    int c=0;
    char *f=strtok(line,",");
    double v_score=0,v_protective=0,v_support=0,v_stress=0,v_intervention=0;
    while(f){
      if(c==score) v_score=atof(f);
      if(c==protective) v_protective=atof(f);
      if(c==support) v_support=atof(f);
      if(c==stress) v_stress=atof(f);
      if(c==intervention) v_intervention=atof(f);
      f=strtok(NULL,",");
      c++;
    }
    n++;
    score_sum+=v_score;
    protective_sum+=v_protective;
    support_sum+=v_support;
    stress_sum+=v_stress;
    intervention_sum+=v_intervention;
  }

  fclose(fp);
  printf("Rows analyzed: %ld\n", n);
  printf("Mean development_score: %.4f\n", score_sum/n);
  printf("Mean protective_context: %.4f\n", protective_sum/n);
  printf("Mean current_support: %.4f\n", support_sum/n);
  printf("Mean acute_stress: %.4f\n", stress_sum/n);
  printf("Mean intervention: %.4f\n", intervention_sum/n);
  return 0;
}
