import streamlit as st
import json
import os
from processor import process_video
from database import save_meeting
from database import init_db

init_db()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Meeting Summarizer", layout="wide")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "result" not in st.session_state:
    st.session_state.result = None

if "error" not in st.session_state:
    st.session_state.error = None

if "filename" not in st.session_state:
    st.session_state.filename = None


# -----------------------------
# PAGE 1: UPLOAD PAGE
# -----------------------------
def upload_page():
    st.title("Upload Meeting Recording")

    uploaded_file = st.file_uploader(
        "Choose your meeting file",
        type=["mp3", "wav", "mp4",  "txt"]
    )

    if uploaded_file:
        st.success("File uploaded successfully!")
        st.session_state.filename = uploaded_file.name

    if st.button("Generate Summary"):
        if uploaded_file is None:
            st.warning("Please upload a file first!")
            return

        try:
            with st.spinner("Processing meeting..."):

                # Save temp file
                file_extension = uploaded_file.name.split(".")[-1]
                temp_file_path = f"temp.{file_extension}"

                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Call backend
                result = process_video(temp_file_path)

                # Save result
                st.session_state.result = result
                st.session_state.page = "results"

                # Cleanup temp file
                os.remove(temp_file_path)

                st.rerun()

        except Exception as e:
            st.session_state.error = str(e)


# -----------------------------
# PAGE 2: RESULTS PAGE
# -----------------------------
def results_page():
    st.title("Meeting Summary")

    result = st.session_state.result

    if result is None:
        st.error("No data found. Go back and upload a file.")
        return

    # Back button
    if st.button("Back"):
        st.session_state.page = "upload"
        st.session_state.result = None
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    # LEFT COLUMN
    with col1:
        st.subheader("📄 Meeting Overview")
        st.write(result.get("overview", "N/A"))

        st.subheader("🔑 Key Discussion Points")
        for point in result.get("discussion_points", []):
            st.write(f"• {point}")

        st.subheader("✅ Action Items")
        for item in result.get("action_items", []):
            st.write(f"• {item}")

    # RIGHT COLUMN
    with col2:
        st.subheader("📌 Decisions")
        for d in result.get("decisions", []):
            st.write(f"• {d}")

        st.subheader("👥 Task Assignments")
        for t in result.get("task_assignments", []):
            st.write(f"• {t}")

        st.subheader("➡️ Next Steps")
        for step in result.get("next_steps", []):
            st.write(f"• {step}")

    # Download as JSON
    st.divider()

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.download_button(
            "Download Summary (JSON)",
            data=json.dumps(result, indent=4),
            file_name="meeting_summary.json",
            mime="application/json"
        )

    with col2:
        if st.button("Save Meeting"):
            if result.get("overview"):

                save_meeting(
                    st.session_state.filename,
                    result
                )

                st.success("Meeting saved successfully!")

            else:
                st.error("Cannot save empty summary.")

# -----------------------------
# ROUTING
# -----------------------------
if st.session_state.page == "upload":
    upload_page()

elif st.session_state.page == "results":
    results_page()


# -----------------------------
# ERROR DISPLAY (SAFE)
# -----------------------------
if st.session_state.error:
    st.error(st.session_state.error)
    st.session_state.error = None  # prevent infinite loop