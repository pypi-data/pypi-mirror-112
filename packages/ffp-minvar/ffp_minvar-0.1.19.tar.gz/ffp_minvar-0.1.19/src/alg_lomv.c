#include "../include/alg_lomv.h"

double linf(int d, gsl_vector * a, gsl_vector * b){
    double max = 0;
    for(int i=0; i<d; i++){
        double diff = fabs(gsl_vector_get(a, i) - gsl_vector_get(b, i));
        if (diff > max){
            max = diff;
        }
    }
    return max;
}


// Slides 16  "Define psi." Name declaration slightly different.
/* 21. 
    def psi(theta):
    chi = Dinv * (ones >= B @ theta)
    b = B.T @ chi  # q-1
    A = Vinv + (B.T @ np.diag(chi)) @ B
    return solve(A,b)
*/
// p-q : 500-4 from .py
// theta: q-1, 4-1
// B: p-q, 500-4
// V: q-q, 4-4
// Delta: p-p, 500-500. But D passed in here is 500-1 for ease of inverse
// modify(return): x: q-1, 4-1

// ** use unsigned int (x)
// ** pass in delta as vector of all diagnoals. Saved memory.
void psi(int p, int q, gsl_vector * theta, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta, gsl_vector * x){
    gsl_vector *  B_theta = gsl_vector_alloc(p);
    gsl_vector * comparison = gsl_vector_alloc(p);
    gsl_vector * chi = gsl_vector_alloc(p);
    gsl_vector * b = gsl_vector_alloc(q);;

    // B_theta: B @ theta
    // p-1
    gsl_blas_dgemv(CblasNoTrans, 1.0, B, theta, 0.0, B_theta);

    // comparison: ones >= B @ theta
    // p-1
    for(int i=0; i<p; i++){
        double value = (1 >= gsl_vector_get(B_theta, i)) ? 1.0:0.0; // change to 1.0 for formal use
        gsl_vector_set(comparison, i, value);
    }

    // D is diagonal, so Dinv is just 1/diag
    gsl_matrix * Dinv = gsl_matrix_alloc(p, p);
    gsl_matrix_set_zero(Dinv);
    for(int i=0; i<p; i++){
        double diag_inv = 1/gsl_vector_get(Delta, i);
        gsl_matrix_set(Dinv, i, i, diag_inv);
    }

    // chi = Dinv * (ones >= B @ theta)
    // p-1
    gsl_blas_dgemv(CblasNoTrans, 1.0, Dinv, comparison, 0.0, chi);

    // b = B.T @ chi
    // q-1
    gsl_blas_dgemv(CblasTrans, 1.0, B, chi, 0.0, b);

    // A = Vinv + (B.T @ np.diag(chi)) @ B
    // V memory will be modified by the gsl_linalg_LU_decomp. 
    int s;
    gsl_permutation * perm = gsl_permutation_alloc(q);
    gsl_matrix * Vinv = gsl_matrix_alloc(q, q);
    gsl_linalg_LU_decomp(V, perm, &s);
    gsl_linalg_LU_invert(V, perm, Vinv);

    // B.T @ np.diag(chi)
    gsl_matrix * temp1 = gsl_matrix_alloc(q, p);
    gsl_matrix * chi_D = gsl_matrix_alloc(p, p);
    gsl_matrix_set_zero(chi_D);
    for(int i=0; i<p; i++){
        gsl_matrix_set(chi_D, i, i, gsl_vector_get(chi, i));
    }
    gsl_blas_dgemm(CblasTrans, CblasNoTrans, 1.0, B, chi_D, 0.0, temp1);

    // ~ @ B
    gsl_matrix * temp2 = gsl_matrix_alloc(q, q);
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, temp1, B, 0.0, temp2);
    
    //gsl_matrix_fprintf(stdout, temp1, "%g");
    //gsl_matrix_fprintf(stdout, temp2, "%g");
    //printf("-------------------\n");

    // the sum will be stored in Vinv. A is in fact Vinv.
    gsl_matrix_add(Vinv, temp2);

    // Use gsl_linalg_lU_decomp + gsl_linalg_lu_solve. (BLAS gsl_blas_dtrsv?)
    gsl_linalg_LU_decomp(Vinv, perm, &s);
    gsl_linalg_LU_solve(Vinv, perm, b, x);

    //free all created matrices and vectors
    gsl_vector_free(B_theta);
    gsl_vector_free(comparison);
    gsl_vector_free(chi);
    gsl_vector_free(b);
    gsl_matrix_free(Dinv);
    gsl_permutation_free(perm);
    gsl_matrix_free(Vinv);
    gsl_matrix_free(temp1);
    gsl_matrix_free(chi_D);
    gsl_matrix_free(temp2);

}


