
# Create your views here.

import pathlib
from multiprocessing import context
from django.template import Template, Context, loader
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import  (get_object_or_404, redirect, render)
from mitcbdayapp import settings
from birthday.models import staffDetails
from django.urls import reverse


# Birthday Check View
def bdaycheck(request):    
    # sourcery skip: list-comprehension, move-assign-in-block
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
    if not celebrants:    

        print("No birthdays today \n")        
        t = loader.get_template('nobirthday.html')        
        return HttpResponse(t.render())    

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

    contents = pathlib.Path('birthday/templates/bmessage_1.html').read_text()
    for celebrant in celebrants:
        # convert 'contents' to a template object
        template = Template(contents)
        context = Context({"NAME": f"{celebrant.get('firstname')} {celebrant.get('lastname')}"})
        html_content = template.render(context)

        subject = f"Happy Birthday {celebrant.get('firstname')} {celebrant.get('lastname')}!!"
        from_ = f"MBTC Edo State <{settings.EMAIL_HOST_USER}>"
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