from django.core.management.base import BaseCommand
from django_q.tasks import schedule


class Command(BaseCommand):
    """
    Custom management command for scheduling the update of the database.

    Inherits from Django's BaseCommand class.
    """
    help = 'Run utility function to update the database '

    def handle(self, *args, **options):
        """
        Handle the execution of the command.

        Schedules the synchronization of Hacker News items using Django-Q's schedule function.

        """
        schedule('hackernews.scheduler.tasks.schedule_sync_news', name='hackernewsScheduler', hook='hackernews.scheduler.hooks.print_result', schedule_type='I', minutes=5, repeats=-1)

        print(f'hackernewsScheduler created and will run every 5 mintues')