/* 22.
    def compute_fixed_point (t):
        s = t + 2 * tol
        while (norm(s - t) > tol * norm(s)):
            t = s
            s = psi(t)

        return(s)
*/

// 1. An ffp function that only returns theta so far. 
//    or actually, not returning anything...
// theta: q-1
// B: p-q
// V: q-q
// Delta: p-p
// return: q-1
gsl_vector * ffp(int p, int q, gsl_vector * theta, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta){
    int i;
    //  th_old = t0 - np.inf
    gsl_vector * th_old = gsl_vector_alloc(q);
    gsl_vector_set_zero(th_old);
    for(i=0; i<q;i++){
        gsl_vector_set(th_old, i, gsl_vector_get(theta, i) - INFINITY);
    } 

    //  th_new = t0
    gsl_vector * th_new = gsl_vector_alloc(q);
    gsl_vector_memcpy(th_new, theta);

    while(linf(q, th_new, th_old) > pow(10, -15)){ // 1e-15
        // free space before assign new values
        gsl_vector_memcpy(th_old, th_new);

        // th_new = psi(th_old)
        // ** memory issue ****
        // ** Just pass in th_new to psi. Work on the th_new memory from psi. No need to return double pointer.
        psi(p ,q, th_old, B, V, Delta, th_new);
    }

    gsl_vector_free(th_old);
    return th_new;
}


// Slides 11 eq. For verifying theorem1.
/* 23. 
    def lo_weights ():
        theta = psi (np.zeros(q))
        // w is a fixed point of psi, i.e., w = psi(w)
        w = Dinv @ maximum(ones - B @ theta, 0)

        // unique solution x = w/<w, e>
        return w / sum(w)
*/
/* INPUT: 
   OUTPUT: w/sum(w). p-1
   x: p-1
   B: p-q
   V: q-q
   Delta: p-p
   theta: q-1
*/

gsl_vector * lo_minvar(int p, int q, gsl_matrix * B, gsl_matrix * V, gsl_vector * Delta){
    int i;
    // theta = psi (np.zeros(q))
    gsl_vector * zeros = gsl_vector_alloc(q);
    gsl_vector_set_zero(zeros);
    gsl_vector * theta = ffp(p, q, zeros, B, V, Delta);
    // w = Dinv @ maximum(ones - B @ theta, 0)
    // B @ theta
    gsl_vector *  B_theta = gsl_vector_alloc(p);
    gsl_blas_dgemv(CblasNoTrans, 1.0, B, theta, 0.0, B_theta);

    // maximum(ones - B @ theta, 0)
    gsl_vector * maximum = gsl_vector_alloc(p);
    for(i=0; i<p; i++){
        double value = (1 > gsl_vector_get(B_theta, i)) ? (1 - gsl_vector_get(B_theta, i)):0.0;
        gsl_vector_set(maximum, i, value);
    }

    // w = Dinv @ maximum
    gsl_matrix * Dinv = gsl_matrix_alloc(p, p);
    gsl_matrix_set_zero(Dinv);
    for(i=0; i<p; i++){
        double diag_inv = 1/gsl_vector_get(Delta, i);
        gsl_matrix_set(Dinv, i, i, diag_inv);
    }

    gsl_vector * w = gsl_vector_alloc(p);
    gsl_blas_dgemv(CblasNoTrans, 1.0, Dinv, maximum, 0.0, w);

    // w = w/sum(w)

    double sum = 0;
    for(i=0; i<p; i++){
        sum += gsl_vector_get(w, i);
    }
    //absolute sum: gsl_blas_dasum(w); 
    gsl_vector_scale(w, 1/sum);

    // free space
    gsl_vector_free(zeros);
    gsl_vector_free(theta);
    gsl_vector_free(B_theta);
    gsl_vector_free(maximum);
    gsl_matrix_free(Dinv);

    return w;
}




