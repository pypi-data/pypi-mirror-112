from datetime import timedelta
from django.utils import timezone

from NEMO_transaction_validation.models import Contest
from NEMO.models import UsageEvent


def auto_validate_transactions():
    outdated_transactions = UsageEvent.objects.filter(validated=False, end__lte=timezone.now() + timedelta(days=5))
    for ot in outdated_transactions:
        if not Contest.objects.filter(admin_approved=False, transaction=ot.id).exists():
            ot.validated = True
            ot.save()
