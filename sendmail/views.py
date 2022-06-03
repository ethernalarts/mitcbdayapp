
# Create your views here.
from django.template import Template, Context, loader
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import render
from mitcbdayapp import settings
from sendmail.models import staffDetails
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy


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
                {'databaseid': record.id, 
                 'firstname': record.first_name, 
                 'lastname': record.last_name, 
                 'email': record.email, 
                 'phonenumber': record.phone_number}
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
        
        # t = loader.get_template('bmessage_2.html')
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
    return render (request, 'index.html')


# Staff Detail View
class staffDetailsView(DetailView):
    model = staffDetails
    context_object_name = 'staff'  # your own name for the list as a template variable
    template_name = 'staffdetails.html'
           
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(staffDetailsView, self).get_context_data(**kwargs)
        
        # Create any data and add it to the context
        context['title'] = "Author's Details"
        return context


# Add Staff View
class staffDetailsCreate(CreateView):
    model = staffDetails
    fields = [
        'first_name', 'middle_name', 'last_name', 'phone_number', 'email',
        'birth_month', 'birth_day'
    ]
    template_name = 'addstaff.html'
    

# Update Staff View
class staffDetailsUpdate(UpdateView):
    model = staffDetails
    fields = [
        'first_name', 'middle_name', 'last_name', 'phone_number', 'email',
        'birth_month', 'birth_day'
    ]   
    template_name = 'book_update_form.html'
    

# Delete Staff View
class staffDetailsDelete(DeleteView):
    model = staffDetails
    #permission_required: 'catalog.can_renew'
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books')