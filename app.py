import streamlit as st

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


# -----------------------------
# PAGE 1: UPLOAD PAGE
# -----------------------------
def upload_page():
    st.title("📤 Upload Meeting Recording")

    uploaded_file = st.file_uploader(
        "Choose your meeting file",
        type=["mp3", "wav", "mp4"]
    )

    if uploaded_file:
        st.success("File uploaded successfully!")

    if st.button("🚀 Generate Summary"):
        if uploaded_file is None:
            st.warning("Please upload a file first!")
            return

        # 🔄 Simulate processing
        with st.spinner("Processing meeting..."):
            
            # -----------------------------
            # PLACEHOLDER DATA (YOUR JSON)
            # -----------------------------
            result = {
                "overview": "This meeting focused on project progress, deadlines, and team responsibilities.",
                "discussion_points": [
                    "Project timeline review",
                    "Budget constraints",
                    "Client feedback"
                ],
                "action_items": [
                    "Prepare project report",
                    "Update client presentation"
                ],
                "decisions": [
                    "Deadline extended by 3 days",
                    "Adopt new design approach"
                ],
                "task_assignments": [
                    "Rahul → Report preparation",
                    "Anita → Client communication"
                ],
                "next_steps": [
                    "Conduct follow-up meeting",
                    "Finalize deliverables"
                ]
            }

            # Save to session
            st.session_state.result = result

            # Move to next page
            st.session_state.page = "results"
            st.rerun()


# -----------------------------
# PAGE 2: RESULTS PAGE
# -----------------------------
def results_page():
    st.title("📊 Meeting Summary")

    result = st.session_state.result

    if result is None:
        st.error("No data found. Go back and upload a file.")
        return

    # 🔙 Back Button
    if st.button("⬅️ Back"):
        st.session_state.page = "upload"
        st.rerun()

    st.divider()

    # -----------------------------
    # LAYOUT
    # -----------------------------
    col1, col2 = st.columns(2)

    # LEFT SIDE
    with col1:
        st.subheader("📄 Meeting Overview")
        st.write(result["overview"])

        st.subheader("🔑 Key Discussion Points")
        for point in result["discussion_points"]:
            st.write(f"• {point}")

        st.subheader("✅ Action Items")
        for item in result["action_items"]:
            st.write(f"• {item}")

    # RIGHT SIDE
    with col2:
        st.subheader("📌 Decisions")
        for d in result["decisions"]:
            st.write(f"• {d}")

        st.subheader("👥 Task Assignments")
        for t in result["task_assignments"]:
            st.write(f"• {t}")

        st.subheader("➡️ Next Steps")
        for step in result["next_steps"]:
            st.write(f"• {step}")

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    st.divider()

    st.download_button(
        "⬇️ Download Summary",
        data=str(result),
        file_name="meeting_summary.txt"
    )


# -----------------------------
# ROUTING LOGIC
# -----------------------------
if st.session_state.page == "upload":
    upload_page()
else:
    results_page()