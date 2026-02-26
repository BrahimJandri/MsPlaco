# PlacoPro – Site Web BA13

Site professionnel pour artisan plaquiste, construit avec **Flask + Jinja2 + Tailwind CSS + GSAP**.

---

## 📁 Structure du projet

```
placopro/
├── app.py                  ← Application Flask principale
├── requirements.txt        ← Dépendances Python
├── .env.example            ← Modèle de configuration (copier en .env)
├── .gitignore
├── templates/
│   └── index.html          ← Page d'accueil (HTML + Tailwind + GSAP)
└── static/
    ├── images/             ← Vos photos de chantier
    ├── css/                ← CSS personnalisé (optionnel)
    └── js/                 ← JS personnalisé (optionnel)
```

---

## 🚀 Installation & Lancement (5 étapes)

### 1. Cloner / télécharger le projet
```bash
cd votre-dossier
```

### 2. Créer un environnement virtuel Python
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Ouvrez .env et remplissez vos vraies valeurs :
#   MAIL_USERNAME=votre.email@gmail.com
#   MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  (mot de passe d'application Gmail)
#   OWNER_EMAIL=email-de-votre-frere@gmail.com
```

### 5. Lancer le serveur
```bash
python app.py
```
Ouvrez http://localhost:5000 dans votre navigateur.

---

## 📧 Configuration Gmail (pour les emails)

1. Activez l'**authentification à 2 facteurs** sur le compte Gmail de votre frère
2. Allez dans **Compte Google → Sécurité → Mots de passe des applications**
3. Créez un mot de passe pour "Autre application" → nommez-le "PlacoPro"
4. Copiez le mot de passe à 16 caractères dans `.env` → `MAIL_PASSWORD`

---

## 🌐 Déploiement en ligne (gratuit)

### Option A – Render.com (recommandé)
1. Créez un compte sur [render.com](https://render.com)
2. "New Web Service" → connectez votre dépôt GitHub
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Ajoutez vos variables d'environnement dans "Environment"

### Option B – PythonAnywhere (facile débutant)
1. Créez un compte sur [pythonanywhere.com](https://pythonanywhere.com)
2. Upload vos fichiers
3. Configurez un "Web app" Flask
4. Ajoutez vos variables d'environnement

---

## 🖼️ Ajouter vos vraies photos

1. Placez vos photos dans `static/images/`
2. Dans `index.html`, remplacez les blocs `.gallery-placeholder` par :
```html
<img src="{{ url_for('static', filename='images/votre-photo.jpg') }}" 
     alt="Chantier BA13" style="width:100%; height:100%; object-fit:cover;" />
```

---

## ✏️ Personnalisation rapide

| Ce qu'il faut changer | Où |
|---|---|
| Numéro de téléphone | `index.html` → section Contact |
| Email affiché | `index.html` → section Contact |
| Nom de l'entreprise | `index.html` → navbar + footer |
| Zone d'intervention | `index.html` → section Contact |
| Stats (150 projets, 8 ans...) | `index.html` → `data-count` attributes |

---

## 📦 Technologies utilisées

- **Flask** – Serveur web Python
- **Flask-Mail** – Envoi d'emails
- **Jinja2** – Templates HTML dynamiques
- **Tailwind CSS** – Styles via CDN
- **GSAP + ScrollTrigger** – Animations
- **python-dotenv** – Variables d'environnement sécurisées