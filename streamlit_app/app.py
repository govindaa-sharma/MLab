import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_BASE = "https://mlab-thit.onrender.com"

st.set_page_config(
    page_title="MLab Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080c14;
    color: #e2e8f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem; }

section[data-testid="stSidebar"] {
    background: #0d1321 !important;
    border-right: 1px solid rgba(99,179,237,0.12);
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 10px;
    padding: 14px 16px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(99,179,237,0.35);
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    opacity: 0.6;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
}

[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
}

[data-testid="stButton"] button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover {
    opacity: 0.85 !important;
    box-shadow: 0 4px 16px rgba(56,189,248,0.3) !important;
}

/* Invisible overlay buttons for experiment cards */
.card-btn-wrapper [data-testid="stButton"] button {
    opacity: 0 !important;
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: unset !important;
    padding: 0 !important;
    margin: 0 !important;
    cursor: pointer !important;
    z-index: 10 !important;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(99,179,237,0.1) !important;
    margin: 1.2rem 0 !important;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    border-left: 3px solid #38bdf8;
    padding-left: 10px;
    margin-bottom: 0;
}
.badge-healthy {
    display: inline-block;
    background: rgba(52,211,153,0.12);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.06em;
}
.badge-issue {
    display: inline-block;
    background: rgba(248,113,113,0.12);
    color: #f87171;
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.06em;
}
.exp-id-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #38bdf8;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 6px;
    padding: 3px 10px;
}
.copilot-answer {
    background: #111827;
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 10px;
    padding: 16px 18px;
    font-size: 13px;
    line-height: 1.75;
    color: #94a3b8;
    margin-top: 12px;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}
