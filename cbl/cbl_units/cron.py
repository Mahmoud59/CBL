from django.core.mail import send_mail
from visit.models import Visit
from datetime import date
from visit.signals import send_student_mail
from cbl_units.settings import EMAIL_HOST_USER


def get_ended_visits():
    return Visit.objects.filter(to__lte=date.today(), email_status=False)


def my_scheduled_job():
    visits = get_ended_visits()
    for visit in visits:
        emails = visit.students.values_list('email', flat=True)
        kwargs = {'visit': visit.name}
        send_student_mail(emails, **kwargs)
    visits.filter(email_status=False).update(email_status=True)
    # send_mail(
    #     'Subject',
    #     f"Message. + {x+1}",
    #     'mahmoudfarweez@gmail.com',
    #     ['ma7moudf3rweez@yahoo.com', 'mahmoud.farweez@shipblu.com'],
    # )

