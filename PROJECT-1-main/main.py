from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define the database connection and session
engine = create_engine('sqlite:///./users.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    # Validate the registration form data
    if len(username) < 4:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username must be at least 4 characters long."})
    if len(password) < 6:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Password must be at least 6 characters long."})
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Passwords do not match."})
    
    # Check if the user already exists in the database
    db = SessionLocal()
    if db.query(User).filter_by(username=username).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists."})
    if db.query(User).filter_by(email=email).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already exists."})
    
    # Add the new user to the database
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Redirect the user to the login page
    return templates.TemplateResponse("index.html", {"request": request, "success": "Registration successful. Please log in."})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Validate the login form data
    db = SessionLocal()
    user = db.query(User).filter_by(username=username, password=password).first()
    if not user:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid username or password."})
    
    # Redirect the user to the dashboard
    return templates.TemplateResponse("dashboard.html", {"request": request})
