
# Create your views here.
from multiprocessing import context
from django.template import Template, Context, loader
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import  (get_object_or_404, redirect, render, HttpResponseRedirect)
from mitcbdayapp import settings
from django.db.models import Q
from sendmail.models import staffDetails
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.generic import DetailView
from django.urls import reverse, reverse_lazy


# Birthday Check View
def bdaycheck(request):  
    celebrants = []  
    data = staffDetails.objects.all()
    
    print("\nChecking...\n")

    # iterate over the QuerySet "data" to look for any record with "birth_month" 
    # and "birth_day" fields that matches "current_month" and "current_day"
    for record in data:
        if record.BIRTHDAY_TODAY:

            celebrants.append(
                {
                    'databaseid': record.id,
                    'firstname': record.first_name,
                    'middlename': record.middle_name,
                    'lastname': record.last_name,
                    'email': record.email,
                    'phonenumber': record.phone_number
                }
            )

    # no birthdays today
    if (len(celebrants) == 0):    
            
        print("No birthdays today \n")        
        t = loader.get_template('nobirthday.html')        
        return HttpResponse(t.render())    
    
    # there is one or more birthdays today
    else:
        print("We have birthday(s) today: \n")
                
        for celebrant in celebrants:
            for key, value in celebrant.items():
                print(f'{key}: {value}')
            print('')            
        
        # t = loader.get_template('emailsent.html')
        # return HttpResponse(t.render(context = {'celebrants': celebrants, 'title': 'Birthdays Today'}))    
        return sendmail(request, celebrants)



# Sendmail View
def sendmail(request, celebrants):
    connection = mail.get_connection()
    connection.open()
    mail_count = 0
    failed = []

    print("Sending Birthday felicitation(s)...\n")

    with open(f'sendmail/templates/bmsg.html') as bmsg:
            contents = bmsg.read()
            
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
            pass

    connection.close()

    # all emails were sent
    if mail_count == len(celebrants):
        t = loader.get_template('emailsent.html')
        return HttpResponse(t.render(context = {'celebrants': celebrants, 'title': 'Birthdays Today'}))
    
    # one or more messages failed to send
    else:   
        return HttpResponse(render(request, 'emailerror.html', context = {'failed_msgs': failed}))



# Index View
def index(request):
    context = {'title': 'Homepage'}
    return render (request, 'index.html', context)



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
        context['title'] = "Staff's Details"
        context['phone_number_default'] = staffDetails._meta.get_field('phone_number').get_default()
    
        return context
    


# Add Staff View
class staffDetailsCreate(CreateView):
    model = staffDetails
    fields = [
        'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
        'cadre', 'level', 'step', 'staff_image', 'birth_month', 'birth_day'
    ] 
    template_name = 'addstaff.html'
    
    

# Update Staff View
class staffDetailsUpdate(UpdateView):
    model = staffDetails
    context_object_name = 'staff'
    fields = [
        'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
        'cadre', 'level', 'step', 'staff_image', 'birth_month', 'birth_day'
    ]   
    template_name = 'updatestaff.html'
    


# Delete Staff View
class staffDetailsDelete(DeleteView):
    model = staffDetails
    def get_success_url(self):
        return reverse(
            'staffdeleted',
            kwargs={                
                'first_name': self.object.first_name,
                'middle_name': self.object.middle_name,
                'last_name': self.object.last_name
            }
        )    


# remove Staff
def removeStaff(request, id):
    # list to copy some data 
    list = []
    
    # fetch the object related to passed id
    obj = get_object_or_404(staffDetails, id=id)
    
    if request.method == "POST":
        list.append(
                first_name = obj.first_name,
                middle_name = obj.middle_name,
                last_name = obj.last_name
        )
        
        # delete object
        obj.delete()
        
        # after deletion, redirect...
        t = loader.get_template('staffdeleted.html')
        return HttpResponse(t.render(context = list))
    
    

# Staff Removed Confirmation
def staffDeleted(request):
    return (request, 'staffdeleted.html')
    

# Search
class SearchResultView(ListView):
    model = staffDetails
    template_name = 'searchresult.html'
    context_object_name = 'searchresult'
    paginate_by = 5
    ordering = ['id']
    
    def get_queryset(self): 
        query = self.request.GET.get("q")
        
        if query:
            object_list = staffDetails.objects.filter(
                Q(first_name__icontains=query) | Q(middle_name__icontains=query) | Q(last_name__icontains=query)
            )            
            return object_list.all()
        
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SearchResultView, self).get_context_data(**kwargs)
        
        #paginator setup start
        #paginator = Paginator(queryset,3)
        
        # Create any data and add it to the context
        context['title'] = 'Search Results'
        context['query'] = self.request.GET.get("q")
        context['count_query'] = self.get_queryset().count()
        
        return context