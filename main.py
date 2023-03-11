from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# create SQLAlchemy engine and
engine = create_engine("postgresql://postgres:12345@localhost/fastdb")
Session = sessionmaker(bind=engine)
session = Session()

# create declarative base
Base = declarative_base()


# create Users table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String, unique=True, index=True)


# create Profile table
class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    profile_picture = Column(String)

    user = relationship(User, backref="profile")


# create tables in database
Base.metadata.create_all(engine)

# create FastAPI app
app = FastAPI()

# for registering template and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# define registration request body
class RegistrationRequest(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str = None


# define defult endpont
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# define registration endpoint
@app.post("/register")
async def register_user(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    email = form_data.get("email")
    phone = form_data.get("phone")
    password = form_data.get("password")
    profile_pic = form_data.get("profile")
    profile_picture = await profile_pic.read()

    # check if email or phone already exist
    if session.query(User).filter_by(email=email).first() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    if session.query(User).filter_by(phone=phone).first() is not None:
        raise HTTPException(status_code=400, detail="Phone already registered")

    # create user object and add to database session
    user = User(first_name=name, email=email, password=password, phone=phone)
    session.add(user)
    session.flush()  # make sure user.id is populated

    # create profile object and add to database session
    if profile_picture:
        profile = Profile(user_id=user.id, profile_picture=profile_picture)
        session.add(profile)

    # commit changes to database
    session.commit()

    return {"message": "User registered successfully"}


# define all users data getting endpoint
@app.get("/allusers")
def det_allusers(request: Request):
    # Retrieve the user details and profile picture from the database
    users = session.query(User).all()
    # return users
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )


# define get user endpoint
@app.get("/users/{user_id}")
def get_user(user_id: int, request: Request):
    # get user object from database
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # get profile object from database
    profile = session.query(Profile).filter_by(user_id=user_id).first()
    profile_pic = profile.profile_picture
    

    # return user and profile data as JSON
    return templates.TemplateResponse(
        "userdetails.html",
        {
            "request": request,
            "id": user.id,
            "full_name": user.first_name,
            "email": user.email,
            "phone": user.phone,
            "profile_picture": profile_pic if profile else None,
        },
    )

