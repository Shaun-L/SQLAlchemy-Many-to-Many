from orm_base import Base
from sqlalchemy import UniqueConstraint, ForeignKey, Date, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Column, Identity
from datetime import datetime

class Enrollment(Base):
    """The association class between Section and Student."""
    __tablename__ = "enrollments"
    #the enrollments table has no attributes of its own the, following are foreign keys.
    section: Mapped["Section"] = relationship(back_populates="students")
    student: Mapped["Student"] = relationship(back_populates="sections")
    studentId: Mapped[int] = mapped_column('student_id', nullable=False, primary_key=True)
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation", nullable=False, primary_key=True)
    courseNumber: Mapped[int] = mapped_column("course_number", nullable=False, primary_key=True)
    sectionNumber: Mapped[int] = mapped_column("section_number", nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column("section_year", nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column("semester", nullable=False, primary_key=True)

    #to ensure that no student enrolls into the same course more than once in a semester.
    __table_args__ = (UniqueConstraint("department_abbreviation", "course_number", "section_year", "semester", "student_id",
                                       name="enrollments_uk_01"),
                      ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionNumber, sectionYear, semester],
                                           ["sections.department_abbreviation", "sections.course_number", "sections.section_number",
                                            "sections.section_year", "sections.semester"]),
                      ForeignKeyConstraint([studentId], ["students.student_id"]))
    #testin

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





