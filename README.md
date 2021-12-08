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
from django.views.generic import TemplateView
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('entry/', include('entries.urls')) # new
    path("", TemplateView.as_view(template_name="home.html")), # (optional: if fresh project install)
]
```

Add to database:

```zsh
.venv> python manage.py migrate # adds the `Entry` model to the database.
.venv> python manage.py createsuperuser # (optional: if fresh project install)
```

Run server and login to admin then logout:

1. Run `python manage.py runserver`
2. Visit `http://127.0.0.1:8000/entry/entries/list` assumes _entry_ as main folder in in `project_folder/urls.py`
3. There is no option to add a new blog since only logged in users are permitted.
4. Authentication is not part of this package so login via `http://127.0.0.1:8000/admin/` via created superuser
5. Visit `http://127.0.0.1:8000/entry/entries/list` again to see the `Add entry` button.
