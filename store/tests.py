from django.test import TestCase, Client
from .models import *
from django.urls import reverse

def create_booking(album, contact):

    return Booking.objects.create(album=contact, contact=contact)


class AlbumModelTests(TestCase):

        
    def test_album_is_available(self):
        album = Album(title="Test Album")

        self.assertIs(album.available,True)

class DetailPageTests(TestCase):

    def setUp(self):

        new_album = Album.objects.create(title="New album")

        self.album =Album.objects.get(title="New album")



    def test_detail_page_returns_200(self):

        url = reverse('store:detail',args=(self.album.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code,200)

    def test_detail_page_returns_404(self):

        url = reverse('store:detail',args=(self.album.id+1,))

        response = self.client.get(url)

        self.assertEqual(response.status_code,404)


class BookingPageTests(TestCase):

    def setUp(self):

        Contact.objects.create(name="Mac Gayver", email="macgayver@gmail.com")

        self.contact = Contact.objects.get(email="macgayver@gmail.com")

        Artist.objects.create(name="Alan Walker")

        self.artist = Artist.objects.get(name="Alan Walker")

        Album.objects.create(title="Different World")

        self.album = Album.objects.get(title="Different World")

        self.artist.albums.add(self.album)

        self.album.artists.add(self.artist)

    def test_booking_is_registred(self):

        old_bookings = Booking.objects.count()

        self.client.post(reverse('store:detail',args=(self.album.id,)),

            {
                'name':self.contact.name,
                'email':self.contact.email,

            }
        
        )

        self.assertEqual(Booking.objects.count()-1,old_bookings)

    def test_booking_is_not_registred(self):

        old_bookings = Booking.objects.count()

        self.album.available = False

        self.album.save()

        self.client.post(reverse('store:detail',args=(self.album.id,)),

            {
                'name':self.contact.name,
                'email':self.contact.email,

            }
        
        )

        self.assertEqual(Booking.objects.count(),old_bookings)










# Create your tests here.
