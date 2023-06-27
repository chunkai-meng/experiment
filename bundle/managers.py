from django.db import models
from django.utils import timezone
from simple_history.exceptions import AlternativeManagerError, NotHistoricalModelError
from simple_history.utils import bulk_update_with_history


class ArchivableQuerySet(models.QuerySet):
    def delete(self):
        now = timezone.now()
        objs = self.all()
        for obj in objs:
            obj.updated_at = obj.removed_at = now
        try:
            bulk_update_with_history(
                objs, self.model, ["updated_at", "removed_at"], batch_size=500
            )
        except (AlternativeManagerError, NotHistoricalModelError):
            return False, 0
        return True, objs.count()


class ArchivableManager(models.Manager):
    def get_queryset(self):
        return ArchivableQuerySet(self.model, using=self._db).filter(removed_at=None)
