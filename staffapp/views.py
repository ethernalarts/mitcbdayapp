from multiprocessing import context
from operator import attrgetter

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.db.models import Q
from staffapp.models import staffDetails
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy
from staffapp.forms import *


# Index View
def index(request):
    return render(request, "index.html")


# Staff List View
class staffListView(ListView):
    model = staffDetails
    context_object_name = "stafflist"
    template_name = "stafflist.html"
    paginate_by = 10

    def get_queryset(self):
        return staffDetails.objects.all().order_by("first_name")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(staffListView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        context["title"] = "List of all Staff"
        context["total_staff"] = staffDetails.objects.all().count()
        return context


# Add Staff View
class staffDetailsCreate(CreateView):
    model = staffDetails
    form_class = staffDetailsCreateForm
    template_name = "addstaff.html"

    def get_queryset(self):
        return staffDetails.objects.all()

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(
            self.get_context_data(
                form=self.form_class(self.request.GET),
            )
        )


# Staff Detail View
class staffDetailsView(DetailView):
    model = staffDetails
    context_object_name = "staff"
    template_name = "staffdetails.html"

    def get_object(self, queryset=None):
        try:
            return staffDetails.objects.get(id=self.kwargs["pk"])
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist("Staff not found") from e

    def get_context_data(self, **kwargs):
        context = super(staffDetailsView, self).get_context_data(**kwargs)
        context["tag"] = staffDetailsCreateForm
        return context


# Update Staff View
class staffDetailsUpdate(UpdateView):
    form_class = staffDetailsUpdateForm
    context_object_name = "staff"
    template_name = "updatestaff.html"

    def get_queryset(self):
        return staffDetails.objects.all()

    def get_success_url(self):
        return reverse("staffdetails", kwargs={"pk": self.object.id})

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(
            self.get_context_data(
                form=self.form_class(self.request.POST)
            )
        )


def removeStaff(request, pk):
    obj = get_object_or_404(staffDetails, id=pk)

    if request.method == "POST":

        # save first name for context data
        first_name = obj.first_name

        # save middle name for context data
        if obj.middle_name:
            middle_name = obj.middle_name

        # save last name for context data
        last_name = obj.last_name

        # delete object
        obj.delete()

        context = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
        }

        # retrieve template to render
        t = loader.get_template("staffdeleted.html")

        # after deletion, redirect
        return HttpResponse(t.render(context))


# Search view
class searchQueryView(ListView):
    model = staffDetails
    template_name = "searchresult.html"
    context_object_name = "searchresult"
    paginate_by = 8

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
        # Call the base implementation first to get the context
        context = super(searchQueryView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        context["query"] = str(self.request.GET.get("q"))
        context["count_query"] = len(self.get_queryset())
        context["staffdata"] = staffDetails.objects.all()

        return context
