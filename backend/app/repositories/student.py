__all__ = ('StudentRepository')

from typing import List, Union

from beanie import PydanticObjectId

from app.models import Student


class StudentRepository:

    def __init__(self):
        self.collection = Student

    async def retrieve_students(self) -> List[Student]:
        students = await self.collection.all().to_list()
        return students

    async def add_student(self, new_student: Student) -> Student:
        student = await new_student.create()
        return student

    async def retrieve_student(self, student_id: PydanticObjectId) -> Student:
        student = await self.collection.get(student_id)
        if student:
            return student

    async def delete_student(self, student_id: PydanticObjectId) -> bool:
        student = await self.collection.get(student_id)
        if student:
            await student.delete()
            return True

    async def update_student_data(self, student_id: PydanticObjectId, data: dict) -> Union[bool, Student]:
        update_query = {"$set": {**data}}
        student = await self.collection.get(student_id)
        if student:
            await student.update(update_query)
            return student
        return False
