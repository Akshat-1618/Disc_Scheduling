# utils/animation.py
import streamlit as st
import matplotlib.pyplot as plt

class AnimationController:
    """
    Controls step-by-step animation state using st.session_state.
    Stores:
      - st.session_state['ds_sequence'] -> list of head positions (including initial head)
      - st.session_state['ds_idx'] -> current index into sequence
      - st.session_state['ds_disk_size'] -> disk_size for progress normalization (optional)
    """

    SEQ_KEY = "ds_sequence"
    IDX_KEY = "ds_idx"
    DISK_KEY = "ds_disk_size"

    def __init__(self):
        # Initialize keys if missing
        if self.SEQ_KEY not in st.session_state:
            st.session_state[self.SEQ_KEY] = []
        if self.IDX_KEY not in st.session_state:
            st.session_state[self.IDX_KEY] = 0
        if self.DISK_KEY not in st.session_state:
            st.session_state[self.DISK_KEY] = 0

    def set_sequence(self, seq, disk_size=200):
        """Set a new sequence and reset index to 0."""
        st.session_state[self.SEQ_KEY] = list(seq)
        st.session_state[self.IDX_KEY] = 0
        st.session_state[self.DISK_KEY] = int(disk_size)

    def next(self):
        """Advance one step (no-op at end)."""
        if st.session_state[self.SEQ_KEY]:
            st.session_state[self.IDX_KEY] = min(
                st.session_state[self.IDX_KEY] + 1,
                len(st.session_state[self.SEQ_KEY]) - 1,
            )

    def prev(self):
        """Go one step back (no-op at start)."""
        if st.session_state[self.SEQ_KEY]:
            st.session_state[self.IDX_KEY] = max(st.session_state[self.IDX_KEY] - 1, 0)

    def reset(self):
        """Reset index to the beginning."""
        st.session_state[self.IDX_KEY] = 0

    def clear(self):
        """Clear the animation data."""
        st.session_state[self.SEQ_KEY] = []
        st.session_state[self.IDX_KEY] = 0
        st.session_state[self.DISK_KEY] = 0

    def get_state(self):
        """Return (sequence, idx, disk_size)."""
        return (
            st.session_state.get(self.SEQ_KEY, []),
            st.session_state.get(self.IDX_KEY, 0),
            st.session_state.get(self.DISK_KEY, 0),
        )

    def show_current(self, container=None, show_full_path=True):
        """
        Render the current animation frame.
        - container: optional st.container() or st.empty() to draw into (created by caller)
        - show_full_path: if True, also show full path (lighter color) and highlight current position
        """
        seq, idx, disk_size = self.get_state()
        if not seq:
            # No data yet
            if container:
                with container:
                    st.info("No animation data yet. Run an algorithm first.")
            else:
                st.info("No animation data yet. Run an algorithm first.")
            return

        # Build the plot
        fig, ax = plt.subplots(figsize=(8, 3))

        # plot the full sequence lightly, if requested
        x_full = list(range(len(seq)))
        y_full = seq

        if show_full_path:
            ax.plot(x_full, y_full, linewidth=1, alpha=0.3, marker='o', linestyle='--', label='Full path')

        # plot up to current index (solid)
        x_partial = list(range(idx + 1))
        y_partial = seq[: idx + 1]
        ax.plot(x_partial, y_partial, linewidth=2, marker='o', label='So far')

        # highlight current head position
        ax.scatter([idx], [seq[idx]], s=120, c='tab:blue', edgecolors='black', zorder=5, label='Current head')

        ax.set_xlabel("Step")
        ax.set_ylabel("Cylinder / Track")
        ax.set_title(f"Head Movement — Step {idx} / {len(seq)-1}  (Head at {seq[idx]})")
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='upper right', fontsize='small')

        # optional progress-like bar using disk_size (normalized)
        if disk_size and disk_size > 0:
            # show a small progress indicator below the chart (as text)
            prog_percent = (seq[idx] / disk_size) if disk_size else 0
            ax.text(0.01, -0.15, f"Track: {seq[idx]}  •  Normalized position: {prog_percent:.2f}", transform=ax.transAxes)

        # Render into container or directly
        if container:
            with container:
                st.pyplot(fig)
        else:
            st.pyplot(fig)
