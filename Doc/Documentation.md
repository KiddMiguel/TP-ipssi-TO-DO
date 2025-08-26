## 1) Préparation & commandes

```bash
# 1. Créer et activer l’environnement virtuel
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

# 2. Installer Django
pip install django

# 3. Créer le projet
django-admin startproject mysite .

# 4. Créer l’application
python manage.py startapp todoapp

# 5. Appliquer les migrations initiales
python manage.py migrate

# 6. Créer un superutilisateur (pour l’admin)
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

Arborescence attendue (résumé) :
```
.
├─ manage.py
├─ mysite/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
└─ todoapp/
   ├─ admin.py
   ├─ apps.py
   ├─ models.py
   ├─ views.py
   ├─ urls.py
   ├─ templates/
   │  ├─ base.html
   │  ├─ home.html
   │  ├─ about.html
   │  ├─ liste.html
   │  ├─ liste_active.html
   │  └─ detail.html
   └─ migrations/
```

---

## 2) Configuration du projet

### `mysite/settings.py`
Ajoute **`todoapp`** dans `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todoapp',
]
```

*(Optionnel mais conseillé)* : pour avoir la bonne heure locale en France/Congo, précise le fuseau si besoin :
```python
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'  # ou 'Africa/Brazzaville' selon ton cas
USE_I18N = True
USE_TZ = True
```

---

## 3) Modèle (To‑Do)

### `todoapp/models.py`
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Applique les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 4) Admin (facultatif mais conseillé)

### `todoapp/admin.py`
```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title",)
```

Ensuite, va sur `http://127.0.0.1:8000/admin/` et insère **8–12 tâches** pour tester.

---

## 5) Vues (avec date du jour en français)

> Exigence : **chaque vue** passe la date du jour (format **JJ/MM/AAAA**) au template.

### `todoapp/views.py`
```python
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Task

# Petit utilitaire pour formater la date du jour au format requis JJ/MM/AAAA
def today_str():
    return datetime.now().strftime("%d/%m/%Y")

# 1) Accueil: /
#    - Statique + date du jour

def home(request):
    context = {
        "today": today_str(),
    }
    return render(request, "home.html", context)

# 2) À propos: /about/
#    - Statique + date du jour

def about(request):
    context = {
        "today": today_str(),
    }
    return render(request, "about.html", context)

# 3) Liste: /liste/
#    - Toutes les tâches, triées du plus récent au plus ancien
#    - Compteurs: total, done, todo

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

# 4) Liste filtrée: /liste/filtre/
#    - Tâches actives (completed=False)

def liste_active(request):
    tasks = Task.objects.filter(completed=False).order_by("-created_at")
    context = {
        "today": today_str(),
        "tasks": tasks,
        "count": tasks.count(),
    }
    return render(request, "liste_active.html", context)

# 5) Détail: /detail/<id>/

def detail(request, id):
    task = get_object_or_404(Task, pk=id)
    context = {
        "today": today_str(),
        "task": task,
    }
    return render(request, "detail.html", context)
```

---

## 6) URLs

