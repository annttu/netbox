from django.db import models

# Create your models here.

from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from extras.models import CustomFieldModel, CustomFieldValue
from tenancy.models import Tenant
from utilities.models import CreatedUpdatedModel
from utilities.utils import csv_format
from django.db.models import Count, Q, ObjectDoesNotExist


IFACE_ORDERING_POSITION = 1
IFACE_ORDERING_NAME = 2
IFACE_ORDERING_CHOICES = [
    [IFACE_ORDERING_POSITION, 'Slot/position'],
    [IFACE_ORDERING_NAME, 'Name (alphabetically)']
]


@python_2_unicode_compatible
class VirtualMachineGroup(models.Model):
    """
    An arbitrary collection of virtual machines.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?group={}".format(reverse('virtual:virtual_machine_list'), self.pk)


@python_2_unicode_compatible
class VirtualMachine(CreatedUpdatedModel, CustomFieldModel):
    """
    Virtual Machine is a virtual computer instance.
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    group = models.ForeignKey('VirtualMachineGroup', related_name='groups', blank=True, null=True, on_delete=models.SET_NULL)
    tenant = models.ForeignKey(Tenant, related_name='virtual_machines', blank=True, null=True, on_delete=models.PROTECT)
    description = models.CharField(max_length=100, blank=True, help_text="Long-form name (optional)")
    comments = models.TextField(blank=True)
    custom_field_values = GenericRelation(CustomFieldValue, content_type_field='obj_type', object_id_field='obj_id')

    primary_ip4 = models.OneToOneField('ipam.IPAddress', related_name='primary_ip4_for_virtual', on_delete=models.SET_NULL,
                                       blank=True, null=True, verbose_name='Primary IPv4')
    primary_ip6 = models.OneToOneField('ipam.IPAddress', related_name='primary_ip6_for_virtual', on_delete=models.SET_NULL,
                                       blank=True, null=True, verbose_name='Primary IPv6')

    class Meta:
        ordering = ['group', 'name', 'tenant']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('virtual:virtual_machine', args=[self.pk])

    def to_csv(self):
        return csv_format([
            self.name,
            self.slug,
            self.group.name if self.group else None,
            self.description,
        ])


class VirtualInterfaceManager(models.Manager):

    def order_naturally(self, method=IFACE_ORDERING_POSITION):

        queryset = self.get_queryset()
        sql_col = '{}.name'.format(queryset.model._meta.db_table)
        ordering = {
            IFACE_ORDERING_POSITION: ('_slot', '_subslot', '_position', '_channel', '_name'),
            IFACE_ORDERING_NAME: ('_name', '_slot', '_subslot', '_position', '_channel'),
        }[method]
        return queryset.extra(select={
            '_name': "SUBSTRING({} FROM '^([^0-9]+)')".format(sql_col),
            '_slot': "CAST(SUBSTRING({} FROM '([0-9]+)\/[0-9]+\/[0-9]+(:[0-9]+)?$') AS integer)".format(sql_col),
            '_subslot': "CAST(SUBSTRING({} FROM '([0-9]+)\/[0-9]+(:[0-9]+)?$') AS integer)".format(sql_col),
            '_position': "CAST(SUBSTRING({} FROM '([0-9]+)(:[0-9]+)?$') AS integer)".format(sql_col),
            '_channel': "CAST(SUBSTRING({} FROM ':([0-9]+)$') AS integer)".format(sql_col),
        }).order_by(*ordering)

@python_2_unicode_compatible
class VirtualInterface(models.Model):
    """
    A physical data interface within a Device. An Interface can connect to exactly one other Interface via the creation
    of an InterfaceConnection.
    """
    virtual_machine = models.ForeignKey('VirtualMachine', related_name='interfaces', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

    objects = VirtualInterfaceManager()

    class Meta:
        ordering = ['virtual_machine', 'name']
        unique_together = ['virtual_machine', 'name']

    def __str__(self):
        return self.name

    @property
    def is_connected(self):
        return bool(self.connection)
