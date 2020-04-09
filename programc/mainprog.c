#include <stdio.h>
#include <stdlib.h>
#include "matriks.h"
#include <time.h>
#define Gs 100000
#define T 0.0005

typedef struct component{
  char type;
  int node1; // (-)
  int node2; // (+)
  float val;
} cmp;

int n_comp, n_nodes;
float t;

// Debugging tool cek Netlist
// void printNet(cmp *arr){
//   cmp temp;
//   printf("Jenis\tKoneksi\tNilai\n");
//   for (int i = 0; i < n_comp; i++){
//     temp = *(arr+i);
//     printf("%c \t%d-%d \t%f\n", temp.type, temp.node1, temp.node2, temp.val);
//   }
// }

void getConductance(cmp *arr, float **conductance){
  int i;
  cmp temp;

  for (i = 0; i < n_comp; i++){
    temp = arr[i];
    float Geq = 0;
    // printf("%d\n", i);

    if ((temp.type) == 'c'){
      Geq = temp.val/T;
    }
    else if ((temp.type) == 'r'){
      Geq = 1/temp.val;
    }
    else if ((temp.type) == 'v'){
      Geq = Gs;
    }

    if (temp.node1 != 0 && temp.node2 != 0){
      conductance[temp.node1 - 1][temp.node1 - 1] += Geq;
      conductance[temp.node1 - 1][temp.node2 - 1] += Geq * -1;
      conductance[temp.node2 - 1][temp.node1 - 1] += Geq * -1;
      conductance[temp.node2 - 1][temp.node2 - 1] += Geq;
    }
    else if (temp.node1 == 0){
      conductance[temp.node2 - 1][temp.node2 - 1] += Geq;
    }
    else {
      conductance[temp.node1 - 1][temp.node1 - 1] += Geq;
    }
  }
}

// Debugging tool
// void printEquation (float *rhs, float *v, float **conductance){
//   for (int i = 0; i < n_nodes; i++){
//     printf("[");
//     for (int j = 0; j < n_nodes; j++){
//       printf("%8.2f ", conductance[i][j]);
//     }
//     printf("] ");
//     printf("[v[%d]]\t [%8.2f] \n", i+1, rhs[i]);
//   }
// }

void getRHS(cmp *arr, float *rhs, float *v){
  int i;
  cmp temp;

  for (int j = 0; j < n_nodes; j++){
    rhs[j] = 0;
  }

  for (i = 0; i < n_comp; i++){
    temp = arr[i];
    float rhs_val = 0;
    // printf("%d\n", i);

    if ((temp.type) == 'c'){
      // Kapasitor bertindak seperti sumber tegangan polar, dengan node2
      // adalah node positif.
      if (temp.node1 != 0 && temp.node2 != 0){
        rhs_val = temp.val * (v[temp.node2-1] - v[temp.node1-1]) / T;
        rhs[temp.node1 - 1] += rhs_val * -1;
        rhs[temp.node2 - 1] += rhs_val;
      }
      else if (temp.node1 == 0){
        rhs_val = (temp.val / T) * v[temp.node2 - 1];
        rhs[temp.node2 - 1] += rhs_val;
      }
      else {
        rhs_val = (temp.val  / T) * v[temp.node1 - 1];
        rhs[temp.node1 - 1] += rhs_val;
      }
    }

    else if ((temp.type) == 'v'){
      rhs_val = Gs * temp.val;
      // Node 2 Positif dan node1 Negatif
      if (temp.node1 != 0 && temp.node2 != 0){
        rhs[temp.node1 - 1] += rhs_val * -1;
        rhs[temp.node2 - 1] += rhs_val;
      }
      else if (temp.node1 == 0){
        rhs[temp.node2 - 1] = rhs_val;
      }
      else {
        rhs[temp.node1 - 1] = -rhs_val;
      }
    }
  }
}

int main(){
  FILE *fp;
  fp = fopen("../interface/netlist.txt", "r");
  fscanf(fp, "%d %d ", &n_nodes, &n_comp);

  cmp* arrComp = (cmp*)malloc(sizeof(cmp)*n_comp);

  for (int i = 0; i < n_comp; i++){
    cmp temp;
    fscanf(fp, " %c %d %d %f ", &temp.type, &temp.node1, &temp.node2, &temp.val);
    arrComp[i] = temp;
  }
  fscanf(fp, "%f", &t);
  // printNet(arrComp);
  float *rhs = (float*)malloc((n_nodes)*sizeof(float));
  float *vi = (float*)malloc((n_nodes)*sizeof(float));
  float **conductance = (float**)malloc(n_nodes*sizeof(float*));
  for (int i = 0; i < n_nodes; i++){
    conductance[i] = (float*)malloc(n_nodes*sizeof(float));
  }

  float **conductanceInv = (float**)malloc(n_nodes*sizeof(float*));
  for (int i = 0; i < n_nodes; i++){
    conductanceInv[i] = (float*)malloc(n_nodes*sizeof(float));
  }

  getConductance(arrComp, conductance);
  inverseMatrix(conductance, conductanceInv, n_nodes);


  // Get Initial Condition
  // getRHS(arrComp, rhs, vi);
  // multMatrix(conductanceInv, rhs, vf, n_nodes);
  // updateV(vf, vi, n_nodes);
  FILE *fout;
  fout = fopen("../interface/output.csv", "w");

  // Header output file
  fprintf(fout, "time");
  for (int i = 0; i < n_nodes; i++){
    fprintf(fout, ",v_%d", i+1);
  }
  for (int p = 0; p < n_nodes-1; p++){
  fprintf(fout, ",i_%d", p+1);
  } 
  fprintf(fout, "\n");

  for (int i = 0; i <= (t/T); i++){
    fprintf(fout, "%.5f", i*T);
    for (int j = 0; j < n_nodes; j++){
      fprintf(fout, ",%.5f", vi[j]);
    }
    for (int p = 1; p <= n_nodes-1; p++){
      fprintf(fout, ",%.5f", ((double)(vi[p-1]-vi[p])/(double)arrComp[1].val)*1000); //buat arus
    }  

    getRHS(arrComp, rhs, vi);
    multMatrix(conductanceInv, rhs, vi, n_nodes);
    fprintf(fout, "\n");
  }
}
