# metrc-python
Python backend for connecting with Metrc

## Instructions for example Flask server

Install [pipenv](https://pypi.org/project/pipenv/)

Clone this repostitory, go to the root folder, and run the following commands

`pipenv shell`

`pip install -r requirements.txt`

Now edit the file `example/flask/configs.yml.example` to have key value pairs of the states you have vendor keys in to those vendor keys and rename to `example/flask/configs.yml`

Now run the following and the server should run

`cd example/flask`

`flask run`
