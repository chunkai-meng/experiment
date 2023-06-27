from django.db import models
from django.utils.timezone import now

from .managers import ArchivableManager


class ArchivableModel(models.Model):
    removed_at = models.DateTimeField(blank=True, null=True)

    objects = ArchivableManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.removed_at = now()
        self.save(update_fields=("removed_at",))
        return 1, {}


# Create your models here.
class Bundle(ArchivableModel, models.Model):
    name = models.CharField(max_length=100)
    length = models.IntegerField()
    parents = models.ManyToManyField(
        "self",
        symmetrical=False,
        help_text="The previous pack(s) that this was created from",
        blank=True,
        verbose_name="Source BulkPacks",
        related_name="children",
    )

    def __str__(self):
        return f"{self.id}-{self.name}"

    @property
    def get_length_value(self):
        return float(self.length or 0)

    @property
    def parent_pack_code(self):
        """Returns the parent pack of this pack, if any."""
        if self.parents.count() == 1:
            return self.parents.first()
        elif self.parents.count() > 1:
            return list(self.parents.values_list("id", flat=True))
        else:
            return ""
