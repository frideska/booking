from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from booking.filters import AdminFilter, UserFilter
from .models import Booking, Location
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from groups.models import SportsGroup
from groups.models import Membership


@login_required
def index(request):
    model = Location
    locations = model.objects.all()
    return render(request, 'booking/booking.html', {
        'locations': locations})

def api(request, **kwargs):
    model = Booking
    bookings = model.objects.all().values('title', 'description', 'start', 'end', 'location__name', 'person__first_name')
    booking_list = list(bookings)
    return JsonResponse(booking_list, safe=False)

class BookingList(ListView):
    model = Booking

    def all(request):
        locations = []
        bookings = []
        for location in list(Location.objects.filter()):
            locations.append(location.name)
        for booking in list(Booking.objects.filter()):
            bookings.append(booking)
        return render(request, 'booking/booking_list.html', {
            'locations': locations,
            'bookings': bookings, })

@login_required
def booking_all(request):
        book = []
        for booking in list(Booking.objects.filter()):
            book.append(booking)
        bookings = Booking.objects.all()
        booking_filter = AdminFilter(request.GET, queryset=bookings)
        return render(request, 'booking/booking_all.html', {
            'filter': booking_filter,
            'bookings': book})

def get_my_groups(request):
    user = request.user
    thelist = Membership.objects.filter(person=user).values_list('group', flat=True)
    my_groups = []
    for x in thelist:
        thelist3 = SportsGroup.objects.get(id=x).name
        my_groups.append(thelist3)
    return my_groups

def booking_list(request):
    model = Booking
    bookings = model.objects.all()
    user = request.user
    my_bookings_list = Booking.objects.filter(person=user)
    my_groups = get_my_groups(request)
    my_group_bookings_list = []
    for group in my_groups:
        booking = Booking.objects.filter(group=group).exclude(person=user)
        my_group_bookings_list.append(booking)

    print(my_group_bookings_list)

    return render(request, 'booking/bookings_list.html', {
        'my_bookings_list': my_bookings_list,
        'my_group_bookings_list': booking,
        'bookings': bookings})

def confirmation_mail(request):
    name = request.user.first_name
    body = 'Hey ' + name + ', you have created a new booking!'
    print(body)

def save_booking_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bookings = Booking.objects.all()
            data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
                'bookings': bookings
            })
            confirmation_mail(request)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def booking_create(request):
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST)
    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create.html')

def booking_create_from_calendar(request):
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST)
    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create_calendar.html')


def booking_update(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST, instance=book)
    else:
        user = request.user
        form = BookingForm(user, instance=book)
    return save_booking_form(request, form, 'booking/includes/partial_booking_update.html')

def booking_delete(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        bookings = Booking.objects.all()
        data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
            'bookings': bookings
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('booking/includes/partial_booking_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)