.header-brand {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #e2e8f0;
    margin-bottom: 0;
}
.header-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    color: #475569;
    text-transform: uppercase;
    margin-top: 2px;
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #38bdf8;
    box-shadow: 0 0 10px #38bdf8;
    margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def fetch_experiments():
    try:
        res = requests.get(f"{API_BASE}/experiments/", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Could not reach backend: {e}")
        return []


@st.cache_data(ttl=30)
def fetch_analysis(experiment_id):
    try:
        res = requests.get(f"{API_BASE}/experiments/{experiment_id}/analysis", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to load analysis: {e}")
        return None


@st.cache_data(ttl=30)
def fetch_metrics(experiment_id):
    try:
        res = requests.get(f"{API_BASE}/experiments/{experiment_id}/metrics", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to load metrics: {e}")
        return []


def ask_copilot(query, experiment_id):
    try:
        res = requests.post(
            f"{API_BASE}/copilot/query",
            json={"query": query, "experiment_id": experiment_id},
            timeout=15
        )
        res.raise_for_status()
        data = res.json()

        # Case 1: simple {"answer": "..."} string
        raw = data.get("answer", "")
        if isinstance(raw, str) and raw.strip():
            return raw

        # Case 2: answer is a list of content blocks
        # [{"type": "text", "text": "...", ...}, ...]
        if isinstance(raw, list):
            texts = [block["text"] for block in raw if block.get("type") == "text" and block.get("text")]
            return "\n\n".join(texts)

        # Case 3: the whole response IS a list of content blocks (no "answer" wrapper)
        if isinstance(data, list):
            texts = [block["text"] for block in data if block.get("type") == "text" and block.get("text")]
            return "\n\n".join(texts)

        return "No answer returned."

    except Exception as e:
        return f"Error contacting copilot: {e}"


def format_metrics(raw_metrics):
    if not raw_metrics:
        return pd.DataFrame()
    rows = {}
    for m in raw_metrics:
        step = m["step"]
        if step not in rows:
            rows[step] = {"step": step}
        rows[step][m["name"]] = m["value"]
    return pd.DataFrame(list(rows.values())).sort_values("step").reset_index(drop=True)


def get_status_color(status):
    s = (status or "").lower()
    if s in ("completed", "success"): return "#34d399"
    if s in ("failed", "error"):      return "#f87171"
    if s == "running":                return "#38bdf8"
    return "#475569"


def exp_name(exp):
    return exp.get("project") or exp.get("project_name") or exp.get("name") or "Unnamed"


# ── SESSION STATE DEFAULTS ────────────────────────────────────────────────────
if "selected_id"   not in st.session_state: st.session_state.selected_id   = None
if "sidebar_page"  not in st.session_state: st.session_state.sidebar_page  = 1
if "last_search"   not in st.session_state: st.session_state.last_search   = ""
if "copilot_answer" not in st.session_state: st.session_state.copilot_answer = ""


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:1.5rem;padding-bottom:1rem;
            border-bottom:1px solid rgba(99,179,237,0.1);'>
  <div class='header-brand'>
    <span class='live-dot'></span>MLab
    <span style='color:#38bdf8;font-weight:400;'> Dashboard</span>
  </div>
  <div class='header-sub'>Experiment Tracker · v1.0</div>
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<p class='section-label'>Experiments</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    experiments = fetch_experiments()

    if not experiments:
        st.warning("No experiments found. Is the backend running?")
        st.stop()

    # Set default selection
    if st.session_state.selected_id is None:
        st.session_state.selected_id = experiments[0]["id"]

    # ── SEARCH ──
    search = st.text_input(
        "search",
        placeholder="🔍  Search by ID or project…",
        label_visibility="collapsed",
        key="search_box"
    )

    # Reset page when search changes
    if search != st.session_state.last_search:
        st.session_state.sidebar_page = 1
        st.session_state.last_search = search

    # Filter
    def matches(exp):
        q = search.strip().lower()
        if not q:
            return True
        return q in str(exp["id"]).lower() or q in exp_name(exp).lower()

    filtered = [e for e in experiments if matches(e)]

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── EXPERIMENT CARDS ──
    page_size   = 8
    total_pages = max(1, -(-len(filtered) // page_size))
    page        = max(1, min(st.session_state.sidebar_page, total_pages))
    paginated   = filtered[(page - 1) * page_size : page * page_size]

    if not paginated:
        st.markdown(
            "<p style='font-family:DM Mono,monospace;font-size:11px;"
            "color:#475569;'>No experiments match your search.</p>",
            unsafe_allow_html=True
        )
    else:
        for exp in paginated:
            name      = exp_name(exp)
            status    = exp.get("status") or ""
            exp_id    = exp["id"]
            is_sel    = st.session_state.selected_id == exp_id
            s_color   = get_status_color(status)
            card_bg   = "rgba(56,189,248,0.08)" if is_sel else "#111827"
            card_bdr  = "rgba(56,189,248,0.5)"  if is_sel else "rgba(99,179,237,0.1)"
            id_color  = "#38bdf8"               if is_sel else "#475569"

            # Card HTML
            st.markdown(f"""
            <div style='
                background:{card_bg};
                border:1px solid {card_bdr};
                border-radius:10px;
                padding:10px 14px;
                margin-bottom:2px;
                position:relative;
            '>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-family:DM Mono,monospace;font-size:10px;
                                 color:{id_color};letter-spacing:0.08em;'>#{exp_id}</span>
                    <span style='font-size:9px;color:{s_color};font-family:DM Mono,monospace;
                                 text-transform:uppercase;letter-spacing:0.06em;'>{status}</span>
                </div>
                <div style='font-size:12px;color:#e2e8f0;margin-top:4px;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>
                    {name}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Transparent click button
            if st.button("_", key=f"exp_btn_{exp_id}", use_container_width=True):
                st.session_state.selected_id    = exp_id
                st.session_state.copilot_answer = ""   # clear old answer on switch
                st.rerun()

    # ── PAGINATION ──
    st.markdown("<br>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1, 2, 1])

    with p1:
        if st.button("←", key="prev_page", use_container_width=True):
            st.session_state.sidebar_page = max(1, page - 1)
            st.rerun()

    with p2:
        st.markdown(
            f"<p style='text-align:center;font-family:DM Mono,monospace;"
            f"font-size:10px;color:#475569;margin:6px 0;'>{page} / {total_pages}</p>",
            unsafe_allow_html=True
        )

    with p3:
        if st.button("→", key="next_page", use_container_width=True):
            st.session_state.sidebar_page = min(total_pages, page + 1)
            st.rerun()

    st.markdown(
        f"<p style='font-family:DM Mono,monospace;font-size:10px;"
        f"color:#475569;margin-top:4px;'>{len(filtered)} experiment(s)</p>",
        unsafe_allow_html=True
    )


# ── MAIN PANEL ────────────────────────────────────────────────────────────────
selected_id = st.session_state.selected_id

if not selected_id:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;
                justify-content:center;padding:100px 20px;color:#475569;text-align:center;'>
      <div style='font-size:40px;margin-bottom:12px;opacity:0.4;'>◈</div>
      <p style='font-family:DM Mono,monospace;font-size:12px;'>
        Select an experiment from the sidebar
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

analysis = fetch_analysis(selected_id)

if analysis:
    sig  = analysis.get("signals",     {})
    diag = analysis.get("diagnostics", {})

    # ID tag
    st.markdown(
        f"<span class='exp-id-tag'>exp #{analysis.get('experiment_id', selected_id)}</span>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── SIGNALS ──
    st.markdown("<p class='section-label'>Signals</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Primary Metric",   sig.get("primary_metric",    "—"))
    c2.metric("Best Score",       sig.get("best_score",        "—"))
    c3.metric("Best Epoch",       sig.get("best_epoch",        "—"))
    c4.metric("Final Score",      sig.get("final_score",       "—"))
    c5.metric("Variance",         sig.get("training_variance", "—"))

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── DIAGNOSTICS ──
    st.markdown("<p class='section-label'>Diagnostics</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    is_healthy  = diag.get("status") == "HEALTHY"
    badge_class = "badge-healthy" if is_healthy else "badge-issue"
    icon        = "✓" if is_healthy else "⚠"
    issues      = diag.get("issues", [])
    issues_text = ", ".join(issues) if issues else "None"

    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:8px;'>
      <span class='{badge_class}'>{icon}&nbsp;&nbsp;{diag.get("status", "—")}</span>
      <span style='font-size:12px;color:#94a3b8;'>
        Score: <strong style='color:#e2e8f0;'>{diag.get("score", "—")}</strong>
      </span>
      <span style='font-size:12px;color:#94a3b8;'>
        Issues:
        <span style='font-family:DM Mono,monospace;font-size:11px;color:#475569;'>
          {issues_text}
        </span>
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── TRAINING METRICS CHART ──
    st.markdown("<p class='section-label'>Training Metrics</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    raw_metrics = fetch_metrics(selected_id)
    df = format_metrics(raw_metrics)

    if not df.empty:
        fig = go.Figure()

        if "val_accuracy" in df.columns:
            fig.add_trace(go.Scatter(
                x=df["step"], y=df["val_accuracy"],
                name="val_accuracy", mode="lines",
                line=dict(color="#38bdf8", width=2),
                hovertemplate="Step %{x}<br>val_accuracy: %{y:.4f}<extra></extra>"
            ))

        if "loss" in df.columns:
            fig.add_trace(go.Scatter(
                x=df["step"], y=df["loss"],
                name="loss", mode="lines",
                line=dict(color="#f87171", width=2),
                hovertemplate="Step %{x}<br>loss: %{y:.4f}<extra></extra>"
            ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#111827",
            font=dict(family="DM Mono, monospace", size=10, color="#475569"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)),
            xaxis=dict(
                gridcolor="rgba(99,179,237,0.07)",
                zerolinecolor="rgba(99,179,237,0.1)",
                tickfont=dict(color="#475569")
            ),
            yaxis=dict(
                gridcolor="rgba(99,179,237,0.07)",
                zerolinecolor="rgba(99,179,237,0.1)",
                tickfont=dict(color="#475569")
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown(
            "<p style='color:#475569;font-family:DM Mono,monospace;font-size:12px;'>"
            "No metrics data available.</p>",
            unsafe_allow_html=True
        )

else:
    st.markdown("""
    <div style='display:flex;flex-direction:column;align-items:center;
                justify-content:center;padding:80px 20px;color:#475569;text-align:center;'>
      <div style='font-size:40px;margin-bottom:12px;opacity:0.4;'>◈</div>
      <p style='font-family:DM Mono,monospace;font-size:12px;'>
        Could not load analysis for this experiment.
      </p>
    </div>
    """, unsafe_allow_html=True)


# ── AI COPILOT ────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>AI Copilot</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    f"<span style='font-family:DM Mono,monospace;font-size:11px;"
    f"color:#38bdf8;'>Context: exp #{selected_id}</span>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])

with col_input:
    query = st.text_input(
        "copilot_query",
        placeholder="Ask about this experiment…",
        label_visibility="collapsed",
        key="copilot_input"
    )

with col_btn:
    ask_clicked = st.button("Ask →", key="ask_btn")

# Handle ask
if ask_clicked:
    if query.strip():
        with st.spinner("Thinking…"):
            st.session_state.copilot_answer = ask_copilot(query.strip(), selected_id)
    else:
        st.warning("Please type a question first.")

# Show answer
if st.session_state.copilot_answer:
    st.markdown(
        "<p style='font-family:DM Mono,monospace;font-size:10px;"
        "color:#475569;letter-spacing:0.08em;margin-bottom:8px;'>RESPONSE</p>",
        unsafe_allow_html=True
    )
    with st.container():
        st.markdown(
            f"""
            <div style='background:#111827;border:1px solid rgba(99,179,237,0.15);
                        border-radius:10px;padding:18px 20px;margin-top:4px;'>
            """,
            unsafe_allow_html=True
        )
        st.markdown(st.session_state.copilot_answer)   # ← native markdown rendering
        st.markdown("</div>", unsafe_allow_html=True)