# input_handler.py
import streamlit as st

def parse_and_validate_inputs():
    """
    Returns: (requests_list, head, disk_size, error_message_or_None)
    This function uses Streamlit inputs (so keep it idempotent on each run).
    """
    # Requests input
    requests_input = st.text_input("Enter disk requests (comma-separated)", value="98, 183, 37, 122, 14, 124, 65, 67")

    # Disk size and head inputs (head max is disk_size - 1 but we avoid raising error)
    disk_size = st.number_input("Enter disk size (max track number will be disk_size - 1)", min_value=1, value=200)
    head = st.number_input("Initial head position", min_value=0, value=53)

    # Validate parsing
    requests = []
    parse_error = None
    if requests_input.strip() == "":
        parse_error = "Request list is empty. Please enter one or more comma-separated integers."
    else:
        parts = requests_input.split(",")
        for p in parts:
            p = p.strip()
            if p == "":
                continue
            try:
                val = int(p)
                requests.append(val)
            except ValueError:
                parse_error = f"Invalid request value: '{p}'. Use only integers separated by commas."
                break

    # Validate against disk size
    if not parse_error:
        if any(r < 0 for r in requests):
            parse_error = "Requests must be non-negative integers."
        elif any(r >= disk_size for r in requests):
            parse_error = "One or more requests exceed or equal the disk size. Please lower requests or increase disk size."
        elif head < 0 or head >= disk_size:
            parse_error = "Initial head position must be between 0 and disk_size - 1."

    # If parse_error exists, return it in error field
    return requests, head, disk_size, parse_error