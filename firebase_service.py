import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"E:\Uni_Courses\4.2\CSE_4206\student-llm-backend\student-resource-ed013-firebase-adminsdk-fbsvc-7e7a6ec86a.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



def get_courses():
    courses_ref = db.collection("courses").stream()
    return [doc.to_dict() for doc in courses_ref]

def get_notices():
    notices_ref=db.collection('notices').stream()
    return [doc.to_dict() for doc in notices_ref]


def get_results_by_student(student_id: str):
    results_ref = (
        db.collection("results")
        .where("student_id", "==", student_id)
        .stream()
    )
    return [doc.to_dict() for doc in results_ref]