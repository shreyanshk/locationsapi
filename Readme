Dependencies
------------
* Python 3.6
* Python Flask
* SQLAlchemy
* [Alembic](http://alembic.zzzcomputing.com/en/latest/)
* PostgreSQL

Assumptions
-----------
* A Postgres instance is running on localhost
* A role "**shreyansh**" is already created with write access to the database
>If for some reason this new role cannot be created then any previously created roles can be used. Just modify line 5 in "dbModels.py" and line 32 in "alembic.ini" appropriately.

Initialize DB
-------------
1. Open a terminal in the root directory of the project or, in other words, the directory where this file is located.
2. Execute command:
>alembic upgrade head

Start Server
------------
1. Open a terminal in the root directory of the project or, in other words, the directory where this file is located.
2. Execute command:
>python Server.py

API Documentation
-----------------
The APIs implemented are:
1. "/post_location", HTTP method = POST
>Accepts JSON with 3 values: string name, float lat, float lng
>Returns HTTP400 for malformed requests and HTTP409 if "name" already exists.
>Returns HTTP201 for successful requests.

2. "/get_using_self", HTTP method = GET
>Accepts 3 parameters in the URL with values: float dist, float lat, float lng
>Computation is handled in the server itself
>Returns HTTP400 for malformed requests.
>Returns JSON object on success with the structure {name: {lat, lng}}

3. "/get_using_postgres", HTTP method = GET
>Accepts 3 parameters in the URL with values: float dist, float lat, float lng
>Computation is handled by the Postgres extension earthdistance.
>Returns HTTP400 for malformed requests
