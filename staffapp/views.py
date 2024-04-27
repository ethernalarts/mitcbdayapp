import contextlib
from operator import attrgetter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponseRedirect
)
from django.db.models import Q
from django.template import loader, Template
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView, TemplateView
)
from django.urls import reverse, reverse_lazy
from staffapp.forms import *
from staffapp.models import staffDetails


# Index View
def index(request):
    return render(request, "index.html")


# Staff List View
class staffListView(ListView):
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
        context = super(staffListView, self).get_context_data(**kwargs)
        context["total_staff"] = staffDetails.objects.all().count()
        return context


# Add Staff View
class staffDetailsCreate(CreateView):
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

        first_name = self.object.first_name
        middle_name = self.object.middle_name or ""
        last_name = self.object.last_name

        messages.success(
            self.request,
            f"{str(first_name).title()} "
            f"{str(middle_name).title()} "
            f"{str(last_name).title()}'s profile has been created",
        )
        response = HttpResponseRedirect(self.get_success_url())
        response["HX-Refresh"] = "false"
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
class staffDetailsView(DetailView):
    model = staffDetails
    context_object_name = "staff"
    template_name = "staffdetails.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super(staffDetailsView, self).get_context_data(**kwargs)

        view_count = self.request.session.get('view_count', 0) + 1
        self.request.session['view_count'] = view_count

        context["tag"] = staffDetailsCreateForm
        context["view_count"] = view_count
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
class staffDetailsUpdate(UpdateView):
    form_class = staffDetailsUpdateForm
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


class DeleteStaffView(DeleteView):
    success_url = reverse_lazy("index")
    context_object_name = "staff"
    model = staffDetails

    def get_object(self, queryset=None):
        return staffDetails.objects.get(id=self.kwargs["pk"])

    def form_valid(self, form):
        obj = self.get_object(queryset=None)

        first_name = obj.first_name
        middle_name = obj.middle_name or ""
        last_name = obj.last_name

        self.request.session["first_name"] = first_name
        self.request.session["middle_name"] = middle_name
        self.request.session["last_name"] = last_name

        context = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name
        }

        messages.success(
            self.request,
            f"{str(context["first_name"]).title()} "
            f"{str(context["middle_name"]).title()} "
            f"{str(context["last_name"]).title()}'s profile has been deleted"
        )

        self.object.delete()
        self.request.session.flush()

        response = HttpResponseRedirect(self.success_url)
        response["Cache-Control"] = "max-age=60"
        response["HX-Refresh"] = "false"
        return response

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data())


def delete_staff(request, pk):
    staff = staffDetails.objects.get(id=pk)

    first_name = staff.first_name
    middle_name = staff.middle_name or ""
    last_name = staff.last_name

    context = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name
    }

    staff.delete()

    template = Template("staffdeleted.html")

    messages.success(
        request,
        f"{str(context["first_name"]).title()} "
        f"{str(context["middle_name"]).title()} "
        f"{str(context["last_name"]).title()}'s profile has been deleted"
    )
    # template = loader.get_template("staffdeleted.html")
    return HttpResponseRedirect(reverse("staffdeleted"))


# Search view
class searchQueryView(ListView):
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
        context = super(searchQueryView, self).get_context_data(**kwargs)
        context["query"] = str(self.request.GET.get("q"))
        context["total_results"] = len(self.get_queryset())
        return context
