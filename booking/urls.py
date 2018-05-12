from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='booking'),
    url(r'^api', views.api, name='api'),
    url(r'^location_api', views.location_api, name='api'),
    url(r'^profile', views.BookingList.as_view(), name='booking_list'),
    url(r'^bookings_manage/$', views.booking_manage, name="booking_manage_list"),
    url(r'^bookings_list/$', views.booking_list, name='booking_list'),
    url(r'^bookings_list/create/$', views.booking_create, name='booking_create'),
    url(r'^bookings_list/create_calendar/$', views.booking_create_from_calendar, name='booking_create_calendar'),
    url(r'^books/(?P<pk>\d+)/update/$', views.booking_update, name='booking_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.booking_delete, name='booking_delete'),
    url(r'^test_form$', views.show_form, name="show_form")
]
