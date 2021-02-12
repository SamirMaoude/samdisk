from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from . import models

from django.template import loader

from .models import *

from .forms import *

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db import IntegrityError

from django.views import generic

from django.urls import reverse


# Create your views here.


class IndexView(generic.ListView):

    template_name = 'store/index.html'

    context_object_name = 'context'

    def get_queryset(self):

        album_list = Album.objects.filter(available=1).order_by('-created_at')[:12]

        paginator = Paginator(album_list,3)

        page = self.request.GET.get('page')

        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            albums =paginator.page(1)
        except EmptyPage:
            albums=paginator.page(paginator.num_pages)

        return {'albums':albums,'paginate':True}

class ListView(generic.ListView):

    template_name = 'store/listing.html'
    context_object_name = 'context'

    def get_queryset(self):

        page =self.request.GET.get('page')
        album_list = Album.objects.filter(available=True).order_by('-created_at')

        paginator = Paginator(album_list,3)

        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            albums = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            albums = paginator.page(paginator.num_pages)

        return {'albums':albums, 'paginate':True}

    #return render(request, 'store/listing.html', {'albums':albums, 'paginate':True})

def detail(request, id):
    album = get_object_or_404(Album, pk=id)
    context = {
        'album_id':album.id,
        'album_title': album.title,
        'artists_name': ' '.join([artist.name for artist in album.artists.all()]),
        'album_id': album.id,
        'thumbnail': album.picture,

        'form': ContactForm()
    }

    if request.method == "POST":
        form = ContactForm(request.POST)
        try:
            if form.is_valid():
                email = request.POST.get("email")
                name = request.POST.get("name")
                album_id = id

                try:
                    contact = Contact.objects.get(email = email)

                except:
                    contact = Contact(name=name.upper(), email=email)

                    contact.save()

                album = get_object_or_404(Album, pk=album_id)
                
                if not album.available:

                    message = "Merci pour l'intérêt mais {} est indisponible".format(album.title)
                else:
                    Booking.objects.create(contact=contact,album=album)

                    #album.available = False

                    album.save()

                    message = "Merci. Vous avez réservé {} avec succès".format(album.title)

                return render(request, 'store/merci.html',{'message':message})

            else:

                context['errors'] = form.errors.items()
                context['form']=form
        except IntegrityError:

            context['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."



    
    
    return render(request, 'store/detail.html', context)

    


def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requête %s"%query   

    context ={
        'context':
        {
            'albums' : albums,
            'title' : title
        }
    }

    return render(request, 'store/search.html', context)
