from django.db.models import TextChoices


class ExpenseTypeChoice(TextChoices):
    PROFIT = 'profit', 'Profit'
    LOSS = 'loss', 'Loss'

