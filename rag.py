def route_question(question: str):
    q = question.lower()

    if "improve" in q or "grade" in q or "result" in q:
        return "results"

    if "course" in q or "resource" in q:
        return "courses"

    return "all"


def build_context(courses, results, mode="all"):
    text = ""

    if mode in ["all", "courses"]:
        text += "Available Courses This Semester:\n"
        for c in courses:
            text += (
                f"- {c.get('course_code', '')}: "
                f"{c.get('course_name', '')} | "
                f"Semester: {c.get('semester', '')} | "
                f"Credits: {c.get('credits', 'N/A')} | "
                f"Instructor: {c.get('instructor', 'N/A')}\n"
            )

    if mode in ["all", "results"]:
        text += "\nStudent Previous Results:\n"
        for r in results:
            text += (
                f"- {r.get('course_code')} "
                f"{r.get('course_name')} | "
                f"Grade: {r.get('grade')} | "
                f"Marks: {r.get('marks')} | "
                f"Semester: {r.get('semester')}\n"
            )

    return text
