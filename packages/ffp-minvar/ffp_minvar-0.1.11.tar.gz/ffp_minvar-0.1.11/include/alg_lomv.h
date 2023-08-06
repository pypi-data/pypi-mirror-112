#ifndef ALG_LOMV
#define ALG_LOMV

#include "string.h"
#include "assert.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_permutation.h>
#include <gsl/gsl_linalg.h>


double linf(int d, gsl_vector * a, gsl_vector * b);

void psi(int p, int q, gsl_vector * theta, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta, gsl_vector * x);

gsl_vector * ffp(int p, int q, gsl_vector * theta, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta);

gsl_vector * lo_minvar(int p, int q, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta);

double * ffp_C_interface(int p, int q, double* theta, double** B, double** V, double* Delta);

double* lo_minvar_C_interface(int p, int q, double**B, double** V, double* Delta);

double* psi_C_interface(int p, int q, double**B, double** V, double* Delta);

#endif
