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
    CREATE TABLE public.story2
    (
        id integer NOT NULL DEFAULT nextval('story_id_seq'::regclass) ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
        title text COLLATE pg_catalog."default" NOT NULL,
        description text COLLATE pg_catalog."default" NOT NULL,
        body text COLLATE pg_catalog."default" NOT NULL,
        tags text[] COLLATE pg_catalog."default",
        created timestamp(4) with time zone NOT NULL DEFAULT now(),
        published boolean NOT NULL DEFAULT false,
        CONSTRAINT story_pkey PRIMARY KEY (id)
    )
    
    
    # Change DB credentials in db_utils.py from line no 9 to 12

## Running the app

    # Start the Flask development web server
    python3 server.py

Point your web browser to http://localhost:5000/
