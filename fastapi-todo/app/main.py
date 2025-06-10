# ==== app/main.py ====
from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from . import models, database, auth, crud, schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/register")

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    if crud.get_user_by_username(db, username):
        return {"error": "User already exists"}
    hashed_pw = auth.get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, username, password)
    if not user:
        return {"error": "Invalid credentials"}
    return RedirectResponse(f"/tasks_html?user_id={user.id}", status_code=302)

@app.get("/tasks_html", response_class=HTMLResponse)
def read_tasks_html(user_id: int, request: Request, db: Session = Depends(database.get_db)):
    tasks = crud.get_tasks(db, user_id)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks, "user_id": user_id})

@app.post("/tasks")
def create_task(title: str = Form(...), user_id: int = Form(...), db: Session = Depends(database.get_db)):
    crud.create_task(db, user_id, title)
    return RedirectResponse(f"/tasks_html?user_id={user_id}", status_code=302)

@app.post("/tasks/delete")
def delete_task(task_id: int = Form(...), user_id: int = Form(...), db: Session = Depends(database.get_db)):
    crud.delete_task(db, task_id)
    return RedirectResponse(f"/tasks_html?user_id={user_id}", status_code=302)

@app.post("/tasks/update")
def update_task(task_id: int = Form(...), title: str = Form(...), user_id: int = Form(...), db: Session = Depends(database.get_db)):
    crud.update_task(db, task_id, title)
    return RedirectResponse(f"/tasks_html?user_id={user_id}", status_code=302)

@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def read_task_detail(task_id: int, request: Request, db: Session = Depends(database.get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        return HTMLResponse("Task not found", status_code=404)
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})

