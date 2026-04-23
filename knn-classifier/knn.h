/*
 * knn.h — k-Nearest Neighbours Classifier in C
 *
 * A generic k-NN classifier using void * (S10) for the feature vectors.
 * Training data stored in a dynamic array with the doubling strategy (S8).
 * Neighbour sorting uses qsort with a custom distance comparator (S10).
 * The knn_model type is an opaque struct (S6/S8).
 *
 * CS 136 concepts used:
 *   S6  — opaque struct, .h/.c module design, static helpers
 *   S7  — O(n·d) prediction complexity analysis
 *   S8  — dynamic array with doubling strategy, malloc/free/realloc
 *   S10 — qsort with generic comparator for neighbour sorting
 */

#ifndef KNN_H
#define KNN_H

#include <stddef.h>

/* Opaque model type (S6/S8) */
struct knn_model;

/*
 * knn_create — initialise an empty k-NN model.
 *   k         : number of neighbours to use in voting
 *   n_features: dimensionality of each feature vector
 *
 * Returns heap-allocated model, or NULL on failure.
 * effects: allocates heap memory [caller must call knn_destroy]
 */
struct knn_model *knn_create(int k, int n_features);

/* Free all heap memory. No-op on NULL. */
void knn_destroy(struct knn_model *model);

/*
 * knn_train — add one labelled training example.
 *   features : array of n_features doubles
 *   label    : integer class label (e.g. 0, 1, 2)
 *
 * Returns 1 on success, 0 on allocation failure.
 * Time: amortized O(1) per call (doubling strategy).
 * effects: may realloc internal storage
 */
int knn_train(struct knn_model *model,
              const double *features,
              int label);

/*
 * knn_predict — predict the class label for a query point.
 *   query : array of n_features doubles
 *
 * Returns the majority class label among the k nearest neighbours.
 * Uses Euclidean distance and plurality voting.
 * Time: O(n · d + n log n) where n = training size, d = n_features.
 */
int knn_predict(const struct knn_model *model, const double *query);

/*
 * knn_evaluate — compute accuracy on a labelled test set.
 *   features : 2D array [n_test][n_features]
 *   labels   : ground-truth labels [n_test]
 *   n_test   : number of test examples
 *
 * Returns fraction correct in [0, 1].
 */
double knn_evaluate(const struct knn_model *model,
                    const double *features,
                    const int    *labels,
                    int           n_test);

/*
 * knn_print_info — print model configuration and training size.
 */
void knn_print_info(const struct knn_model *model);

#endif /* KNN_H */
