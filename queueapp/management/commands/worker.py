from datetime import datetime
import os
import platform
from setproctitle import setproctitle
import sys
import time
import traceback

from django.core.management.base import BaseCommand, CommandError

from integlib.logbook_utils import configure_logging

from queueapp.models import Queue, JiraPoller, AutoFilter, NopFilter, JenkinsActuator, Log
from queueapp.utils import Tee

FULL_RUN_INTERVAL = 120  # do a full run each 2 minutes

PROCNAME = 'this is the queueapp worker process'
TEEFILE = '/tmp/queueapp_worker'


def get_active_comp(comp_class, queue):
    return comp_class.objects.filter(queue=queue).exclude(is_active=False)


class Command(BaseCommand):
    help = 'Run the queueapp worker process'

    def __init__(self, *args, **kwargs):
        self.pid = os.getpid()
        self.first_run = True

        setproctitle(f'{PROCNAME}:{self.pid}')

        teefile = open(f'{TEEFILE}.{self.pid}', 'wb', buffering=0)
        sys.stdout = Tee(sys.stdout, teefile)
        sys.stderr = Tee(sys.stderr, teefile)

        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        if platform.system() == 'Darwin' and ('TMPDIR' not in os.environ
                                              or not os.environ['TMPDIR'].startswith('/Volumes/')):
            self.stderr.write(
                'Macintosh traditionally defaults to a case-insensitive FS, bless its little soul.\n'
                'I am assuming that this is the case on this computer (CBA to test it properly).\n'
                'Set the TMPDIR environment variable pointing to a case-sensitive FS to continue.')
            return

        verbosity = int(options['verbosity'])
        configure_logging(verbose=verbosity > 1)

        while True:
            self.stdout.write('\n\n---')
            started = datetime.now()
            self.stdout.write(f'Started a full run on {started}')

            self.full_run()
            self.first_run = False

            duration = datetime.now() - started
            self.stdout.write(f'The run took {duration}')
            duration_sec = duration.total_seconds()
            if duration_sec < FULL_RUN_INTERVAL:
                pause = FULL_RUN_INTERVAL - duration_sec
                self.stdout.write(f'Chilling for {pause} seconds')
                time.sleep(pause)

    def full_run(self):
        queues = list(Queue.objects.exclude(is_active=False))

        self.stdout.write('The following queues are active:')
        for q in queues:
            self.stdout.write(f'- {q.name}')
            if self.first_run:
                q.log(f'Worker process started, pid={self.pid}')

        for q in queues:
            jpoller = get_active_comp(JiraPoller, q).first()
            if jpoller:
                self.run_and_log_errors(jpoller)

            nopfilters = get_active_comp(NopFilter, q)
            for filter in nopfilters:
                self.run_and_log_errors(filter)

            autofilters = get_active_comp(AutoFilter, q)
            for filter in autofilters:
                self.run_and_log_errors(filter)

            actuator = get_active_comp(JenkinsActuator, q).first()
            if actuator:
                self.run_and_log_errors(actuator)

            Log.truncate_logs(q)

    def run_and_log_errors(self, runnable):
        try:
            runnable.run()
        except KeyboardInterrupt:
            self.stderr.write('Received ^C, quitting')
            raise
        except:
            self.stderr.write(f'An error occurred in {runnable}')
            self.stderr.write(traceback.format_exc())
