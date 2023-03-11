FastAPI Project README
This FastAPI project is a web application that allows users to do user registration, and Viewing details.
This README file contains information on how to set up and use the project.
Installation
To install the project, follow these steps:

1.Clone the repository to your local machine:
  open gitbash
  git clone https://github.com/your-username/your-project.git
2.Create a virtual environment and activate it:
  bash
  python -m venv venv
  source venv/bin/activate
3.Install the project dependencies:
  pip install -r requirements.txt
4.Database creation
 To create the databases, follow these steps:
  PostgreSQL
  1.Open a terminal and navigate to the root directory of the project.
  2.Start the PostgreSQL server:
  3.Create the database:
    CREATE DATABASE your_postgres_database_name;
  MongoDB
    1.Open a terminal and navigate to the root directory of the project.
    2.Start the MongoDB server:
    3.Switch to the database you want to use:
      use your_mongodb_database_name
5.Start the FastAPI server:
  uvicorn main:app --reload


