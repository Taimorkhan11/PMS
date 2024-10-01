Django Project Management System

Overview
This project is a Project Management System built using Django and Django Rest Framework (DRF). The system allows users to:

Sign up and log in using JWT for authentication.
Create projects, add multiple users to the projects, and manage tasks within those projects.
Perform CRUD operations on tasks.
Implement soft delete for both projects and tasks.



Features
JWT Authentication: User authentication via JSON Web Tokens.
Project Management: Users can create projects with unique names, descriptions, and add users to the project.
Task Management: Within each project, users can create, read, update, and delete tasks. Each task includes a title, description, status, and due date.
Soft Delete: Both projects and tasks are marked as deleted (using a is_deleted flag) without actually removing them from the database.


Requirements
Python 3.8+
Django 4.0+
Django Rest Framework 3.12+
Simple JWT for JWT authentication



Create a Virtual Environment

python -m venv venv             # because I have linux
source venv/bin/activate        # command for linux

Install Dependencies
pip install -r requirements.txt


JWT Authentication
This is used in all APIs and you can get from the logic api there are 2 ways to authentication one is that we can signup and directly hit the apis with token but in my project firstly you can hit signp api after this login api and login api give you a access_token and refresh_token you use the access_token with following below syntax in postman or Frontend.

Authorization: Bearer <jwt_token>


