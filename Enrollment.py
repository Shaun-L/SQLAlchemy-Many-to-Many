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
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation", nullable=False, primary_key=True)
    courseNumber: Mapped[int] = mapped_column("course_number", nullable=False, primary_key=True)
    sectionNumber: Mapped[int] = mapped_column("section_number", Integer, Identity(start=1, cycle=True),
                                               nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column("section_year", Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column("semester", String(10), nullable=False, primary_key=True)

