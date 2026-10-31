from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def enroll_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        full_name=student.full_name,
        specialty=student.specialty,
        status="enrolled"
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def expel_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db_student.status = "expelled"
        db.commit()
        db.refresh(db_student)
    return db_student

def transfer_student(db: Session, student_id: int, new_specialty: str):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db_student.specialty = new_specialty
        db.commit()
        db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

def generate_report(db: Session):
    active_records = db.query(
        models.Student.specialty,
        func.count(models.Student.id)
    ).filter(models.Student.status == "enrolled").group_by(models.Student.specialty).all()

    by_specialty = {specialty: count for specialty, count in active_records}
    total_active = sum(by_specialty.values())

    total_expelled = db.query(models.Student).filter(models.Student.status == "expelled").count()

    return {
        "active_students_by_specialty": by_specialty,
        "total_active_students": total_active,
        "total_expelled_students": total_expelled
    }