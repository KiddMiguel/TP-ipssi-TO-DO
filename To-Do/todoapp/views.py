from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Task
# Create your views here.
def today_str():
    return datetime.now().strftime("%d/%m/%Y")

# La page d'accueil avec filtre de la date du jour
def home(request):
    context = {
        "today": today_str(),
    }
    return render(request, "home.html", context)

def about(request):
    context = {
        "today": today_str(),
    }
    return render(request, "about.html", context)

# Liste des tâches crée du plus petit au plus recent
def liste(request):
    tasks = Task.objects.all().order_by("-created_at")
    total = tasks.count()
    done = tasks.filter(completed=True).count()
    todo = total - done
    context = {
        "today": today_str(),
        "tasks": tasks,
        "total": total,
        "done": done,
        "todo": todo,
    }
    return render(request, "liste.html", context)

# Liste des tâches encours qui sont pas encore complété
def liste_active(request):
    tasks = Task.objects.filter(completed=False).order_by("-created_at")
    context = {
        "today": today_str(),
        "tasks": tasks,
        "count": tasks.count(),
    }
    return render(request, "liste_active.html", context)


def detail(request, id):
    task = get_object_or_404(Task, pk=id)
    context = {
        "today": today_str(),
        "task": task,
    }
    return render(request, "detail.html", context)