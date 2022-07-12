
# Create your views here.

from multiprocessing import context
from django.template import Template, Context, loader
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import  (get_object_or_404, redirect, render)
from sendmail.models import staffDetails
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
    return render (request, 'index.html')
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
    model = staffDetails
    fields = [
        'first_name', 'middle_name', 'last_name', 'gender', 'phone_number', 'email', 
        'cadre', 'first_appointment', 'department', 'level', 'step', 'staff_image', 
        'birth_month', 'birth_day'
    ] 
    template_name = 'addstaff.html'
    model = staffDetails
    form_class = staffDetailsUpdateForm  
    context_object_name = 'staff' 
    template_name = 'updatestaff.html'
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