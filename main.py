from fastapi import FastAPI
from pydantic import BaseModel

from firebase_service import get_courses, get_results_by_student
from rag import build_context, route_question
from llm import call_llm

app = FastAPI()


class AskRequest(BaseModel):
    student_id: str
    question: str


@app.post("/ask")
def ask_llm(req: AskRequest):
    courses = get_courses()
    results = get_results_by_student(req.student_id)

    mode = route_question(req.question)
    context = build_context(courses, results, mode)

    prompt = f"""
You are an academic advisor for a university student.

Use the student data below to answer the question.
Do NOT give generic advice.
Base suggestions on grades, marks, and courses.

STUDENT DATA:
{context}

QUESTION:
{req.question}
"""

    answer = call_llm(prompt)

    return {
        "answer": answer,
        "mode_used": mode,
        "courses_used": len(courses),
        "results_used": len(results)
    }
