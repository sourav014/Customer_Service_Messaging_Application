# Customer_Service_Messaging_Application

## Prerequisites 
We assume you already have the following installed already: 
Python3 Postgres (we used Postgres 14.5, but newer or older versions should also work). Installation instructions for all platforms can be found here. Alternatively, a simple SQLite database could also work.

## Create the virtual environment using the Command.
	python3 -m venv venv
## Start the virtual environment using the command to download all the dependencies inside the virtual environment with the proper versions.
	source venv/bin/activate
## Start the project using the Command.
	django-admin startproject Branch_CS_Messaging_App
## Install the django dependency inside the environment using the command
	pip install django
## Create an app inside the folder named messaging_service using the command
	python3 manage.py startapp messaging_service
## Create another app inside the folder name user_service using the command
	python3 manage.py startapp user_service
## Define the schemas inside the models.py file of user_service folder for User schema and Message or Query schema in messaging
	Then define database credentials inside the settings.py file.
## To create the tables inside the database run the commands.
	python3 manage.py makemigrations
	python3 manage.py migrate
## Start the server using the Command.
	python3 manage.py runserver
After this the app will be ready to use and use below APIs to interact with the app.

## API Documentation
	https://documenter.getpostman.com/view/15932967/2s8YemuZii#4910ad1f-3851-4985-8b64-4045ddcd603a

## Application Documentation
	https://docs.google.com/document/d/1oGfRl_xgdmTtau9yl3_EElVRWoMZQtTpAAdNtE8WnfY/edit?usp=sharing

## Demo of the Application
<video src="https://drive.google.com/file/d/1SxtRlEk1qQp7tTykArM_ASg9RxCvYvLn/view?usp=sharing"></video>
