from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Livre, Emprunt
from .forms import LivreForm

def liste_livres(request):
    tous_les_livres = Livre.objects.all().order_by('titre') # Trié par titre
    paginator = Paginator(tous_les_livres, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    nb_emprunts_en_cours = Emprunt.objects.filter(dateRetour__isnull=True).count()
    total_livres = Livre.objects.count()
    disponibles = total_livres - nb_emprunts_en_cours


    top_auteur_data = Livre.objects.values('auteur').annotate(total=Count('id')).order_by('-total').first()

    context = {
        'page_obj': page_obj,
        'livres_disponibles': disponibles,
        'top_auteur': top_auteur_data,
    }
    return render(request, 'livres/liste.html', context)


def ajouter_livre(request):
    if request.method == "POST":
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm()
    return render(request, 'livres/formulaire.html', {'form': form, 'titre': 'Ajouter un Livre'})


def modifier_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == "POST":
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'livres/formulaire.html', {'form': form, 'titre': 'Modifier le Livre'})


def supprimer_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == "POST":
        livre.delete()
        return redirect('liste_livres')
    return render(request, 'livres/supprimer_confirm.html', {'livre': livre})