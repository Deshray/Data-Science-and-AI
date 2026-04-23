"""
app.py — k-NN From Scratch: interactive Streamlit demo

Upload a labelled CSV dataset, choose feature columns and label column,
and interactively explore:
  • Optimal k selection via cross-validation
  • Classification report (accuracy, precision, recall, F1 per class)
  • Decision boundary visualization (2D feature pairs)
  • Comparison of distance metrics
  • Prediction on custom input

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from knn import KNNClassifier

st.set_page_config(page_title="k-NN From Scratch", page_icon="🔵", layout="wide")
st.title("🔵 k-Nearest Neighbours — Implemented from Scratch")
st.caption("NumPy-based k-NN classifier with vectorised distance computation, "
           "cross-validation, and decision boundary visualisation. No sklearn for the core algorithm.")

# ── Dataset ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")
    data_source = st.radio("Dataset", ["Iris (built-in)", "Upload CSV"])

if data_source == "Iris (built-in)":
    from sklearn.datasets import load_iris
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["label"] = iris.target
    label_names = {i: n for i, n in enumerate(iris.target_names)}
    feature_cols = list(iris.feature_names)
    label_col = "label"
else:
    uploaded = st.file_uploader("Upload labelled CSV", type=["csv"])
    if not uploaded:
        st.info("Upload a CSV or switch to the Iris demo.")
        st.stop()
    df = pd.read_csv(uploaded)
    all_cols = df.columns.tolist()
    label_col = st.sidebar.selectbox("Label column", all_cols, index=len(all_cols)-1)
    feature_cols = st.sidebar.multiselect(
        "Feature columns",
        [c for c in all_cols if c != label_col],
        default=[c for c in all_cols if c != label_col][:4],
    )
    label_names = {v: str(v) for v in df[label_col].unique()}

with st.sidebar:
    k_val   = st.slider("k (neighbours)", 1, 25, 5)
    metric  = st.selectbox("Distance metric", ["euclidean", "manhattan", "minkowski"])
    test_sz = st.slider("Test split", 0.1, 0.4, 0.2, 0.05)
    scale   = st.checkbox("Standardise features", value=True)
    n_folds = st.slider("CV folds", 3, 10, 5)

# ── Prepare data ──────────────────────────────────────────────────────────────

if not feature_cols:
    st.warning("Select at least one feature column.")
    st.stop()

X = df[feature_cols].dropna().values.astype(float)
y = df.loc[df[feature_cols].notna().all(axis=1), label_col].values

# Encode labels to integers if needed
classes = np.unique(y)
if not np.issubdtype(y.dtype, np.integer):
    lbl_map = {c: i for i, c in enumerate(classes)}
    y = np.array([lbl_map[v] for v in y])
    label_names = {i: str(c) for i, c in enumerate(classes)}

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_sz, stratify=y, random_state=42
)

if scale:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

# ── Train & Evaluate ──────────────────────────────────────────────────────────

model = KNNClassifier(k=k_val, metric=metric)
model.fit(X_train, y_train)
report = model.classification_report(X_test, y_test)

st.header("📊 Classification Report")
mc1, mc2, mc3, mc4 = st.columns(4)
mc1.metric("Accuracy",         f"{report['accuracy']*100:.1f}%")
mc2.metric("Macro Precision",  f"{report['macro_precision']*100:.1f}%")
mc3.metric("Macro Recall",     f"{report['macro_recall']*100:.1f}%")
mc4.metric("Macro F1",         f"{report['macro_f1']*100:.1f}%")

rows = []
for cls_id, m in report["per_class"].items():
    rows.append({
        "Class":     label_names.get(cls_id, str(cls_id)),
        "Precision": f"{m['precision']*100:.1f}%",
        "Recall":    f"{m['recall']*100:.1f}%",
        "F1":        f"{m['f1']*100:.1f}%",
        "Support":   m["support"],
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Optimal k Selection ───────────────────────────────────────────────────────

st.header("🔍 Optimal k via Cross-Validation")

with st.spinner("Running cross-validation..."):
    k_results = KNNClassifier.select_k(
        X_train, y_train,
        k_range=range(1, min(26, len(X_train) // 2)),
        n_folds=n_folds,
        metric=metric,
    )

ks   = list(k_results["k_scores"].keys())
accs = list(k_results["k_scores"].values())

fig_k = go.Figure()
fig_k.add_trace(go.Scatter(x=ks, y=[a * 100 for a in accs],
                             mode="lines+markers",
                             line=dict(color="#4C72B0", width=2),
                             marker=dict(size=6)))
fig_k.add_vline(x=k_results["best_k"], line_dash="dash",
                 line_color="red",
                 annotation_text=f"Best k={k_results['best_k']} ({k_results['best_acc']*100:.1f}%)")
fig_k.update_layout(xaxis_title="k", yaxis_title="CV Accuracy (%)",
                     height=350, margin=dict(t=20, b=20, l=20, r=20))
st.plotly_chart(fig_k, use_container_width=True)
st.info(f"Best k = **{k_results['best_k']}**  |  CV accuracy = **{k_results['best_acc']*100:.1f}%**")

# ── Metric Comparison ─────────────────────────────────────────────────────────

st.header("📐 Distance Metric Comparison")

metric_rows = []
for m in KNNClassifier.METRICS:
    mod = KNNClassifier(k=k_val, metric=m)
    mod.fit(X_train, y_train)
    acc = mod.score(X_test, y_test)
    metric_rows.append({"Metric": m, "Test Accuracy": f"{acc*100:.1f}%"})

st.dataframe(pd.DataFrame(metric_rows), hide_index=True, use_container_width=False)

# ── Decision Boundary (2D) ────────────────────────────────────────────────────

if len(feature_cols) >= 2:
    st.header("🗺️ Decision Boundary (2D Projection)")

    fc1, fc2 = feature_cols[0], feature_cols[1]
    f1_idx, f2_idx = feature_cols.index(fc1), feature_cols.index(fc2)

    db_model = KNNClassifier(k=k_val, metric=metric)
    X_2d_train = X_train[:, [f1_idx, f2_idx]]
    X_2d_test  = X_test[:,  [f1_idx, f2_idx]]
    db_model.fit(X_2d_train, y_train)

    xx, yy, Z = db_model.decision_boundary_grid(
        np.vstack([X_2d_train, X_2d_test]), resolution=120
    )

    palette = px.colors.qualitative.Plotly
    fig_db  = go.Figure()

    # Background (decision regions)
    fig_db.add_trace(go.Contour(
        x=xx[0], y=yy[:, 0], z=Z,
        colorscale=[[i/(len(classes)-1), palette[i % len(palette)]]
                    for i in range(len(classes))],
        opacity=0.25, showscale=False,
        contours=dict(coloring="fill"),
    ))

    # Training and test points
    for split_X, split_y, symbol, name in [
        (X_2d_train, y_train, "circle", "Train"),
        (X_2d_test,  y_test,  "diamond", "Test"),
    ]:
        for cls_id in np.unique(split_y):
            mask = split_y == cls_id
            fig_db.add_trace(go.Scatter(
                x=split_X[mask, 0], y=split_X[mask, 1],
                mode="markers",
                marker=dict(symbol=symbol, size=9,
                             color=palette[int(cls_id) % len(palette)],
                             line=dict(width=1, color="black")),
                name=f"{name} — {label_names.get(cls_id, cls_id)}",
            ))

    fig_db.update_layout(
        xaxis_title=fc1, yaxis_title=fc2,
        height=480, margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig_db, use_container_width=True)
    st.caption(f"2D boundary using features: **{fc1}** vs **{fc2}** "
               f"(k={k_val}, {metric} distance)")

# ── Custom Prediction ─────────────────────────────────────────────────────────

st.header("🔮 Predict a Custom Point")

input_vals = []
cols_inp = st.columns(min(len(feature_cols), 4))
for i, feat in enumerate(feature_cols):
    col_mean = float(np.mean(X_train[:, i]))
    input_vals.append(
        cols_inp[i % 4].number_input(feat, value=round(col_mean, 3), step=0.1)
    )

query = np.array([input_vals])
pred  = model.predict(query)[0]
proba = model.predict_proba(query)[0]

st.success(f"**Predicted class:** {label_names.get(pred, pred)}")
vote_df = pd.DataFrame({
    "Class":       [label_names.get(c, c) for c in np.unique(model._y)],
    "Vote share":  [f"{p*100:.0f}%" for p in proba],
})
st.dataframe(vote_df, hide_index=True, use_container_width=False)
