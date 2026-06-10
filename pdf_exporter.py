from fpdf import FPDF


SECTIONS = [
    ("Key Discussion Points", "discussion_points"),
    ("Action Items", "action_items"),
    ("Decisions", "decisions"),
    ("Task Assignments", "task_assignments"),
    ("Next Steps", "next_steps"),
]


def _safe(text):
    return (
        str(text or "")
        .replace("•", "-")
        .replace("—", "-")
        .replace("–", "-")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def _add_wrapped_text(pdf, text, size=11, bold=False):
    style = "B" if bold else ""
    pdf.set_font("Helvetica", style=style, size=size)

    clean_text = _safe(text).replace("\n", " ").replace("\r", "")
    pdf.multi_cell(0, 6, clean_text)


def _add_bullet_list(pdf, items):
    pdf.set_font("Helvetica", size=11)

    if not items:
        pdf.multi_cell(0, 6, "None recorded")
        return

    for item in items:
        if not item:
            continue

        text = _safe(item).replace("\r", "")

        pdf.multi_cell(
            0,
            6,
            f"- {text}"
        )

        pdf.ln(1)

def generate_summary_pdf(result, title="Meeting Summary"):
    pdf = FPDF()

    pdf.set_margins(left=10, top=10, right=10)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, _safe(title), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Meeting Overview", new_x="LMARGIN", new_y="NEXT")

    pdf.set_text_color(0, 0, 0)
    overview = result.get("overview", "").strip() or "None recorded"
    _add_wrapped_text(pdf, overview)
    pdf.ln(4)

    for heading, key in SECTIONS:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")

        pdf.set_text_color(0, 0, 0)
        _add_bullet_list(pdf, result.get(key, []))
        pdf.ln(4)

    return pdf.output(dest='S')