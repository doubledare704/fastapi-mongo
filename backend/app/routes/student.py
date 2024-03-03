from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends

from app.models import Student
from app.repositories import StudentRepository
from app.schemas.student import Response, UpdateStudentModel

router = APIRouter()


@router.get("/", response_description="Students retrieved", response_model=Response)
async def get_students(sr: StudentRepository = Depends(StudentRepository)):
    students = await sr.retrieve_students()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": students,
    }


@router.get("/{student_id}", response_description="Student data retrieved", response_model=Response)
async def get_student_data(student_id: PydanticObjectId, sr: StudentRepository = Depends(StudentRepository)):
    student = await sr.retrieve_student(student_id)
    if student:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Student data retrieved successfully",
            "data": student,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Student doesn't exist",
    }


@router.post(
    "/",
    response_description="Student data added into the database",
    response_model=Response,
)
async def add_student_data(student: Student = Body(...), sr: StudentRepository = Depends(StudentRepository)):
    new_student = await sr.add_student(student)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student created successfully",
        "data": new_student,
    }


@router.delete("/{student_id}", response_description="Student data deleted from the database")
async def delete_student_data(student_id: PydanticObjectId, sr: StudentRepository = Depends(StudentRepository)):
    deleted_student = await sr.delete_student(student_id)
    if deleted_student:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Student with ID: {} removed".format(id),
            "data": deleted_student,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Student with id {0} doesn't exist".format(id),
        "data": False,
    }


@router.patch("/{student_id}", response_model=Response)
async def update_student(
        student_id: PydanticObjectId,
        req: UpdateStudentModel,
        sr: StudentRepository = Depends(StudentRepository)
):
    updated_student = await sr.update_student_data(student_id, req.model_dump(exclude_none=True))
    if updated_student:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Student with ID: {} updated".format(student_id),
            "data": updated_student,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Student with ID: {} not found".format(student_id),
        "data": False,
    }
