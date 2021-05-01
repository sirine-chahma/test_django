from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking

# Index page
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    # test that index page returns a 200


# Detail Page
class DetailPageTestCase(TestCase):

    def setUp(self):
        impossible = Album.objects.create(title='impossible')
        self.album = Album.objects.get(title="impossible")
    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id, )))
        self.assertEqual(response.status_code, 200)
    # test that detail page returns a 404 if the items does not exist
    def test_detail_page_returns_404(self):
        album_id = self.album.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id, )))
        self.assertEqual(response.status_code, 404)


# Booking Page
class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name="Freddie", email="fred@queens.fr")
        impossible = Album.objects.create(title='impossible')
        journey = Artist.objects.create(name="Journey")
        impossible.artists.add(journey)
        self.album = Album.objects.get(title="impossible")
        self.contact = Contact.objects.get(name="Freddie")
    # test that a new booking is made
    def test_new_booking_is_registered(self):
        old_bookings = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {'name': name, 'email': email})
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings, old_bookings + 1)
    # test that a booking belongs to a contact
    # test that a booking belongs to an album
    # test that an album is not available after a booking is made
