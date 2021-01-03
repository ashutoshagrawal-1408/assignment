# Assignment

## Setting up a development environment

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/ashutoshagrawal-1408/assignment.git my_app

    # Create the 'my_app' virtual environment
    python3 -m venv my_app
    virtualenv my_app/

    # Install required Python packages
    cd ~/dev/my_app
    source my_app/bin/activate
    pip3 install -r requirements.txt

## Initializing the Database

    # Create DB tables story
    python manage.py init_db


## Running the app

    # Start the Flask development web server
    python3 server.py

Point your web browser to http://localhost:5000/
