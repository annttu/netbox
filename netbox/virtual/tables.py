#
# Virtual Machine
#
import django_tables2 as tables
from django_tables2.utils import Accessor

from utilities.tables import BaseTable, ToggleColumn
from virtual.models import VirtualMachine, VirtualMachineGroup, VirtualCluster


STATUS_ICON = """
{% if record.status %}
    <span class="glyphicon glyphicon-ok-sign text-success" title="Active" aria-hidden="true"></span>
{% else %}
    <span class="glyphicon glyphicon-minus-sign text-danger" title="Offline" aria-hidden="true"></span>
{% endif %}
"""


class VirtualMachineTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('virtual:virtual_machine', args=[Accessor('pk')], verbose_name='Name')
    status = tables.TemplateColumn(template_code=STATUS_ICON, verbose_name='')
    virtual_cluster = tables.LinkColumn('virtual:virtual_cluster', args=[Accessor('virtual_cluster.pk')], verbose_name='Virtual Cluster')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    group = tables.LinkColumn('virtual:virtual_machine_group', args=[Accessor('group.pk')], verbose_name='Group')

    class Meta(BaseTable.Meta):
        model = VirtualMachine
        fields = ('pk', 'name', 'status', 'description', 'group', 'tenant', 'virtual_cluster')


class VirtualMachineGroupTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('virtual:virtual_machine_group', args=[Accessor('pk')], verbose_name='Name')

    class Meta(BaseTable.Meta):
        model = VirtualMachineGroup
        fields = ('pk', 'name', 'description')


class VirtualClusterTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('virtual:virtual_cluster', args=[Accessor('pk')], verbose_name='Name')

    class Meta(BaseTable.Meta):
        model = VirtualCluster
        fields = ('pk', 'name', 'description')
