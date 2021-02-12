from django.contrib import admin

from .models import Album,Artist,Contact,Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter=['created_at','contacted']
    readonly_fields = ["created_at", "contact", 'album', 'contacted']

    def has_add_permission(self,request):
        return False

class BookingInline(admin.TabularInline):

    model = Booking

    fieldsets =[(None,{'fields':['album','contacted','created_at']})]

    readonly_fields = ['album','contacted','created_at']
    extra=0
    """
    def Booking.has_add_permission(self,request):
        return False
    """


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    inlines = [BookingInline]


class AlbumArtistInline(admin.TabularInline):
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

    model = Album.artists.through # the query goes through an intermediate table.
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline,]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title','reference']
    




# Register your models here.