### `todoapp/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                 # /
    path("about/", views.about, name="about"),         # /about/
    path("liste/", views.liste, name="liste"),         # /liste/
    path("liste/filtre/", views.liste_active, name="liste_active"),  # /liste/filtre/
    path("detail/<int:id>/", views.detail, name="detail"),           # /detail/<id>/
]
```

### `mysite/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todoapp.urls")),  # Route tout vers l’app
]
```

---

## 7) Templates

> Place tous ces fichiers dans `todoapp/templates/`.

### `base.html`
```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}To‑Do{% endblock %}</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,"Helvetica Neue",Arial;max-width:860px;margin:40px auto;padding:0 16px;}
    header,footer{opacity:.8}
    nav a{margin-right:12px;text-decoration:none}
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;border:1px solid #ddd}
    .done{background:#eafbea}
    .todo{background:#fff7e6}
    .card{border:1px solid #eee;border-radius:12px;padding:16px;margin:12px 0}
    .muted{color:#666}
  </style>
</head>
<body>
  <header>
    <h1>Mini‑site To‑Do</h1>
    <nav>
      <a href="/">Accueil</a>
      <a href="/about/">À propos</a>
      <a href="/liste/">Liste</a>
      <a href="/liste/filtre/">Actives</a>
    </nav>
    <p class="muted">Aujourd’hui : {{ today }}</p>
    <hr>
  </header>

  {% block content %}{% endblock %}

  <footer>
    <hr>
    <p class="muted">TP Django — Sujet To‑Do</p>
  </footer>
</body>
</html>
```

### `home.html`
```html
{% extends "base.html" %}
{% block title %}Accueil — To‑Do{% endblock %}
{% block content %}
  <div class="card">
    <h2>Bienvenue 👋</h2>
    <p>Ce site démontre un mini CRUD en lecture (liste/détail) pour des tâches, avec filtrage simple.</p>
    <ul>
      <li>5 pages : Accueil, À propos, Liste, Liste filtrée, Détail</li>
      <li>Date du jour affichée sur chaque page</li>
      <li>Tri par date de création (plus récentes d’abord)</li>
    </ul>
  </div>
{% endblock %}
```

### `about.html`
```html
{% extends "base.html" %}
{% block title %}À propos — To‑Do{% endblock %}
{% block content %}
  <div class="card">
    <h2>À propos</h2>
    <p>Exemple pédagogique Django : architecture MVT, ORM, vues et templates.</p>
  </div>
{% endblock %}
```

### `liste.html`
```html
{% extends "base.html" %}
{% block title %}Liste des tâches — To‑Do{% endblock %}
{% block content %}
  <h2>Toutes les tâches</h2>
  <p class="muted">Total: {{ total }} • Terminées: {{ done }} • À faire: {{ todo }}</p>

  {% if tasks %}
    <ul>
      {% for t in tasks %}
        <li class="card">
          <strong>{{ t.title }}</strong>
          {% if t.completed %}
            <span class="pill done">✔ Terminée</span>
          {% else %}
            <span class="pill todo">✗ À faire</span>
          {% endif %}
          <div class="muted">Créée le {{ t.created_at|date:"d/m/Y H:i" }}</div>
          <div><a href="/detail/{{ t.id }}/">Voir le détail</a></div>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>Aucune tâche.</p>
  {% endif %}
{% endblock %}
```

### `liste_active.html`
```html
{% extends "base.html" %}
{% block title %}Tâches actives — To‑Do{% endblock %}
{% block content %}
  <h2>Tâches actives (non terminées)</h2>
  <p class="muted">Nombre: {{ count }}</p>

  {% if tasks %}
    <ul>
      {% for t in tasks %}
        <li class="card">
          <strong>{{ t.title }}</strong>
          <span class="pill todo">✗ À faire</span>
          <div class="muted">Créée le {{ t.created_at|date:"d/m/Y H:i" }}</div>
          <div><a href="/detail/{{ t.id }}/">Voir le détail</a></div>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    <p>Aucune tâche active.</p>
  {% endif %}
{% endblock %}
```

### `detail.html`
```html
{% extends "base.html" %}
{% block title %}Détail — To‑Do{% endblock %}
{% block content %}
  <h2>Détail de la tâche</h2>
  <div class="card">
    <p><strong>Titre :</strong> {{ task.title }}</p>
    <p><strong>Statut :</strong>
      {% if task.completed %}
        ✔ Terminée
      {% else %}
        ✗ À faire
      {% endif %}
    </p>
    <p class="muted">Créée le {{ task.created_at|date:"d/m/Y H:i" }}</p>
  </div>
  <p><a href="/liste/">← Retour à la liste</a></p>
{% endblock %}
```

---

## 8) Tests manuels rapides

1. **Données** : via l’admin, crée 8–12 tâches (mélange terminées / non terminées).
2. **Pages** :
   - `http://127.0.0.1:8000/` → Accueil (date visible)
   - `http://127.0.0.1:8000/about/` → À propos (date visible)
   - `http://127.0.0.1:8000/liste/` → Liste triée + compteurs
   - `http://127.0.0.1:8000/liste/filtre/` → Tâches actives
   - `http://127.0.0.1:8000/detail/1/` → Détail (remplacer 1 par un id existant)

---

## 9) Mini README (à déposer avec le projet)

Crée un fichier `README.md` à la racine :

```md
# Mini‑site Django — To‑Do

## Prérequis
- Python 3.10+
- pip

## Installation
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Pages
- `/` → Accueil (avec date)
- `/about/` → À propos (avec date)
- `/liste/` → Liste triée (avec compteurs + date)
- `/liste/filtre/` → Liste filtrée (tâches actives + date)
- `/detail/<id>/` → Détail (avec date)

## Modèle
- `Task(title: CharField(200), completed: BooleanField(default=False), created_at: DateTimeField(auto_now_add=True))`
```

---