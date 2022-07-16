
# Create your views here.

from multiprocessing import context
from operator import attrgetter
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import  (get_object_or_404, redirect, render)
from django.db.models import Q
from birthday.models import staffDetails
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import staffDetailsUpdateForm
from rest_framework.decorators import api_view



# Index View
def index(request):
    return render (request, 'index.html')



# Staff List View
class staffListView(ListView):
    model = staffDetails
    context_object_name = 'stafflist'   # your own name for the list as a template variable
    template_name = 'stafflist.html'  # Specify your own template name/location
    paginate_by = 10
    
    def get_queryset(self):        
        return staffDetails.objects.all()
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(staffListView, self).get_context_data(**kwargs)
        
        # Create any data and add it to the context
        context['title'] = 'List of all Staff'
        context['total_staff'] = staffDetails.objects.all().count()
        return context
    


# Staff Detail View
class staffDetailsView(DetailView):
    context_object_name = 'staff'  # your own name for the list as a template variable
    template_name = 'staffdetails.html'
           
    def get_queryset(self):        
        return staffDetails.objects.all().distinct()
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(staffDetailsView, self).get_context_data(**kwargs)
        
        # Create any data and add it to the context
        context['phone_number_default'] = staffDetails._meta.get_field('phone_number').get_default()
    
        return context
    


# Add Staff View
class staffDetailsCreate(CreateView):
    model = staffDetails
    fields = [
        'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
        'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
        'birth_month', 'birth_day'
    ] 
    template_name = 'addstaff.html'
    
    

# Update Staff View
class staffDetailsUpdate(UpdateView):
    model = staffDetails
    form_class = staffDetailsUpdateForm  
    context_object_name = 'staff' 
    template_name = 'updatestaff.html'
    


# removeStaff view
def removeStaff(request, pk):  # sourcery skip: avoid-builtin-shadow
    # fetch the object related to passed id
    obj = get_object_or_404(staffDetails, id=pk)

    if request.method == "POST":    
        
        # list to copy some data before deletion
        list = [f"{obj.first_name}"]

        # save middle name for context
        if obj.middle_name:
            list.append(f"{obj.middle_name}")
        else:
            list.append('')

        # save last name for context
        list.append(f"{obj.last_name}")

        # delete object
        obj.delete()       

        # after deletion, redirect
        t = loader.get_template('staffdeleted.html')
        return HttpResponse(t.render(context={
                    'first_name': list[0],
                    'middle_name': list[1],
                    'last_name': list[2]
                }
                    )
                        )

  

# Search view
class searchQueryView(ListView):
    model = staffDetails
    template_name = 'searchresult.html'
    context_object_name = 'searchresult'
    paginate_by = 8

    # get search query object
    def get_queryset(self, query=None):
        query = self.request.GET.get("q", None) if self.request.GET.get("q") else ''
        queryset = []
        queries = query.split(" ")
        for q in queries:
            results = staffDetails.objects.filter(
                   Q(first_name__icontains=q) |
                    Q(middle_name__icontains=q) |
                    Q(last_name__icontains=q)
                ).distinct()

            queryset.extend(iter(results))
        return sorted(list(set(queryset)), key=attrgetter('first_name'), reverse=True)
    
    # context data
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(searchQueryView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        context['query'] = str(self.request.GET.get("q"))
        context['count_query'] = len(self.get_queryset())
        context['staffdata'] = staffDetails.objects.all()

        return context

