from typing import Optional, Any

from pydantic import BaseModel, EmailStr, Field


class UpdateStudentModel(BaseModel):
    fullname: Optional[str] = Field(None, alias='fullname')
    email: Optional[EmailStr] = Field(None, alias='email')
    course_of_study: Optional[str] = Field(None, alias='course_of_study')
    year: Optional[int] = Field(None, alias='year')
    gpa: Optional[float] = Field(None, alias='gpa')

    class Collection:
        name = "student"

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez",
                "email": "abdul@school.com",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "5.0",
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
