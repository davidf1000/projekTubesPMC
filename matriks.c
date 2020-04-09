#include "matriks.h"
#include <stdlib.h>
#include <stdio.h>

void inverseMatrix(float** src, float** dest, int n){
  float ratio, a, matrix[10][10];
  int i, j, k;
  for(i = 0; i < n; i++){
      for(j = 0; j < n; j++){
          matrix[i][j] = src[i][j];
      }
  }
  for(i = 0; i < n; i++){
      for(j = n; j < 2*n; j++){
          if(i==(j-n))
              matrix[i][j] = 1.0;
          else
              matrix[i][j] = 0.0;
      }
  }
  for(i = 0; i < n; i++){
      for(j = 0; j < n; j++){
          if(i!=j){
              ratio = matrix[j][i]/matrix[i][i];
              for(k = 0; k < 2*n; k++){
                  matrix[j][k] -= ratio * matrix[i][k];
              }
          }
      }
  }
  for(i = 0; i < n; i++){
      a = matrix[i][i];
      for(j = 0; j < 2*n; j++){
          matrix[i][j] /= a;
      }
  }
  for(i = 0; i < n; i++){
      for(j = n; j < 2*n; j++){
          dest[i][j-n] = matrix[i][j];
      }
  }
}

void multMatrix(float** src1, float *src2, float* dest, int n){
  int i, j;
  float temp;
  for (i = 0; i < n; i++){
    temp = 0;
    for (j = 0; j < n; j++){
      temp += src1[i][j] * src2[j];
    }
    dest[i] = temp;
  }
}

void updateV(float* src, float* dest, int n){
  for (int i = 0; i < n; i++){
    dest[i] = src[i];
  }
}
