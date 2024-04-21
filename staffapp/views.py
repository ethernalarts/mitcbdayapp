from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView, DetailView, UpdateView
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
        if self.request.htmx:
            if self.request.GET.get("page"):
                return "snippets/htmx-staff-list.html"
            return "searchresult.html"
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

    def get_queryset(self):
        return staffDetails.objects.all()

    def get_success_url(self):
        return self.object.get_absolute_url()

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
    model = staffDetails

    # def get_template_names(self):
    #     return self.object.get_absolute_url_update_staff()

    def get_object(self, queryset=None):
        try:
            return staffDetails.objects.get(id=self.kwargs["pk"])
        except ObjectDoesNotExist as e:
            raise ObjectDoesNotExist("User not found") from e

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


class DeleteStaffView(DeleteView):
    success_url = reverse_lazy("index")
    context_object_name = "staff"
    model = staffDetails

    def form_valid(self, form):
        obj = get_object_or_404(staffDetails, id=self.kwargs["pk"])
        first_name = obj.first_name
        middle_name = obj.middle_name or ""
        last_name = obj.last_name

        success_url = self.get_success_url()
        self.object.delete()
        messages.success(
            self.request,
            f"{str(first_name).title()} {str(middle_name).title()} {str(last_name).title()}'s profile has been deleted",
        )
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        for error in form.non_field_errors():
            messages.error(self.request, f"{error}")
        return self.render_to_response(self.get_context_data(form=form))


# Search view
class searchQueryView(ListView):
    model = staffDetails
    template_name = "searchresult.html"
    context_object_name = "searchresult"
    paginate_by = 3

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
        context["count_query"] = len(self.get_queryset())
        context["staffdata"] = staffDetails.objects.all()
        return context
