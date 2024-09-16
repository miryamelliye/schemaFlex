from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from .utils import get_model_from_cache


@shared_task
def send_confirmation_email(user_email, imported_count):
    subject = 'Data Import Completed'
    message = f'Your data import has been successfully completed. {imported_count} records were imported.'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])


@shared_task
def import_data_task(table_id, data):
    model = get_model_from_cache(table_id)
    objects = []
    errors = []

    for item in data:
        try:
            obj = model(**item)
            obj.full_clean()
            objects.append(obj)
        except Exception as e:
            errors.append({'data': item, 'errors': e})

    model.objects.bulk_create(objects, batch_size=1000)

    send_confirmation_email.delay('mielliye@gmail.com', len(objects))

    return {'imported': len(objects), 'errors': errors}
