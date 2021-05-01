from django.contrib import admin
from .models import Booking, Contact, Artist, Album

from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class AdminURLMixin(object):

    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%s_change" % (content_type.model), args=(obj.id,))


class BookingInLine(admin.TabularInline):
    readonly_fields = ["created_at", "contact", "album"]
    model = Booking
    fieldsets = [
        (None, {'fields': ['album', 'contacted']})
    ]
    extra = 0
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def has_add_permission(self, request, obj):
        return False


class AlbumArtistInLine(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInLine, ]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInLine, ]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ["created_at", "contact", "album_link"]
    list_filter = ['created_at', 'contacted']
    fieldsets = [
        (None, {'fields': ['created_at', 'album_link', 'contacted']})
    ]

    def has_add_permission(self, request):
        return False

    def album_link(self, booking):
        url = self.get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))
