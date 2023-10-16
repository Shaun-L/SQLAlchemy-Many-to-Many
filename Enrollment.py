from orm_base import Base
from sqlalchemy import UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Column, Identity
from datetime import datetime

class Enrollment(Base):
    __tablename__ = "enrollment"
    section: Mapped["Section"] = relationship(back_populates="sections")
    student: Mapped["Student"] = relationship(back_populates="students")
    studentId: Mapped[int] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation", ForeignKey("sections.department_abbreviation"), primary_key=True)
    courseNumber: Mapped[int] = mapped_column("course_number", ForeignKey("sections.course_number"), primary_key=True)
    sectionNumber: Mapped[int] = mapped_column("section_number", Integer, Identity(start=1, cycle=True),
                                               ForeignKey("sections.section_number"), primary_key=True)
    sectionYear: Mapped[int] = mapped_column("section_year", Integer, ForeignKey("sections.section_year"), primary_key=True)
    semester: Mapped[str] = mapped_column("semester", String(10), ForeignKey("sections.semester"), primary_key=True)

    __table_args__ = (UniqueConstraint("department_abbreviation", "course_number", "section_year", "semester", "student_id",
                                       name="enrollments_uk_01"))

    def __init__(self, section, student):
        self.section = section
        self.student = student
        self.studentId = student.studentID
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.sectionYear = section.sectionYear
        self.semester = section.semester

    def __str__(self):
        return f"Student enrollment - student: {self.student} course: {self.courseNumber} section: {self.sectionNumber}"





