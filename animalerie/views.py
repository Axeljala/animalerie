from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement, Animal

# Create your views here.
def list_accueil(request):
    equipements = Equipement.objects.order_by("id_equip")
    animals = Animal.objects.order_by("id_animal")
    return render(
        request,
        "animalerie/accueil.html",
        {"equipements": equipements, "animals": animals},
    )


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    lieu = Animal.lieu
    message = ""
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        # print(animal.lieu)
        if form.is_valid():
            # print(animal.lieu)
            # print(ancien_lieu)
            form.save(commit=False)
            if animal.lieu.disponibilite == "libre":
                ancien_lieu.disponibilite = "libre"
                # print(animal.lieu)
                nouveau_lieu = get_object_or_404(
                    Equipement, id_equip=animal.lieu.id_equip
                )
                # print(nouveau_lieu)
                if not nouveau_lieu.id_equip == "Litière":
                    nouveau_lieu.disponibilite = "occupé"
                if ancien_lieu.id_equip == "Nid" and nouveau_lieu.id_equip == "Litière":
                    animal.etat = "affamé"
                elif (
                    ancien_lieu.id_equip == "Litière"
                    and nouveau_lieu.id_equip == "Mangeoire"
                ):
                    animal.etat = "repus"
                elif (
                    ancien_lieu.id_equip == "Mangeoire"
                    and nouveau_lieu.id_equip == "Roue"
                ):
                    animal.etat = "fatigué"
                elif ancien_lieu.id_equip == "Roue" and nouveau_lieu.id_equip == "Nid":
                    animal.etat = "endormi"
                else:
                    form.clean()
                    message = "Mouvement non autorisé"
                    print("Mouvement interdit")
                    return render(request,"animalerie/animal_detail.html",{"animal": animal, "lieu": lieu, "form": form, "message": message})
                ancien_lieu.save()
                nouveau_lieu.save()
                animal.save()
                return redirect("animal_detail", pk=pk)
            else:
                form.clean()
                message = "Equipement déjà occupé"
                print("Equipement occupe")
                return render(request,"animalerie/animal_detail.html",{"animal": animal, "lieu": lieu, "form": form, "message": message})
        else:
            form = MoveForm()
    else:
        form = MoveForm()
    return render(
        request,
        "animalerie/animal_detail.html",
        {"animal": animal, "lieu": lieu, "form": form, "message": message},
    )


def equipment_detail(request, pk):
    equi = get_object_or_404(Equipement, pk=pk)
    return render(request, "animalerie/equipment_detail.html", {"equipment": equi})
