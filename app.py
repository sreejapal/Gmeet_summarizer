import streamlit as st
import json
import os
from processor import process_video
from database import init_db, save_meeting, delete_meeting, get_all_meetings, search_meetings
from email_sender import send_summary_email

os.makedirs("uploads", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)
os.makedirs("summaries", exist_ok=True)

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
init_db()

st.set_page_config(
    page_title="MeetGenie",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Page background ── */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* ── Hide default Streamlit header/footer ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top nav bar ── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 24px 0;
    border-bottom: 1px solid #1e2130;
    margin-bottom: 36px;
}
.nav-logo {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: -0.4px;
    color: #ffffff;
}
.nav-logo span { color: #4f7cff; }
.nav-tag {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    color: #5a6070;
    background: #1a1d2b;
    border: 1px solid #252836;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Section card ── */
.section-card {
    background: #141720;
    border: 1px solid #1e2130;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
}
.section-card h4 {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    color: #4f7cff;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0 0 14px 0;
}
.section-card p, .section-card li {
    color: #c8ccd8;
    font-size: 14px;
    line-height: 1.7;
    margin: 0;
}
.section-card ul {
    padding-left: 18px;
    margin: 0;
}
.section-card li { margin-bottom: 6px; }

/* ── Overview card special ── */
.overview-card {
    background: linear-gradient(135deg, #141c38 0%, #141720 100%);
    border: 1px solid #2a3260;
    border-radius: 12px;
    padding: 28px;
    margin-bottom: 24px;
}
.overview-card h4 {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    color: #7c9fff;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0 0 12px 0;
}
.overview-card p {
    color: #dde2f0;
    font-size: 15px;
    line-height: 1.75;
    margin: 0;
}

/* ── Meeting history card ── */
.meeting-card {
    background: #141720;
    border: 1px solid #1e2130;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.meeting-card:hover { border-color: #2e3a5c; }
.meeting-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #e8eaf0;
    margin-bottom: 4px;
}
.meeting-card-meta {
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    color: #4a5068;
    margin-bottom: 10px;
}
.meeting-card-overview {
    font-size: 13px;
    color: #7a8098;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ── Stat badge ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}
.stat-badge {
    background: #141720;
    border: 1px solid #1e2130;
    border-radius: 8px;
    padding: 12px 18px;
    flex: 1;
    min-width: 120px;
}
.stat-badge .stat-num {
    font-size: 22px;
    font-weight: 600;
    color: #4f7cff;
    display: block;
}
.stat-badge .stat-label {
    font-size: 11px;
    color: #5a6070;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-family: 'DM Mono', monospace;
}

/* ── Page title ── */
.page-title {
    font-size: 28px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}
.page-subtitle {
    font-size: 14px;
    color: #5a6070;
    margin-bottom: 32px;
}

/* ── Upload zone ── */
.upload-hint {
    font-size: 12px;
    color: #3a4060;
    font-family: 'DM Mono', monospace;
    margin-top: 6px;
}

/* ── Divider ── */
hr { border-color: #1e2130 !important; }

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stFileUploader > div {
    background-color: #141720 !important;
    border-color: #1e2130 !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
}
.stTextInput > label, .stFileUploader > label {
    color: #7a8098 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stButton > button {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

/* ── Alert overrides ── */
.stAlert {
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* ── Expander override ── */
.streamlit-expanderHeader {
    background: #141720 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for key, default in [("page", "upload"), ("result", None), ("error", None), ("filename", None)]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def nav_bar(current_page):
    page_labels = {"upload": "New Meeting", "results": "Summary", "history": "History"}
    label = page_labels.get(current_page, "")
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-logo">Meet<span>Genie</span></div>
        <div class="nav-tag">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def section_card(title, items, icon=""):
    if not items:
        content = '<p style="color:#3a4060;font-style:italic;font-size:13px;">None recorded</p>'
    else:
        lis = "".join(f"<li>{item}</li>" for item in items)
        content = f"<ul>{lis}</ul>"
    st.markdown(f"""
    <div class="section-card">
        <h4>{icon} {title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)


def stat_badges(result):
    counts = [
        (len(result.get("discussion_points", [])), "Discussion Points"),
        (len(result.get("action_items", [])), "Action Items"),
        (len(result.get("decisions", [])), "Decisions"),
        (len(result.get("task_assignments", [])), "Task Assignments"),
        (len(result.get("next_steps", [])), "Next Steps"),
    ]
    badges = "".join(
        f'<div class="stat-badge"><span class="stat-num">{n}</span><span class="stat-label">{label}</span></div>'
        for n, label in counts
    )
    st.markdown(f'<div class="stat-row">{badges}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE 1 — UPLOAD
# ─────────────────────────────────────────────
def upload_page():
    nav_bar("upload")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="page-title">New Meeting Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Upload a recording or transcript to generate an AI-powered summary.</div>', unsafe_allow_html=True)

        meeting_name = st.text_input("Meeting name", placeholder="e.g. Q2 Planning - June 2026")

        uploaded_file = st.file_uploader(
            "Recording or transcript",
            type=["mp3", "wav", "mp4", "txt"],
            help="Supported formats: MP3, WAV, MP4 (audio/video), TXT (transcript)"
        )
        st.markdown('<div class="upload-hint">MP3 · WAV · MP4 · TXT</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.success(f"✓ Ready to process **{uploaded_file.name}**")
            st.session_state.filename = meeting_name.strip()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Generate Summary →", type="primary", use_container_width=True):
            if not uploaded_file:
                st.warning("Please upload a file before generating a summary.")
                return
            if not meeting_name.strip():
                st.warning("Please enter a meeting name.")
                return

            try:
                with st.spinner("Transcribing and summarising — this may take a minute…"):
                    ext = uploaded_file.name.rsplit(".", 1)[-1]
                    temp_path = f"temp.{ext}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())

                    result = process_video(temp_path)
                    st.session_state.result = result
                    st.session_state.page = "results"
                    os.remove(temp_path)

                st.rerun()

            except Exception as e:
                st.session_state.error = str(e)

    with col_side:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card">
            <h4>How it works</h4>
            <ul>
                <li>Upload your meeting recording or paste a transcript (.txt)</li>
                <li>Whisper transcribes audio files automatically</li>
                <li>Gemini AI extracts key insights, action items and decisions</li>
                <li>Download the summary as JSON or email it directly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📋  View Meeting History", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()

    if st.session_state.error:
        st.error(f"⚠ {st.session_state.error}")
        st.session_state.error = None


# ─────────────────────────────────────────────
#  PAGE 2 — RESULTS
# ─────────────────────────────────────────────
def results_page():
    nav_bar("results")

    result = st.session_state.result
    if not result:
        st.error("No summary data found. Please go back and process a meeting.")
        if st.button("← Back"):
            st.session_state.page = "upload"
            st.rerun()
        return

    # Header row
    title_col, btn_col = st.columns([4, 1])
    with title_col:
        name = st.session_state.filename or "Meeting Summary"
        st.markdown(f'<div class="page-title">{name}</div>', unsafe_allow_html=True)
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← New Meeting", use_container_width=True):
            st.session_state.page = "upload"
            st.session_state.result = None
            st.rerun()

    # Stats row
    stat_badges(result)

    # Overview — full width
    overview = result.get("overview", "").strip()
    st.markdown(f"""
    <div class="overview-card">
        <h4>📄 &nbsp;Meeting Overview</h4>
        <p>{overview if overview else '<span style="color:#3a4060;font-style:italic">No overview generated.</span>'}</p>
    </div>
    """, unsafe_allow_html=True)

    # Detail grid — 3 columns
    c1, c2, c3 = st.columns(3)
    with c1:
        section_card("Key Discussion Points", result.get("discussion_points", []), "🔑")
        section_card("Decisions", result.get("decisions", []), "📌")
    with c2:
        section_card("Action Items", result.get("action_items", []), "✅")
        section_card("Task Assignments", result.get("task_assignments", []), "👥")
    with c3:
        section_card("Next Steps", result.get("next_steps", []), "➡️")

        # Save + Download stacked in right column
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save to History", use_container_width=True):
            if overview:
                save_meeting(st.session_state.filename, result)
                st.success("Meeting saved successfully.")
            else:
                st.error("Cannot save a summary with no overview.")

        st.download_button(
            "Download JSON",
            data=json.dumps(result, indent=4),
            file_name="meeting_summary.json",
            mime="application/json",
            use_container_width=True
        )

    # Email section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    email_col, btn_col = st.columns([3, 1])
    with email_col:
        email = st.text_input("Send summary via email", placeholder="recipient@example.com", label_visibility="visible")
    with btn_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Send Email →", use_container_width=True):
            if not email:
                st.warning("Please enter a recipient email address.")
            else:
                try:
                    send_summary_email(email, result)
                    st.success(f"Summary sent to **{email}**.")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")


# ─────────────────────────────────────────────
#  PAGE 3 — HISTORY
# ─────────────────────────────────────────────
def history_page():
    nav_bar("history")

    title_col, back_col = st.columns([4, 1])
    with title_col:
        st.markdown('<div class="page-title">Meeting History</div>', unsafe_allow_html=True)
    with back_col:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()

    search_query = st.text_input("", placeholder="🔍  Search meetings by name, keyword, or content…", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    meetings = search_meetings(search_query) if search_query.strip() else get_all_meetings()

    if not meetings:
        if search_query:
            st.info(f'No meetings found matching "**{search_query}**".')
        else:
            st.info("No meetings saved yet. Process a meeting and click **Save to History**.")
        return

    count_label = f"{len(meetings)} meeting{'s' if len(meetings) != 1 else ''} found" if search_query else f"{len(meetings)} saved meeting{'s' if len(meetings) != 1 else ''}"
    st.markdown(f'<div style="font-size:12px;color:#4a5068;font-family:DM Mono,monospace;margin-bottom:16px;">{count_label}</div>', unsafe_allow_html=True)

    for meeting in meetings:
        meeting_id, filename, created_at, overview, summary_json = meeting

        st.markdown(f"""
        <div class="meeting-card">
            <div class="meeting-card-title">{filename or "Untitled Meeting"}</div>
            <div class="meeting-card-meta">{created_at}</div>
            <div class="meeting-card-overview">{overview or "No overview available."}</div>
        </div>
        """, unsafe_allow_html=True)

        detail_col, del_col = st.columns([5, 1])
        with detail_col:
            with st.expander("View full summary"):
                parsed = json.loads(summary_json)
                section_card("Overview", [parsed.get("overview", "")], "📄")
                ec1, ec2 = st.columns(2)
                with ec1:
                    section_card("Discussion Points", parsed.get("discussion_points", []), "🔑")
                    section_card("Action Items", parsed.get("action_items", []), "✅")
                with ec2:
                    section_card("Decisions", parsed.get("decisions", []), "📌")
                    section_card("Task Assignments", parsed.get("task_assignments", []), "👥")
                section_card("Next Steps", parsed.get("next_steps", []), "➡️")

                st.download_button(
                    "⬇  Download JSON",
                    data=json.dumps(parsed, indent=4),
                    file_name=f"{filename or 'meeting'}_summary.json",
                    mime="application/json",
                    key=f"dl_{meeting_id}"
                )
        with del_col:
            if st.button("🗑", key=f"del_{meeting_id}", help="Delete this meeting"):
                delete_meeting(meeting_id)
                st.rerun()

        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────
pages = {"upload": upload_page, "results": results_page, "history": history_page}
pages.get(st.session_state.page, upload_page)()
