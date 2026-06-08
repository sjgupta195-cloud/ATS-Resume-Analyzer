print("NEW REPORT_GENERATOR LOADED")

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    ats_score,
    matched_skills,
    missing_skills,
    ai_review,
    roadmap,
    suggestions

):

    pdf = SimpleDocTemplate(
        "ATS_Report.pdf"
    )

    styles = getSampleStyleSheet()
    ai_review = ai_review.replace("\n", "<br/>")
    roadmap = roadmap.replace("\n", "<br/>")
    suggestions = suggestions.replace("\n", "<br/>")

    content = []

    content.append(
        Paragraph(
            "ATS Resume Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>ATS Score: {ats_score:.2f}%</b>",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Matched Skills",
            styles["Heading1"]
        )
    )

    for skill in matched_skills:

        content.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # Missing Skills

    content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading1"]
        )
    )

    for skill in missing_skills:

        content.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "AI Review",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            ai_review,
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Learning Roadmap",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            roadmap,
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Resume Rewrite Suggestions",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            suggestions,
            styles["BodyText"]
        )
    )    

    pdf.build(content)

    return "ATS_Report.pdf"