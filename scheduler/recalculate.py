import datetime
import calendar
from core.models import School
from finance.models import History

import logging
log = logging.getLogger('core')


def recalculate_schools():
    dt = datetime.datetime.today()
    last_day_number = calendar.monthrange(dt.year, dt.month)[1]
    for school in School.objects.filter(status=School.STATUSES[0][0]):
        if dt.day == school.repaymentDate or (last_day_number < school.repaymentDate and last_day_number == dt.day):
            log.debug('School: {school}, auto debit monthly fees start, date: {date}'.format(school=school, date=dt.day))
            for child in school.children.all():
                child.balance -= child.monthlyFee
                child.save()
                log.debug("Child balance after recalculations: {balance}".format(balance=child.balance))
                History.objects.create(school=school, child=child, debitAmount=child.monthlyFee)



