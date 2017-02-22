from copy import deepcopy
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from dcim.views import ComponentCreateView, ComponentEditView, ComponentDeleteView
from ipam.models import IPAddress
from utilities.views import BulkEditView, ObjectDeleteView, ObjectEditView, ObjectListView, BulkDeleteView
from virtual import forms
from virtual import tables
from .models import *



class VirtualMachineListView(ObjectListView):
    queryset = VirtualMachine.objects.all() #select_related('tenant')
    #filter = filters.SiteFilter
    #filter_form = forms.SiteFilterForm
    table = tables.VirtualMachineTable
    template_name = 'virtual/virtual_machine_list.html'


class VirtualComponentCreateView(View):
    parent_model = None
    parent_field = None
    model = None
    form = None
    model_form = None

    def get(self, request, pk):

        parent = get_object_or_404(self.parent_model, pk=pk)

        return render(request, 'virtual/virtual_component_add.html', {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': self.form(initial=request.GET),
            'return_url': parent.get_absolute_url(),
        })

    def post(self, request, pk):

        parent = get_object_or_404(self.parent_model, pk=pk)

        form = self.form(request.POST)
        if form.is_valid():

            new_components = []
            data = deepcopy(form.cleaned_data)

            for name in form.cleaned_data['name_pattern']:
                component_data = {
                    self.parent_field: parent.pk,
                    'name': name,
                }
                component_data.update(data)
                component_form = self.model_form(component_data)
                if component_form.is_valid():
                    new_components.append(component_form.save(commit=False))
                else:
                    for field, errors in component_form.errors.as_data().items():
                        for e in errors:
                            form.add_error(field, u'{}: {}'.format(name, ', '.join(e)))

            if not form.errors:
                self.model.objects.bulk_create(new_components)
                messages.success(request, u"Added {} {} to {}.".format(
                    len(new_components), self.model._meta.verbose_name_plural, parent
                ))
                if '_addanother' in request.POST:
                    return redirect(request.path)
                else:
                    return redirect(parent.get_absolute_url())

        return render(request, 'virtual/virtual_component_add.html', {
            'parent': parent,
            'component_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': parent.get_absolute_url(),
        })


class VirtualComponentEditView(ObjectEditView):
    def get_return_url(self, obj):
        return obj.virtual_machine.get_absolute_url()


class VirtualComponentDeleteView(ObjectDeleteView):
    def get_return_url(self, obj):
        return obj.virtual_machine.get_absolute_url()


def virtual_machine(request, pk):

    virtual_machine = get_object_or_404(VirtualMachine, pk=pk)

    interfaces = VirtualInterface.objects.order_naturally(1) \
        .filter(virtual_machine=virtual_machine)



    # Gather relevant device objects
    ip_addresses = IPAddress.objects.filter(virtual_interface__virtual_machine=virtual_machine).select_related('virtual_interface', 'vrf') \
        .order_by('address')
    #services = Service.objects.filter(device=device)
    #secrets = device.secrets.all()

    # Find any related devices for convenient linking in the UI
    #related_devices = []
    #if device.name:
    #    if re.match('.+[0-9]+$', device.name):
    #        # Strip 1 or more trailing digits (e.g. core-switch1)
    #        base_name = re.match('(.*?)[0-9]+$', device.name).group(1)
    #    elif re.match('.+\d[a-z]$', device.name.lower()):
    #        # Strip a trailing letter if preceded by a digit (e.g. dist-switch3a -> dist-switch3)
    #        base_name = re.match('(.*\d+)[a-z]$', device.name.lower()).group(1)
    #    else:
    #        base_name = None
    #    if base_name:
    #        related_devices = Device.objects.filter(name__istartswith=base_name).exclude(pk=device.pk) \
    #                              .select_related('rack', 'device_type__manufacturer')[:10]

    ## Show graph button on interfaces only if at least one graph has been created.
    #show_graphs = Graph.objects.filter(type=GRAPH_TYPE_INTERFACE).exists()

    return render(request, 'virtual/virtual_machine.html', {
        'virtual_machine': virtual_machine,
        #'console_ports': console_ports,
        #'cs_ports': cs_ports,
        #'power_ports': power_ports,
        #'power_outlets': power_outlets,
        'interfaces': interfaces,
        #'mgmt_interfaces': mgmt_interfaces,
        #'device_bays': device_bays,
        'ip_addresses': ip_addresses,
        #'services': services,
        #'secrets': secrets,
        #'related_devices': related_devices,
        #'show_graphs': show_graphs,
    })

