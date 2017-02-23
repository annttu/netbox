from django.conf.urls import url

from . import views


urlpatterns = [

    # Virtual Cluster
    url(r'^virtual_cluster/$', views.VirtualClusterListView.as_view(), name='virtual_cluster_list'),
    url(r'^virtual_cluster/add/$', views.VirtualClusterEditView.as_view(), name='virtual_cluster_add'),
    url(r'^virtual_cluster/(?P<pk>\d+)/$', views.virtual_cluster, name='virtual_cluster'),
    url(r'^virtual_cluster/(?P<pk>\d+)/edit/$', views.VirtualClusterEditView.as_view(), name='virtual_cluster_edit'),
    url(r'^virtual_cluster/(?P<pk>\d+)/delete/$', views.VirtualClusterDeleteView.as_view(), name='virtual_cluster_delete'),
    url(r'^virtual_cluster/import/$', views.VirtualClusterEditView.as_view(), name='virtual_cluster_import'),


    # Virtual Machine group
    url(r'^virtual_machine_group/$', views.VirtualMachineGroupListView.as_view(), name='virtual_machine_group_list'),
    url(r'^virtual_machine_group/add/$', views.VirtualMachineGroupEditView.as_view(), name='virtual_machine_group_add'),
    url(r'^virtual_machine_group/(?P<pk>\d+)/$', views.VirtualMachineGroupEditView.as_view(),
        name='virtual_machine_group'),
    url(r'^virtual_machine_group/import/$', views.VirtualMachineGroupEditView.as_view(), name='virtual_machine_group_import'),


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
    url(r'^virtual_interfaces/(?P<pk>\d+)/delete/$', views.VirtualInterfaceDeleteView.as_view(), name='virtual_interface_delete'),

    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/edit/$', views.VirtualInterfaceBulkEditView.as_view(), name='virtual_interface_bulk_edit'),
    url(r'^virtual_machine/(?P<pk>\d+)/interfaces/delete/$', views.VirtualInterfaceBulkDeleteView.as_view(), name='virtual_interface_bulk_delete'),


    url(r'^devices/(?P<pk>\d+)/ip-addresses/assign/$', views.ipaddress_assign, name='ipaddress_assign'),

]
