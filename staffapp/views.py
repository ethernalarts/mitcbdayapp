from operator import attrgetter
from django.contrib import messages
# from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from staffapp.forms import staffDetailsCreateForm, staffDetailsUpdateForm
from staffapp.models import staffDetails


# Index View

class HomePageView(TemplateView):
    template_name = 'index.html'


# Staff List View
class StaffListView(ListView):
    model = staffDetails
    context_object_name = "stafflist"
    paginate_by = 3

    def get_template_names(self):
        if self.request.htmx and self.request.GET.get("page"):
            return "snippets/htmx-staff-list.html"
        return "stafflist.html"

    def get_queryset(self):
        return staffDetails.objects.all().order_by("first_name")

    def get_context_data(self, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        context["total_staff"] = staffDetails.objects.all().count()
        return context


# Add Staff View
class StaffCreateView(CreateView):
    model = staffDetails
    form_class = staffDetailsCreateForm
    template_name = "addstaff.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()

        messages.success(
            self.request,
            f"{str(self.object.first_name).title()} "
            f"{str(self.object.middle_name or "").title()} "
            f"{str(self.object.last_name).title()}'s profile has been created",
        )

        response = HttpResponse()
        response.headers["HX-Refresh"] = False
        response.headers["HX-Redirect"] = self.get_success_url()
        return response

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, f"{error}")
        return self.render_to_response(
            self.get_context_data(
                form=self.form_class(self.request.POST),
            )
        )


# Staff Detail View
class StaffDetailsView(DetailView):
    model = staffDetails
    context_object_name = "staff"
    template_name = "staffdetails.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super(StaffDetailsView, self).get_context_data(**kwargs)

        view_count = self.request.session.get('view_count', 0) + 1
        self.request.session['view_count'] = view_count

        context["tag"] = staffDetailsCreateForm
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Exception as e:
            messages.error(self.request, f"{e}")
            return HttpResponseRedirect(reverse("index"))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


# Update Staff View
class StaffUpdateView(UpdateView):
    form_class = staffDetailsCreateForm
    context_object_name = "staff"
    template_name = "updatestaff.html"
    model = staffDetails

    # def get_template_names(self):
    #     return self.object.get_absolute_url_update_staff()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Exception as e:
            messages.error(self.request, f"{e}")
            return HttpResponseRedirect(reverse("index"))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        messages.success(self.request, "Your Profile has been updated")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(
            self.get_context_data(form=self.form_class(self.request.POST))
        )


def staff_deleted(request):
    return render(request, "staffdeleted.html")


class StaffDeleteView(DeleteView):
    success_url = reverse_lazy("index")
    context_object_name = "staff"
    model = staffDetails

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        first_name = self.object.first_name
        middle_name = self.object.middle_name or ""
        last_name = self.object.last_name

        # self.request.session["first_name"] = first_name
        # self.request.session["middle_name"] = middle_name
        # self.request.session["last_name"] = last_name

        messages.success(
            self.request,
            f"{str(first_name).title()} "
            f"{str(middle_name).title()} "
            f"{str(last_name).title()}'s profile has been deleted"
        )

        self.object.delete()
        self.request.session.flush()

        # return HttpResponseRedirect(reverse("index"))

        response = HttpResponse()
        response["HX-Refresh"] = False
        response["Cache-Control"] = "max-age=60"
        response["HX-Redirect"] = reverse("index")
        return response

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data())


# Search view
class SearchQueryView(ListView):
    model = staffDetails
    context_object_name = "searchresult"
    paginate_by = 3

    def get_template_names(self):
        if self.request.htmx and self.request.GET.get("page"):
            return "snippets/htmx-searchresult-list.html"
        return "searchresult.html"

    # get search query object
    def get_queryset(self, query=None):
        query = self.request.GET.get("q", None) if self.request.GET.get("q") else ""
        queryset = []
        queries = query.split(" ")
        for q in queries:
            results = staffDetails.objects.filter(
                Q(first_name__icontains=q)
                | Q(middle_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(cadre__icontains=q)
            ).distinct()

            queryset.extend(iter(results))
        return sorted(list(set(queryset)), key=attrgetter("first_name"), reverse=True)

    # context data
    def get_context_data(self, **kwargs):
        context = super(SearchQueryView, self).get_context_data(**kwargs)
        context["query"] = str(self.request.GET.get("q"))
        context["total_results"] = len(self.get_queryset())
        return context
