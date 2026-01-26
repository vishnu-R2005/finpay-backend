from datetime import date, timedelta
from bills.models import Bill
from .models import Notification

def create_due_bill_notifications():
    today = date.today()
    reminder_date = today + timedelta(days=1)

    due_bills = Bill.objects.filter(
        due_date=reminder_date,
        is_paid=False
    )

    for bill in due_bills:
        Notification.objects.create(
            user=bill.user,
            title="Bill Due Reminder",
            message=f"Your bill '{bill.title}' of ₹{bill.amount} is due tomorrow."
        )
