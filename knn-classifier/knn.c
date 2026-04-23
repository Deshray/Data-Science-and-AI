/*
 * knn.c — k-Nearest Neighbours Classifier Implementation
 *
 * CS 136 concepts demonstrated:
 *   S6  : opaque struct fully defined here, static helpers never in .h
 *   S8  : dynamic array with doubling strategy for training data
 *   S10 : qsort with dist_cmp comparator; void * for generic interface
 */

#include "knn.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>

/* ── Training example ─────────────────────────────────────────────────────── */

struct example {
    double *features;   /* heap-allocated feature vector */
    int     label;
};

/* ── Neighbour record (used during prediction) ────────────────────────────── */

struct neighbour {
    double dist;
    int    label;
};

/* ── Opaque model struct (S6/S8) ──────────────────────────────────────────── */

struct knn_model {
    int k;
    int n_features;

    /* Dynamic array of training examples — doubling strategy (S8) */
    struct example *examples;
    int             n_examples;
    int             capacity;
};

/* ── Module-scope constants ───────────────────────────────────────────────── */

#define INITIAL_CAPACITY 32

/* ── Static helpers (module scope — S6) ───────────────────────────────────── */

/*
 * squared_euclidean — sum of squared differences over n_features dimensions.
 * O(d) where d = n_features.
 */
static double squared_euclidean(const double *a,
                                 const double *b,
                                 int           d)
{
    double sum = 0.0;
    for (int i = 0; i < d; i++) {
        double diff = a[i] - b[i];
        sum += diff * diff;
    }
    return sum;
}

/*
 * neighbour_cmp — comparison function for qsort (S10).
 * Sorts neighbours by ascending distance.
 */
static int neighbour_cmp(const void *v0, const void *v1)
{
    const struct neighbour *n0 = (const struct neighbour *)v0;
    const struct neighbour *n1 = (const struct neighbour *)v1;
    if (n0->dist < n1->dist) return -1;
    if (n0->dist > n1->dist) return  1;
    return 0;
}

/*
 * majority_vote — return the most common label among the k neighbours.
 * Uses a simple counting pass — O(k).
 *
 * Ties are broken by choosing the label with the smallest index.
 */
static int majority_vote(const struct neighbour *neighbours,
                          int                    k)
{
    /* Find label range */
    int max_label = 0;
    for (int i = 0; i < k; i++)
        if (neighbours[i].label > max_label)
            max_label = neighbours[i].label;

    /* Count votes — heap-allocate count array */
    int *votes = calloc(max_label + 1, sizeof(int));
    if (!votes) return neighbours[0].label;

    for (int i = 0; i < k; i++)
        votes[neighbours[i].label]++;

    int best_label = 0, best_count = 0;
    for (int l = 0; l <= max_label; l++) {
        if (votes[l] > best_count) {
            best_count = votes[l];
            best_label = l;
        }
    }
    free(votes);
    return best_label;
}

/* ── Public API ───────────────────────────────────────────────────────────── */

struct knn_model *knn_create(int k, int n_features)
{
    if (k <= 0 || n_features <= 0) return NULL;

    struct knn_model *m = malloc(sizeof(struct knn_model));
    if (!m) return NULL;

    m->k          = k;
    m->n_features = n_features;
    m->n_examples = 0;
    m->capacity   = INITIAL_CAPACITY;

    /* Dynamic array — will double when full (S8) */
    m->examples = malloc(INITIAL_CAPACITY * sizeof(struct example));
    if (!m->examples) { free(m); return NULL; }

    return m;
}

void knn_destroy(struct knn_model *model)
{
    if (!model) return;

    /* Free each feature vector, then the dynamic array (S8) */
    for (int i = 0; i < model->n_examples; i++)
        free(model->examples[i].features);

    free(model->examples);
    free(model);
}

int knn_train(struct knn_model *model,
              const double     *features,
              int               label)
{
    if (!model || !features) return 0;

    /* Doubling strategy when capacity is full (S8) */
    if (model->n_examples == model->capacity) {
        int new_cap = model->capacity * 2;
        struct example *tmp = realloc(model->examples,
                                       new_cap * sizeof(struct example));
        if (!tmp) return 0;
        model->examples = tmp;
        model->capacity = new_cap;
    }

    /* Deep copy the feature vector onto the heap */
    double *feat_copy = malloc(model->n_features * sizeof(double));
    if (!feat_copy) return 0;
    memcpy(feat_copy, features, model->n_features * sizeof(double));

    model->examples[model->n_examples].features = feat_copy;
    model->examples[model->n_examples].label    = label;
    model->n_examples++;
    return 1;
}

int knn_predict(const struct knn_model *model, const double *query)
{
    if (!model || !query || model->n_examples == 0) return -1;

    int eff_k = model->k;
    if (eff_k > model->n_examples) eff_k = model->n_examples;

    /* Compute distances to all training points — O(n · d) */
    struct neighbour *neighbours = malloc(model->n_examples *
                                           sizeof(struct neighbour));
    if (!neighbours) return -1;

    for (int i = 0; i < model->n_examples; i++) {
        neighbours[i].dist  = squared_euclidean(query,
                                                 model->examples[i].features,
                                                 model->n_features);
        neighbours[i].label = model->examples[i].label;
    }

    /* Sort by distance — qsort with neighbour_cmp (S10) — O(n log n) */
    qsort(neighbours, model->n_examples, sizeof(struct neighbour),
          neighbour_cmp);

    /* Majority vote among k nearest (S7: O(k)) */
    int prediction = majority_vote(neighbours, eff_k);

    free(neighbours);
    return prediction;
}

double knn_evaluate(const struct knn_model *model,
                    const double           *features,
                    const int              *labels,
                    int                     n_test)
{
    if (!model || !features || !labels || n_test <= 0) return 0.0;

    int correct = 0;
    for (int i = 0; i < n_test; i++) {
        const double *q = features + (size_t)i * model->n_features;
        int pred = knn_predict(model, q);
        if (pred == labels[i]) correct++;
    }
    return (double)correct / n_test;
}

void knn_print_info(const struct knn_model *model)
{
    if (!model) return;
    printf("=== k-NN Model ============================\n");
    printf("  k            : %d\n", model->k);
    printf("  Features     : %d\n", model->n_features);
    printf("  Training pts : %d\n", model->n_examples);
    printf("  Capacity     : %d\n", model->capacity);
    printf("===========================================\n");
}
