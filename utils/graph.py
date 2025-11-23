# utils/graph.py
import streamlit as st
import matplotlib.pyplot as plt

def plot_path(sequence, use_streamlit=True):
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(sequence, marker='o', linewidth=2)
    ax.set_xlabel("Step")
    ax.set_ylabel("Track Number")
    ax.set_title("Disk Head Movement Path")
    ax.grid(True)
    if use_streamlit:
        st.pyplot(fig)
    else:
        return fig

def plot_comparison(results_dict, use_streamlit=True):
    fig, ax = plt.subplots(figsize=(6,3))
    names = list(results_dict.keys())
    values = list(results_dict.values())
    ax.bar(names, values, color="#007C91")
    ax.set_ylabel("Total Head Movement")
    ax.set_title("Algorithm Comparison")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    if use_streamlit:
        st.pyplot(fig)
    else:
        return fig