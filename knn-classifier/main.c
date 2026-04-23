/*
 * main.c — k-NN Classifier: Iris dataset demo + test suite
 *
 * Trains a k-NN classifier on a subset of the Iris dataset
 * and evaluates accuracy on a held-out test set.
 */

#include "knn.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static int tests_run = 0, tests_passed = 0, tests_failed = 0;

#define CHECK(expr, msg) \
    do { \
        tests_run++; \
        if (expr) { tests_passed++; printf("  [PASS] %s\n", msg); } \
        else      { tests_failed++; printf("  [FAIL] %s (line %d)\n", msg, __LINE__); } \
    } while (0)

/* ── Iris dataset (subset: 30 train, 12 test, 4 features, 3 classes) ──────── */
/* Features: sepal_length, sepal_width, petal_length, petal_width           */
/* Labels:   0=setosa, 1=versicolor, 2=virginica                            */

static double train_X[30][4] = {
    {5.1,3.5,1.4,0.2}, {4.9,3.0,1.4,0.2}, {4.7,3.2,1.3,0.2},
    {5.0,3.6,1.4,0.2}, {5.4,3.9,1.7,0.4}, {4.6,3.4,1.4,0.3},
    {5.0,3.4,1.5,0.2}, {4.4,2.9,1.4,0.2}, {4.9,3.1,1.5,0.1},
    {5.4,3.7,1.5,0.2},
    /* versicolor */
    {7.0,3.2,4.7,1.4}, {6.4,3.2,4.5,1.5}, {6.9,3.1,4.9,1.5},
    {5.5,2.3,4.0,1.3}, {6.5,2.8,4.6,1.5}, {5.7,2.8,4.5,1.3},
    {6.3,3.3,4.7,1.6}, {4.9,2.4,3.3,1.0}, {6.6,2.9,4.6,1.3},
    {5.2,2.7,3.9,1.4},
    /* virginica */
    {6.3,3.3,6.0,2.5}, {5.8,2.7,5.1,1.9}, {7.1,3.0,5.9,2.1},
    {6.3,2.9,5.6,1.8}, {6.5,3.0,5.8,2.2}, {7.6,3.0,6.6,2.1},
    {4.9,2.5,4.5,1.7}, {7.3,2.9,6.3,1.8}, {6.7,2.5,5.8,1.8},
    {7.2,3.6,6.1,2.5}
};
static int train_y[30] = {
    0,0,0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,1,1,
    2,2,2,2,2,2,2,2,2,2
};

static double test_X[12][4] = {
    {5.1,3.8,1.5,0.3}, {5.7,3.8,1.7,0.3}, {5.1,3.8,1.5,0.3},
    {5.4,3.4,1.7,0.2},
    {5.1,2.5,3.0,1.1}, {5.7,2.8,4.1,1.3}, {6.2,2.9,4.3,1.3},
    {5.1,2.9,4.5,1.5},
    {6.5,3.2,5.1,2.0}, {6.4,2.7,5.3,1.9}, {6.8,3.0,5.5,2.1},
    {5.7,2.5,5.0,2.0}
};
static int test_y[12] = { 0,0,0,0, 1,1,1,1, 2,2,2,2 };

/* ── Tests ────────────────────────────────────────────────────────────────── */

static void run_tests(void)
{
    printf("\n--- Basic API ---\n");

    struct knn_model *m = knn_create(3, 4);
    CHECK(m != NULL, "knn_create(3, 4) returns non-NULL");

    knn_print_info(m);

    printf("\n--- Training ---\n");
    int ok = 1;
    for (int i = 0; i < 30; i++)
        if (!knn_train(m, train_X[i], train_y[i])) { ok = 0; break; }
    CHECK(ok, "30 training examples loaded successfully");

    printf("\n--- Prediction ---\n");
    /* Clear setosa: petal_length < 2 */
    double setosa_q[4]      = {5.0, 3.4, 1.4, 0.2};
    double versicolor_q[4]  = {6.0, 2.7, 4.2, 1.4};
    double virginica_q[4]   = {6.5, 3.1, 5.5, 2.0};

    CHECK(knn_predict(m, setosa_q)     == 0, "setosa query → class 0");
    CHECK(knn_predict(m, versicolor_q) == 1, "versicolor query → class 1");
    CHECK(knn_predict(m, virginica_q)  == 2, "virginica query → class 2");

    printf("\n--- Evaluation ---\n");
    double acc = knn_evaluate(m, (const double *)test_X, test_y, 12);
    printf("  Test accuracy (k=3): %.1f%%\n", acc * 100.0);
    CHECK(acc >= 0.80, "accuracy >= 80% on Iris test set");

    printf("\n--- k comparison ---\n");
    for (int k = 1; k <= 7; k += 2) {
        struct knn_model *mk = knn_create(k, 4);
        for (int i = 0; i < 30; i++) knn_train(mk, train_X[i], train_y[i]);
        double a = knn_evaluate(mk, (const double *)test_X, test_y, 12);
        printf("  k=%d  accuracy=%.1f%%\n", k, a * 100.0);
        knn_destroy(mk);
    }

    printf("\n--- Boundary Conditions ---\n");
    CHECK(knn_create(0, 4) == NULL, "knn_create(k=0) returns NULL");
    CHECK(knn_create(3, 0) == NULL, "knn_create(n_features=0) returns NULL");
    CHECK(knn_predict(m, NULL) == -1, "predict(NULL query) returns -1");

    knn_destroy(m);
    CHECK(1, "knn_destroy does not crash");

    knn_destroy(NULL);
    CHECK(1, "knn_destroy(NULL) does not crash");

    /* Doubling strategy: load >32 examples */
    struct knn_model *md = knn_create(1, 1);
    for (int i = 0; i < 100; i++) {
        double f = (double)i;
        knn_train(md, &f, i % 3);
    }
    knn_print_info(md);
    CHECK(1, "doubling strategy: 100 examples loaded without crash");
    knn_destroy(md);
}

int main(void)
{
    printf("========================================\n");
    printf("   k-NN Classifier — Test Suite\n");
    printf("========================================\n");

    run_tests();

    printf("\n========================================\n");
    printf("  Results: %d/%d passed", tests_passed, tests_run);
    if (tests_failed > 0) printf("  (%d FAILED)", tests_failed);
    printf("\n========================================\n");

    return tests_failed > 0 ? 1 : 0;
}
