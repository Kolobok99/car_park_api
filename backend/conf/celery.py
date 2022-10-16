import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

app = Celery('car_park')

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
	'check-last-inspection': {
		'task': "cabinet.tasks.check_last_inspection",
		'schedule': crontab(minute='*/60'),
	},
	'delete-empty-card': {
		'task': "cabinet.tasks.delete_empty_card",
		'schedule': crontab(minute='*/60'),
	},
	'check-car-docs-date': {
		'task': "cabinet.tasks.check_car_docs_date",
		'schedule': crontab(minute='*/60'),
	},
	'check_user_docs_date': {
		'task': "cabinet.tasks.check_user_docs_date",
		'schedule': crontab(minute='*/60'),
	},
	'create-note-about-ending-cards': {
		'task': "cabinet.tasks.create_note_about_ending_cards",
		'schedule': crontab(minute='*/60'),
	},

}