# app.py
import streamlit as st
from input_handler import parse_and_validate_inputs
from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from algorithms.cscan import cscan
from algorithms.look import look
from algorithms.clook import clook
from utils.animation import AnimationController
from utils.graph import plot_path, plot_comparison

import pandas as pd
import os

# -------------------------
# Page config & theme CSS
# -------------------------
st.set_page_config(page_title="Disk Scheduling Visualizer", layout="wide")

# Custom blue/teal theme (light-ish card background)
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(120deg, #e6fbff 0%, #e7f8ff 50%, #f2fcff 100%);
    }
    .stApp .css-1d391kg {
        background: transparent;
    }
    h1 { color: #064e54; text-align:center; }
    .card { background: white; border-radius:10px; padding:18px; box-shadow: 0 2px 8px rgba(6,78,84,0.08); }
    .alg-title { color:#007C91; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Disk Scheduling Visualizer</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# Left column: Inputs
# -------------------------
left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Input Parameters", unsafe_allow_html=True)

    # Input handler returns (requests, head, disk_size, error_message_or_none)
    requests, head, disk_size, error = parse_and_validate_inputs()

    st.markdown("---")
    st.markdown("**Choose algorithm**")
    algorithm = st.selectbox("", ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"])

    st.markdown("---")
    # Controls
    run_alg = st.button("▶ Run Selected Algorithm")
    compare_btn = st.button("📊 Compare All Algorithms")
    st.markdown("</div>", unsafe_allow_html=True)

# If parse returned an error, show a friendly message and stop further actions
if error:
    st.error(error)
    st.info("Please fix inputs above and re-run.")
    st.stop()

# -------------------------
# Right: Results / Animation / Graph
# -------------------------
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Results & Visualization", unsafe_allow_html=True)

    # Prepare algorithm functions mapping
    algo_map = {
        "FCFS": fcfs,
        "SSTF": sstf,
        "SCAN": lambda reqs, head_pos: scan(reqs, head_pos, disk_size),
        "C-SCAN": lambda reqs, head_pos: cscan(reqs, head_pos, disk_size),
        "LOOK": look,
        "C-LOOK": clook,
    }

    # Animation controller stores index in session_state
    anim = AnimationController()

    # Run single algorithm
    if run_alg:
        func = algo_map[algorithm]
        # compute sequence and seek; algorithm modules return (sequence, seek)
        sequence, seek = func(requests, head)
        st.success(f"Total head movement (seek distance): **{seek}**")
        st.markdown("#### Head Movement Path")
        # show full path once
        plot_path(sequence, use_streamlit=True)

        st.markdown("#### Step-by-step Animation (use Previous / Next)")
        # Initialize animation with the computed sequence (ONLY on Run click)
        anim.set_sequence(sequence, disk_size=disk_size)

    # Always show animation controls (they operate over the session sequence)
    st.markdown("#### Animation Controls")
    col_prev, col_next, col_reset = st.columns([1, 1, 1])
    if col_prev.button("◀ Previous"):
        anim.prev()
    if col_next.button("Next ▶"):
        anim.next()
    if col_reset.button("Reset"):
        anim.reset()

    # Show always the current animation frame (this uses session_state so it persists across clicks)
    anim.show_current()

    # Compare all algorithms
    if compare_btn:
        results = {}
        sequences = {}
        for name, f in algo_map.items():
            seq, s = f(requests, head)
            results[name] = s
            sequences[name] = seq

        st.markdown("#### Comparison Table")
        df = pd.DataFrame({"Algorithm": list(results.keys()), "Seek Time": list(results.values())})
        st.table(df.sort_values("Seek Time"))

        # highlight best
        best = df.loc[df["Seek Time"].idxmin()]
        st.success(f"🏆 Best Algorithm: **{best['Algorithm']}** (Seek Time: {best['Seek Time']})")

        st.markdown("#### Comparison Chart")
        plot_comparison(results, use_streamlit=True)

    # Show example uploaded screenshot (if available)
    uploaded_img_path = "/mnt/data/324bfd56-dbdb-4e41-9107-667c5a1e289d.png"
    if os.path.exists(uploaded_img_path):
        st.markdown("---")
        st.markdown("#### Example error screenshot (your uploaded image)")
        st.image(uploaded_img_path, caption="Your screenshot", use_column_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
