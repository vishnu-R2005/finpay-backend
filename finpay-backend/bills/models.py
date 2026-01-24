from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Bill(models.Model):

    BILL_TYPE_CHOICES = (
        ('ONE_TIME', 'One Time'),
        ('RECURRING', 'Recurring'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bills'
    )

    title = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bill_type = models.CharField(
        max_length=10,
        choices=BILL_TYPE_CHOICES
    )

    due_date = models.DateField()

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
