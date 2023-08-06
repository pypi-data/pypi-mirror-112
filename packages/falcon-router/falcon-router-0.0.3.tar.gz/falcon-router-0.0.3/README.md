# Falcon Router

Simple router lib for [Falcon framework](https://falcon.readthedocs.io/en/stable/) parcels.

## Idea

Falcon's default router requires specifying routes by using `app.add_route()` syntax. While this
might not be a problem with small API's, it is not very friendly to repeat this line for large
API with over 50 routes. This is where Falcon Router comes in.

## Features

- Both ASGI and WSGI apps supported
- Single router file supported
- Multiple router files/groups list supported
- Ending trailing slash supported


## Usage

Basic (single route file) and advanced usage (multiple route groups/files) can be found under
[examples](https://gitlab.com/vojko.pribudic/falcon-router/-/tree/master/examples).


## Credits

Falcon Router is heavily inspired by [falcon-url-versioning](https://github.com/paneru-rajan/falcon-url-versioning)


## Installing Falcon Router

Falcon Router is available on PyPI:

```console
$ python -m pip install falcon-router
```