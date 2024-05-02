import pathlib
from datetime import date
from django.contrib import messages
from django.template import Template, Context
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from mitcbdayapp import settings
from staffapp.models import staffDetails


class BirthdayCheckView(ListView):
    model = staffDetails
    context_object_name = "celebrants"
    # paginate_by = 2

    def get_template_names(self):
        if self.request.htmx and self.request.GET.get("page"):
            return "snippets/htmx-birthday-list.html"
        return "birthdaylist.html"

    def get_context_data(self, **kwargs):
        context = super(BirthdayCheckView, self).get_context_data(**kwargs)
        context["today"] = date.today()
        return context

    def get_queryset(self):
        return [
            staff
            for staff in staffDetails.objects.all()
            if (staff.date_of_birth.month, staff.date_of_birth.day)
               == (date.today().month, date.today().day)
        ]


def send_birthday_message(request, pk):
    celebrant = staffDetails.objects.get(id=pk)

    try:
        connection = mail.get_connection()
        connection.open()
    except Exception as e:
        messages.error(
            request,
            f"{e}"
        )
        return HttpResponse(
            render(
                request,
                'snippets/birthday-message-error.html',
                context={
                    "var": "Connection Error",
                    "pk": celebrant.id
                }
            )
        )

    contents = pathlib.Path('birthday/templates/bmessage-1.html').read_text()
    template = Template(contents)  # convert 'contents' to a template object
    context = Context({"NAME": f"{celebrant.firstname} {celebrant.lastname}"})
    html_content = template.render(context)
    subject = f"Happy Birthday {str(celebrant.firstname).title()} {str(celebrant.lastname).title()}!!"
    from_ = f"MBTC Edo State <{settings.EMAIL_HOST_USER}>"
    to_ = celebrant.official_email

    msg = mail.EmailMultiAlternatives(
        subject,
        html_content,
        from_,
        [to_],
        connection=connection
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        messages.error(
            request,
            f"{e}"
        )
        connection.close()
        return HttpResponse(
            render(
                request,
                'snippets/birthday-message-error.html',
                context={
                    "var": "Message not sent",
                    "pk": celebrant.id
                }
            )
        )
    else:
        connection.close()
        return HttpResponse(
            render(
                request,
                'snippets/birthday-message-success.html'
            )
        )


# def send_birthday_message_button(request):
#     return HttpResponse(
#         render(
#             request,
#             'snippets/send-birthday-message.html'
#         )
#     )
