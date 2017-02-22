from django.conf.urls import url

from . import views


urlpatterns = [

    # Virtual Machines
    url(r'^virtual_machine/$', views.VirtualMachineListView.as_view(), name='virtual_machine_list'),
    url(r'^virtual_machine/add/$', views.VirtualMachineEditView.as_view(), name='virtual_machine_add'),
    url(r'^virtual_machine/edit/$', views.VirtualMachineEditView.as_view(), name='virtual_machine_bulk_edit'),
    url(r'^virtual_machine/import/$', views.VirtualMachineEditView.as_view(), name='virtual_machine_import'),

    url(r'^virtual_machine/(?P<pk>\d+)/$', views.virtual_machine, name='virtual_machine'),
    url(r'^virtual_machine/(?P<pk>\d+)/edit/$', views.VirtualMachineEditView.as_view(), name='virtual_machine_edit'),
    url(r'^virtual_machine/(?P<pk>\d+)/delete/$', views.VirtualMachineDeleteView.as_view(), name='virtual_machine_delete'),

    # Interfaces
    #url(r'^virtual_machine/interfaces/add/$', views.VirtualDeviceBulkAddInterfaceView.as_view(), name='device_bulk_add_interface'),
    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/add/$', views.VirtualInterfaceAddView.as_view(), name='virtual_interface_add'),
    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/(?P<virtualinterface>\d+)/$', views.VirtualInterfaceAddView.as_view(), name='virtual_interface_edit'),
    url(r'^virtual_interfaces/(?P<pk>\d+)/edit/$', views.VirtualInterfaceEditView.as_view(), name='virtual_interface_edit'),
    url(r'^virutal_interfaces/(?P<pk>\d+)/delete/$', views.VirtualInterfaceDeleteView.as_view(), name='virtual_interface_delete'),

    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/edit/$', views.VirtualInterfaceBulkEditView.as_view(), name='virtual_interface_bulk_edit'),
    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/delete/$', views.VirtualInterfaceBulkDeleteView.as_view(), name='virtual_interface_bulk_delete'),


    url(r'^devices/(?P<pk>\d+)/ip-addresses/assign/$', views.ipaddress_assign, name='ipaddress_assign'),

]
