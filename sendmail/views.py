
# Create your views here.

import pathlib
from multiprocessing import context
from operator import attrgetter
from django.template import Template, Context, loader
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import  (get_object_or_404, redirect, render, HttpResponseRedirect)
from mitcbdayapp import settings
from django.db.models import Q
from sendmail.models import staffDetails
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import staffDetailsUpdateForm


# Birthday Check View
def bdaycheck(request):  
    data = staffDetails.objects.all()

    print("\nChecking...\n")

    if celebrants := [
            {
                'databaseid': record.id,
                'firstname': record.first_name,
                'middlename': record.middle_name,
                'lastname': record.last_name,
                'email': record.email,
                'phonenumber': record.phone_number
            } 
            for record in data if record.BIRTHDAY_TODAY
        ]:
        print("We have birthday(s) today: \n")

        for celebrant in celebrants:
            for key, value in celebrant.items():
                print(f'{key}: {value}')
            print('')            

        # t = loader.get_template('emailsent.html')
        # return HttpResponse(t.render(context = {'celebrants': celebrants, 'title': 'Birthdays Today'}))    
        return sendmail(request, celebrants)
    else:
        print("No birthdays today \n")
        t = loader.get_template('nobirthday.html')
        return HttpResponse(t.render())



# Sendmail View
def sendmail(request, celebrants):
    connection = mail.get_connection()
    connection.open()
    mail_count = 0
    failed = []

    print("Sending Birthday felicitation(s)...\n")

    contents = pathlib.Path('sendmail/templates/bmessage_1.html').read_text()
    for celebrant in celebrants:
        # convert 'contents' to a template object
        template = Template(contents)
        context = Context({"NAME": f"{celebrant.get('firstname')} {celebrant.get('lastname')}"})
        html_content = template.render(context)

        subject = f"Happy Birthday {celebrant.get('firstname')} {celebrant.get('lastname')}!!"
        from_ = f"MITC Edo State <{settings.EMAIL_HOST_USER}>"
        to_ = celebrant.get('email')

        msg = mail.EmailMultiAlternatives(subject, html_content, from_, [to_], connection = connection)
        msg.attach_alternative(html_content, "text/html")
        payload = msg.send()

        try:
            # this means the email was sent
            if payload == 1:

                # keeps count of the number of emails sent
                mail_count = mail_count + payload

                print(f"Birthday felicitation sent to {celebrant.get('email')} \n")

        except Exception as e:
            print(f"Birthday felicitation not sent to {celebrant.get('email')}. Reason: {e} \n")

            failed.append(celebrant)
    connection.close()

    if mail_count != len(celebrants):
        return HttpResponse(render(request, 'emailerror.html', context = {'failed_msgs': failed}))
    t = loader.get_template('emailsent.html')
    return HttpResponse(t.render(context = {'celebrants': celebrants, 'title': 'Birthdays Today'}))



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
    paginate_by = 5

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
