from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import EntryForm
from .models import Entry

EDITOR = "entries/entry_edit.html"
DETAIL = "entries/entry_detail.html"
FIRST_PAGE = "entries/entry_list.html"
NEXT_PAGE = "entries/entry_next.html"
ITEM_IN_PAGE = "entries/entry_item.html"
MAX_ITEMS_PER_PAGE = 2


@login_required
def edit_entry(request: HttpRequest, slug: str) -> TemplateResponse:
    entry = Entry.get_for_user(slug, request.user)
    url = reverse("entries:edit_entry", kwargs={"slug": slug})
    form = EntryForm(request.POST or None, instance=entry, submit_url=url)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                form.save()
        return redirect(entry.get_absolute_url())
    context = {"form": form, "edit_header": f"Update {entry.title}"}
    return TemplateResponse(request, EDITOR, context)


@login_required
def add_entry(request: HttpRequest) -> TemplateResponse:
    url = reverse("entries:add_entry")
    form = EntryForm(request.POST or None, submit_url=url)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.author = request.user
        entry.save()
        return redirect(entry.get_absolute_url())
    return TemplateResponse(
        request, EDITOR, {"form": form, "edit_header": "Write An Entry"}
    )


@login_required
@require_http_methods(["DELETE"])
def delete_entry(request: HttpRequest, slug: str) -> HttpResponse:
    url = reverse("entries:list_entries")
    entry = Entry.get_for_user(slug, request.user)
    response = HttpResponse(headers={"HX-Redirect": url})
    entry.delete()
    return response


def view_entry(request: HttpRequest, slug: str) -> TemplateResponse:
    return TemplateResponse(
        request, DETAIL, {"entry": get_object_or_404(Entry, slug=slug)}
    )


def set_context(request: HttpRequest, loader: str) -> TemplateResponse:
    """Add to the `url` from the `request` object's `q` and `next` parameters, if present."""

    # initialize
    context = {}
    context["template_for_item"] = ITEM_IN_PAGE  # template for each page item
    url = reverse("entries:scroll_entries")  # base url for infinity scrolling
    query = request.GET.get("q", None)  # get query from url, else None
    page_number = request.GET.get("next", 1)  # get next from url, else page 1

    # adds to base and filters queryset, if query available; else default
    qs = Entry.objects.all()
    if query:
        url = f"{url}?q={query}"
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )

    # set page from request
    paginator = Paginator(qs, MAX_ITEMS_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj

    # adds to base, if next page available
    next_num = None
    if page_obj.has_next:
        try:
            next_num = page_obj.next_page_number()
        except EmptyPage:
            next_num = None
    if next_num:
        context["next_page_url"] = f"{url}?next={next_num}"

    # return html fragment to the template loader
    return TemplateResponse(request, loader, context)


def list_entries(request: HttpRequest) -> TemplateResponse:
    return set_context(request, FIRST_PAGE)


def scroll_entries(request: HttpRequest) -> TemplateResponse:
    return set_context(request, NEXT_PAGE)


def view_about(request: HttpRequest) -> TemplateResponse:
    return TemplateResponse(request, "about.html", {})
