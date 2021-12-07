# django-entries

## Overview

Basic create-read-update-delete (CRUD) functionality for an `Entry` model.

The base [template](./entries/templates/base.html) makes use of light css and javascript:

1. `starter.css` [stylesheet](./entries/static/css/starter.css)
2. `pylon` 0.1.1 for `<hstack>` and `<vstack>` layouts
3. `htmx` 1.6.1 for html-over-the-wire functionality
4. `hyperscript` 0.9 for client-side reactivity
5. `simplemde` a simple markdown editor

## Quickstart

Install in your virtual environment:

```zsh
.venv> pip3 install django-entries # poetry add django-entries
```

Include package in main project settings file:

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'crispy_forms',  # add crispy_forms at least > v1.13, if not yet added
    'entries' # this is the new django-entries folder
]

# in project_folder/urls.py
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('entry/', include('entries.urls')) # new
]
```

Add to database:

```zsh
.venv> python manage.py migrate # adds the `Entry` model to the database.
```
