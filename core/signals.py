import datetime
import calendar
from django.dispatch import Signal
# from core.models import School

repayment_day_changed = Signal(providing_args=['prev_repayment_date', 'new_repayment_date', 'instance'])


def repayment_date_changed(sender, prev_repayment_date, new_repayment_date, instance, **kwargs):
    dt = datetime.datetime.today()
    last_day_number = calendar.monthrange(dt.year, dt.month)[1]

    # Implement logic here
    '''
    scenarios:
        #1  prev_repayment_date = 1; new_repayment_date = 20; dt.day = 10
        #2  prev_repayment_date = 1; new_repayment_date = 20; dt.day = 25
        #3  prev_repayment_date = 1; new_repayment_date = 20; dt.day = 20
        #4  prev_repayment_date = 1; new_repayment_date = 20; dt.day = 1
        #5  prev_repayment_date = 5; new_repayment_date = 10; dt.day = 1
        
        #6  prev_repayment_date = 10; new_repayment_date = 1; dt.day = 5
        #7  prev_repayment_date = 10; new_repayment_date = 1; dt.day = 15
        #8  prev_repayment_date = 10; new_repayment_date = 1; dt.day = 10
        #9  prev_repayment_date = 10; new_repayment_date = 1; dt.day = 1
        #10 prev_repayment_date = 15; new_repayment_date = 10; dt.day = 5
    '''

    for child in instance.children.all():
        child_daily_fee = child.monthlyFee / int(last_day_number)

        if prev_repayment_date < dt.day < new_repayment_date:  # 'MOVE FORWARD' covers scenarios: 1
            diff = abs(new_repayment_date - prev_repayment_date) + 1
            remaining_amount = child.monthlyFee - diff * child_daily_fee
            child.balance += remaining_amount
            # no need to charge for new month, when 'new_repayment_date' comes it automatically charges
            child.save()

        elif prev_repayment_date < new_repayment_date < dt.day:  # 'MOVE FORWARD' covers scenarios: 2
            diff = abs(new_repayment_date - prev_repayment_date) + 1
            remaining_amount = child.monthlyFee - diff * child_daily_fee
            child.balance += remaining_amount
            child.balance -= child.monthlyFee  # charge for new month, because 'new_repayment_date' has already passed
            child.save()

        elif prev_repayment_date < new_repayment_date == dt.day:  # 'MOVE FORWARD' covers scenarios: 3
            pass  # critical cases check scheduler work and analyze when it fires trigger

        elif new_repayment_date > prev_repayment_date == dt.day:  # 'MOVE FORWARD' covers scenarios: 4
            pass  # critical cases check scheduler work and analyze when it fires trigger

        elif dt.day < prev_repayment_date < new_repayment_date:  # 'MOVE FORWARD' covers scenarios: 5
            diff = abs(new_repayment_date - prev_repayment_date) + 1
            child.balance -= diff * child_daily_fee
            # no need to charge for new month, when 'new_repayment_date' comes it automatically charges
            child.save()

        elif new_repayment_date < dt.day < prev_repayment_date:  # 'MOVE BACKWARD' covers scenarios: 6
            diff = abs(prev_repayment_date - new_repayment_date) + 1
            remaining_amount = diff * child_daily_fee
            child.balance += remaining_amount
            child.balance -= child.monthlyFee  # charge for new month, because 'new_repayment_date' has already passed
            child.save()
        elif new_repayment_date < prev_repayment_date < dt.day:  # 'MOVE BACKWARD' covers scenarios: 7
            diff = abs(prev_repayment_date - new_repayment_date) + 1
            remaining_amount = diff * child_daily_fee
            child.balance += remaining_amount
            # no need to charge for new month, because on 'prev_repayment_date' it already charged
            child.save()
        elif new_repayment_date < prev_repayment_date == dt.day:  # 'MOVE BACKWARD' covers scenarios: 8
            pass  # critical
        elif prev_repayment_date > new_repayment_date == dt.day:  # 'MOVE BACKWARD' covers scenarios: 9
            pass  # critical
        elif dt.day < new_repayment_date < prev_repayment_date:  # 'MOVE BACKWARD' covers scenarios: 10
            diff = abs(prev_repayment_date - new_repayment_date) + 1
            remaining_amount = diff * child_daily_fee
            child.balance += remaining_amount
            # no need to charge for new month, when 'new_repayment_date' comes it automatically charges
            child.save()
        else:  # when previous and new repayment dates are same
            pass


repayment_day_changed.connect(repayment_date_changed, dispatch_uid='repayment_date_signal_id')