// --------------------------- Interface for Python data transfer ----------------------------- //
// -------------------------------------------------------------------------------------------- //

double * ffp_C_interface(int p, int q, double* theta, double** B, double** V, double* Delta){
    gsl_vector * gsl_theta = gsl_vector_alloc(q);
    gsl_matrix * gsl_B = gsl_matrix_alloc(p, q);
    gsl_matrix * gsl_V = gsl_matrix_alloc(q, q);
    gsl_vector * gsl_Delta = gsl_vector_alloc(p);
    int i,j;
    for(i=0; i<q; i++){
        gsl_vector_set(gsl_theta, i, theta[i]);
    } 
    for(i=0; i<p; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_B, i, j, B[i][j]);
        }
    }
    for(i=0; i<q; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_V, i, j, V[i][j]);
        }
    }
    for(i=0; i<p; i++){
        gsl_vector_set(gsl_Delta, i, Delta[i]);
    } 

    gsl_vector * th = ffp(p, q, gsl_theta, gsl_B, gsl_V, gsl_Delta);
    
    // convert x from gsl_vector to double*
    double * th_py = malloc(q * sizeof(double));
    for(i=0; i<q; i++){
        th_py[i] = gsl_vector_get(th, i);
    }
    gsl_vector_free(th);
    return th_py;
}


double* lo_minvar_C_interface(int p, int q, double**B, double** V, double* Delta){
    gsl_matrix * gsl_B = gsl_matrix_alloc(p, q);
    gsl_matrix * gsl_V = gsl_matrix_alloc(q, q);
    gsl_vector * gsl_Delta = gsl_vector_alloc(p);
    int i,j;
    for(i=0; i<p; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_B, i, j, B[i][j]);
        }
    }
    for(i=0; i<q; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_V, i, j, V[i][j]);
        }
    }
    for(i=0; i<p; i++){
        gsl_vector_set(gsl_Delta, i, Delta[i]);
    } 
    gsl_vector * x = lo_minvar(p, q, gsl_B, gsl_V, gsl_Delta);

    /*
    printf("------------- x ------------------\n");
    gsl_vector_fprintf(stdout, x, "%g");*/

    // convert x from gsl_vector to double*
    double * x_py = malloc(p * sizeof(double));
    for(i=0; i<p; i++){
        x_py[i] = gsl_vector_get(x, i);
    }
    gsl_vector_free(x);
    return x_py;

}

double* psi_C_interface(int p, int q, double**B, double** V, double* Delta){
    gsl_vector * zeros = gsl_vector_alloc(q);
    gsl_vector_set_zero(zeros);
    gsl_matrix * gsl_B = gsl_matrix_alloc(p, q);
    gsl_matrix * gsl_V = gsl_matrix_alloc(q, q);
    gsl_vector * gsl_Delta = gsl_vector_alloc(p);
    int i,j;
    for(i=0; i<p; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_B, i, j, B[i][j]);
        }
    }
    for(i=0; i<q; i++){
        for(j=0; j<q; j++){
            gsl_matrix_set(gsl_V, i, j, V[i][j]);
        }
    }
    for(i=0; i<p; i++){
        gsl_vector_set(gsl_Delta, i, Delta[i]);
    } 

    gsl_vector * w = gsl_vector_alloc(q);

    psi(p,q, zeros, gsl_B, gsl_V, gsl_Delta, w);

    gsl_vector_free(zeros);
    gsl_matrix_free(gsl_B);
    gsl_matrix_free(gsl_V);
    gsl_vector_free(gsl_Delta);

    /*
    printf("----------------- w -------------------\n");
    gsl_vector_fprintf(stdout, w, "%g");*/

    // convert w from gsl_vector to double*
    double * w_py = malloc(q * sizeof(double));
    for(i=0; i<q; i++){
        w_py[i] = gsl_vector_get(w, i);
    }
    gsl_vector_free(w);
    return w_py;

}

/* 
phi(theta) = V @ B.T @ Dinv @ maximum(ones - B @ theta, 0)      //slides 11
psi(theta) = Ainv @ b                                           //slides 16    
*/