from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
ITEM_IN_PAGE = "entries/entry_list_item.html"
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
    return TemplateResponse(
        request,
        EDITOR,
        {
            "form": form,
            "edit_header": f"Update {entry.title}",
        },
    )


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
        request,
        EDITOR,
        {
            "form": form,
            "edit_header": "Write An Entry",
        },
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
    context = {"entry": get_object_or_404(Entry, slug=slug)}
    return TemplateResponse(request, DETAIL, context)


def set_context(request: HttpRequest, loader: str) -> TemplateResponse:
    qs = Entry.objects.all().order_by("created")
    paginator = Paginator(qs, MAX_ITEMS_PER_PAGE)
    page_number = request.GET.get("next", 1)
    context = {
        "page_obj": paginator.get_page(page_number),
        "template_for_item": ITEM_IN_PAGE,
        "get_next_page_url": reverse("entries:scroll_entries"),
    }
    return TemplateResponse(request, loader, context)


def list_entries(request: HttpRequest) -> TemplateResponse:
    return set_context(request, FIRST_PAGE)


def scroll_entries(request: HttpRequest) -> TemplateResponse:
    return set_context(request, NEXT_PAGE)


def view_about(request: HttpRequest) -> TemplateResponse:
    return TemplateResponse(request, "about.html", {})
