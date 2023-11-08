# Overloop Django Tech Test Backend

## Running with Docker

- A sample Dockerfile and a docker-compose is provided to run the application in an isolated environment
- Make sure you have `docker` and `docker-compose` installed and that the Docker daemon is running
- Build and run the container: `docker-compose up`
- Run `docker-compose run app python3 setup_and_seed.py` to get a local database setup and seeded with lookup data
- Start making some requests: `curl http://localhost:8000/articles/`

## Running with a virtual environment

- To run the application in a virtual Python environment, follow these instructions. This example will create a virtual Python environment for 3.9.6
- Check you have the pyenv version you need: `pyenv versions`
- You should see 3.9.6s
- If you do not have the correct version of Python, install it like this: `pyenv install 3.9.6`
- On command line do this: `~/.pyenv/versions/3.9.6/bin/python -m venv env`
- This creates a folder called env. Then do this to activate the virtual environment: `source env/bin/activate`
- Lastly do this to check that you are now on the correct Python version: `python --version`
- You can install the dependencies with `pip install -r requirements.txt`
- You should run `python setup_and_seed.py` to get a local database setup and seeded with lookup data
- You can then run the app with `python manage.py runserver 0.0.0.0:8000` in the root directory

## Project Structure Notes

- There are two django apps installed `articles` and `regions`
- Django is used as a RESTful API, no html rendering is required
- Marshmallow is used to serialize and deserialize django object instances

## Tasks

- Add an new entity called `Author` with a `first_name` and a `last_name`. An API user should be able to create a new `Author`, edit an existing one and list all existing ones.
- Update the `Article` entity so that it relates to an `Author`. An API user should be able to select an `Author` and/or `Region` when creating or editing an `Article`.
- A user should be allowed to enter an `Article` with no `Author`, or remove the `Author` from an existing `Article`.
- An API user should be able to perform the following actions for each `Article`, `Author` and `Region` entity:
    - Get all entities
    - Create a single entity
    - Get a single entity
    - Update a single entity
    - Delete a single entity
- The app should be robust and you should make sure that everything works as specified.
- Add unit tests for any code written to implement the tasks using a testing framework of your choice.

### Suggestions

- Poetry seems like phasing out plain virtualenv, consider using it.
- Pytets is fast and it's fixtures are amazing. Even using standard django tests can be much
pleasant with custom client (e.g. with put_json/post_json methods).
- There should be a way not to repeat model fields in marshmellow schema. At least for "usual"
fields. If not, that should be possible to implement.
- With time, urls for each django application should me moved to it's own module.
- Views should use generic views or application specific generic views (e.g. `View.dispatch` is very
generic and `AuthorView.dispatch` handles one more error case.
- `ObjectClass.objects.last()` in tests is not stable (at least for postgresql). For that models
should have ordering.
- `class Meta(object)` - python2 atavisms
- I'd change `super(AuthorView, self).dispatch(...)` to `super().dispatch()`
- Some tests test too much (e.g. article update test)
- Creating objects in schema seems very strange. Schemas should be used for validation, object
handling responsibility of views (actually it's even better to move it to business logic level).
It's possible to overwrite existing object when creating object of that type when ID of that
existing object is supplied (fixed in AuthorsView).

### Questions

- Is the ability to create new authors with article needed?
- Decision on REST related/nested object format needed (e.g. HATEOAS, https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#use-hateoas-to-enable-navigation-to-related-resources)
- Should author's resource return list of authors articles? If yes, should that field be updatable?
