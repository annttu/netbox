from django import forms

from extras.forms import CustomFieldBulkEditForm, CustomFieldForm
from ipam.models import IPAddress
from tenancy.models import Tenant
from utilities.forms import BootstrapMixin, SlugField, ExpandableNameField, BulkEditForm, BulkImportForm, CSVDataField
from virtual.models import VirtualMachine, VirtualInterface, VirtualMachineGroup, VirtualCluster


class VirtualMachineGroupForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = VirtualMachineGroup
        fields = ['name', 'description', 'slug']


class VirtualClusterForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = VirtualCluster
        fields = ['name', 'description', 'slug']


class VirtualMachineForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = VirtualMachine
        fields = ['name', 'description', 'slug', 'comments', 'tenant', 'group', 'status', 'virtual_cluster']


class VirtualMachineBulkEditForm(BootstrapMixin, CustomFieldBulkEditForm):
    pk = forms.ModelMultipleChoiceField(queryset=VirtualMachine.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        nullable_fields = []


class VirtualMachineFromCSVForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(Tenant.objects.all(), to_field_name='name', required=False,
                                    error_messages={'invalid_choice': 'Tenant not found.'})
    group = forms.ModelChoiceField(VirtualMachineGroup.objects.all(), to_field_name='name', required=False,
                                   error_messages={'invalid_choice': 'Virtual Machine Group not found.'})

    class Meta:
        model = VirtualMachine
        fields = ['name', 'slug', 'tenant', 'group', 'description']


class VirtualMachineImportForm(BootstrapMixin, BulkImportForm):
    csv = CSVDataField(csv_form=VirtualMachineFromCSVForm)

#
# Interfaces
#

class VirtualInterfaceForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = VirtualInterface
        fields = ['virtual_machine', 'name', 'description']
        widgets = {
            'virtual_machine': forms.HiddenInput(),
        }


class VirtualInterfaceCreateForm(BootstrapMixin, forms.Form):
    name_pattern = ExpandableNameField(label='Name')
    description = forms.CharField(max_length=100, required=False)


class VirtualInterfaceBulkEditForm(BootstrapMixin, BulkEditForm):
    pk = forms.ModelMultipleChoiceField(queryset=VirtualInterface.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(max_length=100, required=False)

    class Meta:
        nullable_fields = ['description']


#
# Virtual Cluster
#

#class VirtualCluster()

#
# IP addresses
#

class IPAddressForm(BootstrapMixin, CustomFieldForm):
    set_as_primary = forms.BooleanField(label='Set as primary IP for virtual machine', required=False)

    class Meta:
        model = IPAddress
        fields = ['address', 'vrf', 'tenant', 'status', 'virtual_interface', 'description']

    def __init__(self, virtual_machine, *args, **kwargs):

        super(IPAddressForm, self).__init__(*args, **kwargs)

        self.fields['vrf'].empty_label = 'Global'

        interfaces = virtual_machine.interfaces.all()
        self.fields['virtual_interface'].queryset = interfaces
        self.fields['virtual_interface'].required = True

        # If this device has only one interface, select it by default.
        if len(interfaces) == 1:
            self.fields['virtual_interface'].initial = interfaces[0]

        # If this device does not have any IP addresses assigned, default to setting the first IP as its primary.
        if not IPAddress.objects.filter(virtual_interface__virtual_machine=virtual_machine).count():
            self.fields['set_as_primary'].initial = True
