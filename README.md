(I have assumed that you have python and pipenv installed)

- Open a new terminal and cd into this directory
- `$ pipenv install --ignore-pipfile` to install dependencies into a virtual environment
- `$ pipenv shell`
- `$ flask run` - the app will now be running on localhost:5000
- Ctrl+c to exit
- `$ python test.py` to run the unit tests
- `$ python` to open a python session
- `>>> from app import functions`
- `>>> function.find_stores(postcode, radius)` - use this command to test the find_stores function by entering a postcode and radius in kilometers
