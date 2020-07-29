
# flask_backend_boilerplate
Boilerplate for a flask backend with swagger and the app factory pattern and ready Google App Engine

Set up a backend in Flask with Swagger and the App factory pattern without reading a whole bunch of contradictory stuff on Medium!

This is meant to run with Python 3.7 and virtualenv

## Set up (Linux/Mac)
After cloning this repo, navigate to the working directory and set up a virtual environment and activate it:

    cd flask_backend_boilerplate
    virtualenv venv
    source venv/bin/activate
    
Now Install dependencies

    pip install -r requirements.txt
    
Now run the app

    bash env.sh
  Now you can go to [http://127.0.0.1:5000/api/](http://127.0.0.1:5000/api/) and see Swagger running

You can issue yourself an API token by using the only route that does not require authentication in Swagger and using the default admin username and password (you can see this in the env.sh file and the app.yaml file)

    ROOT_USER=admin@example.com
    ROOT_PASSWORD=Abcd1234!

See it live here: [https://boilerplate-flask-swagger.appspot.com/api/](https://boilerplate-flask-swagger.appspot.com/api/)
