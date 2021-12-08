# Concept

1. A view divides a queryset into different pages.
2. The first page will hold a fixed number of items to be displayed.
3. When the last item in page one is `revealed` scrolled to, a trigger is sent via `htmx`.
4. `htmx` can then pull page two and step 3 is repeated.

## Requisites

1. Load htmx in the base template
2. Declare a context that will be used in two views
3. Declare two views: the initial template to load page 1, the subsequent template to load other pages
4. Add the two views to the urlpatterns
5. Configure the template patterns declared in the view, i.e.
