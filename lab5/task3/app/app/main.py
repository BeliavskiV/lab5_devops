from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import get_db

app = FastAPI(
    title="Учёт студентов по специальностям",
    description="Система учёта студентов с бизнес-логикой зачисления, отчисления, перевода и формирования отчётов.",
    version="1.0.0"
)

@app.post("/students/enroll", response_model=schemas.StudentResponse, summary="Зачислить студента")
def enroll_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db=db, student=student)

@app.post("/students/{student_id}/expel", response_model=schemas.StudentResponse, summary="Отчислить за неуспеваемость")
def expel_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.expel_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student

@app.post("/students/{student_id}/transfer", response_model=schemas.StudentResponse, summary="Перевести на другую специальность")
def transfer_student(student_id: int, transfer_data: schemas.StudentTransfer, db: Session = Depends(get_db)):
    student = crud.transfer_student(db=db, student_id=student_id, new_specialty=transfer_data.new_specialty)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student

@app.get("/reports/summary", response_model=schemas.ReportSummary, summary="Сформировать отчёт по обучению и отчислениям")
def get_report(db: Session = Depends(get_db)):
    return crud.generate_report(db=db)

@app.get("/students", response_model=List[schemas.StudentResponse], summary="Получить список всех студентов (CRUD)")
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db=db, skip=skip, limit=limit)

@app.get("/students/{student_id}", response_model=schemas.StudentResponse, summary="Получить студента по ID (CRUD)")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student

@app.delete("/students/{student_id}", summary="Удалить запись о студенте (CRUD)")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return {"message": "Студент успешно удален"}