class VirtualMachineEditView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'virtual.change_virtual_machine'
    model = VirtualMachine
    form_class = forms.VirtualMachineForm
    template_name = 'virtual/virtual_machine_edit.html'
    default_return_url = 'virtual:virtual_machine_list'


class VirtualMachineDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'virtual.delete_virtual_machine'
    model = VirtualMachine
    default_return_url = 'virtual:virtual_machine_list'


#class VirtualMachineBulkImportView(PermissionRequiredMixin, BulkImportView):
#    permission_required = 'dcim.add_site'
#    form = forms.SiteImportForm
#    table = tables.SiteTable
#    template_name = 'dcim/site_import.html'
#    default_return_url = 'dcim:site_list'
#
#
#class VirtualMachineBulkEditView(PermissionRequiredMixin, BulkEditView):
#    permission_required = 'virtual:change_virtual_machine'
#    cls = VirtualMachine
#    #filter = filters.SiteFilter
#    form = forms.VirtualMachineBulkEditForm
#    template_name = 'virtual/virtual_machine_bulk_edit.html'
#    default_return_url = 'virtual:virtual_machine_list'

#
# Interfaces
#

class VirtualInterfaceAddView(PermissionRequiredMixin, VirtualComponentCreateView):
    permission_required = 'virtual.add_virtualinterface'
    parent_model = VirtualMachine
    parent_field = 'virtual_machine'
    model = VirtualInterface
    form = forms.VirtualInterfaceCreateForm
    model_form = forms.VirtualInterfaceForm
    template_name = "virtual/virtual_interface_edit.html"

    def get_return_url(self, obj):
        return obj.virtual_machine.get_absolute_url()


class VirtualInterfaceEditView(PermissionRequiredMixin, VirtualComponentEditView):
    permission_required = 'virtual.change_virtualinterface'
    model = VirtualInterface
    form_class = forms.VirtualInterfaceForm


class VirtualInterfaceDeleteView(PermissionRequiredMixin, VirtualComponentDeleteView):
    permission_required = 'virtual.delete_virtualinterface'
    model = VirtualInterface

    template_name = "virtual/virtual_interface_delete.html"


class VirtualInterfaceBulkEditView(PermissionRequiredMixin, BulkEditView):
    permission_required = 'virtual.change_interface'
    cls = VirtualInterface
    parent_cls = VirtualMachine
    form = forms.VirtualInterfaceBulkEditForm
    template_name = 'virtual/virtual_interface_bulk_edit.html'


class VirtualInterfaceBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'virtual.delete_interface'
    cls = VirtualInterface
    parent_cls = VirtualMachine

#
# IP addresses
#

@permission_required(['virtual.change_virtualmachine', 'ipam.add_ipaddress'])
def ipaddress_assign(request, pk):

    virtual_machine = get_object_or_404(VirtualMachine, pk=pk)

    if request.method == 'POST':
        form = forms.IPAddressForm(virtual_machine, request.POST)
        if form.is_valid():

            ipaddress = form.save(commit=False)
            ipaddress.virtual_interface = form.cleaned_data['virtual_interface']
            ipaddress.save()
            form.save_custom_fields()
            messages.success(request, u"Added new IP address {} to interface {}.".format(ipaddress, ipaddress.interface))

            if form.cleaned_data['set_as_primary']:
                if ipaddress.family == 4:
                    virtual_machine.primary_ip4 = ipaddress
                elif ipaddress.family == 6:
                    virtual_machine.primary_ip6 = ipaddress
                virtual_machine.save()

            if '_addanother' in request.POST:
                return redirect('virtual:ipaddress_assign', pk=virtual_machine.pk)
            else:
                return redirect('virtual:virtual_machine', pk=virtual_machine.pk)

    else:
        form = forms.IPAddressForm(virtual_machine)

    return render(request, 'virtual/ipaddress_assign.html', {
        'virtual_machine': virtual_machine,
        'form': form,
        'return_url': reverse('virtual:virtual_machine', kwargs={'pk': virtual_machine.pk}),
    })

