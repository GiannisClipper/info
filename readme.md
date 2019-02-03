For Heroku deployment:

Adding a Procfile

In order for us to successfully deploy any application to Heroku, we must add a Procfile to that application.

Before we can add a Procfile, we need to first install a web server called Gunicorn. Run the following command within the application folder.

pip install gunicorn

Update the requirements file by running

pip freeze > requirements.txt

Create a new file with Procfile as the name and do not add any extension. Add this line below

web: gunicorn app:app

web is used by Heroku to start a web server for the application. The app:app specifies the module and application name. In our application we have the app module and our flask application is also called app. If your’s are different you can change them.