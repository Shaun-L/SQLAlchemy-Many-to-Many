from Course import Course
from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from typing import List
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy import String, Integer, Column, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from sqlalchemy.types import Time
from Enrollment import Enrollment
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES

table_name: str = "sections"  # The physical name of this table
# Find out whether the user is introspecting or starting over
introspection_type = IntrospectionFactory().introspection_type
#if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
class Section(Base):
    """(ADD DESCRIPTION)"""
    __tablename__ = table_name

    # foreign key constraint from courses in __table_args__
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation", nullable=False, primary_key=True)
    # foreign key constraint from courses in __table_args__
    courseNumber: Mapped[int] = mapped_column("course_number", nullable=False, primary_key=True)
    course: Mapped["Course"] = relationship(back_populates="sections")
    sectionNumber: Mapped[int] = mapped_column("section_number", Integer, Identity(start=1, cycle=True),
                                               nullable=False, primary_key=True)

    # Make sure database only accepts these values: ('Fall', 'Winter', 'Spring', 'Summer I', or 'Summer II')
    semester: Mapped[str] = mapped_column("semester", String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column("section_year", Integer, nullable=False, primary_key=True)

    # Make sure the database will only accept a value building from the list: (VEC, ECS, EN2, EN3, ET, and SSPA)
    building: Mapped[str] = mapped_column("building", String(6), nullable=False)
    room: Mapped[int] = mapped_column("room", Integer, nullable=False)

    # Make sure the database only takes these values: (MW, TuTh, MWF, F, S)
    schedule: Mapped[str] = mapped_column("schedule", String(6), nullable=False)
    startTime: Mapped[Time] = mapped_column("start_time", Time, nullable=False)
    instructor: Mapped[str] = mapped_column("instructor", String(80), nullable=False)

    students: Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                        cascade="all, save-update, delete-orphan")

    __table_args__ = (UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room",
                                       name="sections_uk_01"),
                      UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor",
                                       name="sections_uk_02"),
                      ForeignKeyConstraint([departmentAbbreviation, courseNumber], [Course.departmentAbbreviation,
                                                                                    Course.courseNumber]))

    def __init__(self, course: Course, semester, sectionYear, building, room, schedule, startTime, instructor):
        self.set_course(course)
        self.departmentAbbreviation = self.course.departmentAbbreviation
        self.courseNumber = self.course.courseNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        student_section = Enrollment(student, self)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return

    def set_course(self, course: Course):
        # Questioning the addition of this function into Section.py, not stated in assignment guidelines, but 'feels' neccessary to set relationship between course and section. Not sure if it is neccessary though.
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    def __str__(self):
        return f"\nSection Number: {self.sectionNumber}" \
               f"\nDepartment abbr: {self.departmentAbbreviation}," \
               f"Course Number: {self.courseNumber}," \
               f"Semester: {self.semester}" \
               f"\nSection Year: {self.sectionYear}," \
               f"Building: {self.building}," \
               f"Room: {self.room}" \
               f"\nSchedule: {self.schedule}," \
               f"Start Time: {self.startTime}," \
               f"Instructor: {self.instructor}"


"""
elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table(table_name, Base.metadata, autoload_with=engine)
        course: Mapped["Course"] = relationship(back_populates="sections")
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        courseNumber: Mapped[int] = column_property(__table__.c.course_number)
        sectionNumber: Mapped[int] = column_property(__table__.c.section_number)
        sectionYear: Mapped[int] = column_property(__table__.c.section_year)
        startTime: Mapped[Time] = column_property(__table__.c.start_time)

        def __init__(self, course: Course, semester, sectionYear, building, room, schedule, startTime, instructor):
            self.set_course(course)
            self.departmentAbbreviation = self.course.departmentAbbreviation
            self.courseNumber = self.course.courseNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor
"""






#setattr(Section, 'set_course', set_course)
#setattr(Section, '__str__', __str__)
