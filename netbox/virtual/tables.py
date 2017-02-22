#
# Virtual Machine
#
import django_tables2 as tables
from django_tables2.utils import Accessor

from utilities.tables import BaseTable, ToggleColumn
from virtual.models import VirtualMachine, VirtualMachineGroup


class VirtualMachineTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('virtual:virtual_machine', args=[Accessor('pk')], verbose_name='Name')

    class Meta(BaseTable.Meta):
        model = VirtualMachine
        fields = ('pk', 'name', 'description', 'group', 'tenant')


class VirtualMachineGroupTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('virtual:virtual_machine_group', args=[Accessor('pk')], verbose_name='Name')

    class Meta(BaseTable.Meta):
        model = VirtualMachineGroup
        fields = ('pk', 'name', 'description')
