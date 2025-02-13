from django.db.models import TextChoices


class KirimChiqimStatusChoice(TextChoices):
    PROFIT = 'profit', 'Profit'
    LOSS = 'loss', 'Loss'

