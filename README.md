# MsPlaco – Site Web Expert BA13 & Cloisons Sèches

Site professionnel bilingue (FR/AR) pour artisan plaquiste, avec **Flask backend** + **Netlify static hosting**.

---
 
## 📁 Structure du projet

```
MsPlaco/
├── public/                     ← Site statique déployé sur Netlify
│   ├── index.html              ← Page d'accueil (Français)
│   ├── ar.html                 ← Page d'accueil (Arabe RTL)
│   └── images/                 ← 22 photos de chantier (project-01..22.jpeg)
├── src/
│   ├── app.py                  ← Application Flask (backend)
│   ├── templates/
│   │   ├── index.html          ← Template Flask (Français)
│   │   ├── index_ar.html       ← Template Flask (Arabe RTL)
│   │   ├── admin.html          ← Tableau de bord admin
│   │   └── admin_login.html    ← Page de connexion admin
│   ├── static/images/          ← Photos source des chantiers
│   └── data/quotes.json        ← Stockage des devis (auto-généré)
├── .env                        ← Variables d'environnement (ne pas commiter)
├── netlify.toml                ← Configuration Netlify (publish = "public")
├── package.json                ← Dépendances Node (Tailwind CSS)
└── README.md
```

---

## ✨ Fonctionnalités

- **Bilingue** : Français + Arabe (RTL) avec basculement de langue
- **Galerie** : 22 photos de projets avec lightbox plein écran
- **Formulaire de contact** : Validation, stockage JSON, envoi d'emails
- **Notification WhatsApp** : Alerte instantanée via CallMeBot à chaque nouveau devis
- **Panneau Admin** : Tableau de bord protégé par mot de passe pour gérer les devis (nouveau / en cours / terminé / archivé)
- **Responsive** : Menu hamburger, grilles adaptatives, optimisé mobile (768px + 480px)
- **Animations** : GSAP + ScrollTrigger, curseur personnalisé, compteurs animés

---

## 🚀 Installation & Lancement

### Backend Flask (src/)

```bash
# 1. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Installer les dépendances
pip install flask flask-mail python-dotenv requests

# 3. Configurer les variables d'environnement
cp .env.example .env
# Remplir : MAIL_USERNAME, MAIL_PASSWORD, OWNER_EMAIL, ADMIN_PASSWORD,
#           CALLMEBOT_PHONE, CALLMEBOT_APIKEY

# 4. Lancer le serveur
cd src
python app.py
```
→ Ouvrir http://localhost:5000

### Site statique Netlify (public/)

Le dossier `public/` est déployé automatiquement sur Netlify.
Il contient les fichiers HTML statiques avec formulaires Netlify intégrés.

---

## 📧 Configuration Email (Gmail)

1. Activez l'**authentification à 2 facteurs** sur le compte Gmail
2. **Compte Google → Sécurité → Mots de passe des applications**
3. Créez un mot de passe pour "Autre application" → nommez-le "MsPlaco"
4. Copiez le mot de passe à 16 caractères dans `.env` → `MAIL_PASSWORD`

---

## 📱 Configuration WhatsApp (CallMeBot)

1. Envoyez un message WhatsApp à **+34 644 31 89 93** avec le texte :
   `I allow callmebot to send me messages`
2. Vous recevrez votre **API key** en réponse
3. Mettez à jour `.env` :
   ```
   CALLMEBOT_PHONE=+212659715906
   CALLMEBOT_APIKEY=votre_cle_api
   ```

---

## ⚙️ Variables d'environnement (.env)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
OWNER_EMAIL=email-destination@gmail.com
SECRET_KEY=votre-cle-secrete
ADMIN_PASSWORD=votre-mot-de-passe-admin
CALLMEBOT_PHONE=+212XXXXXXXXX
CALLMEBOT_APIKEY=votre_cle_api
```

---

## 🌐 Déploiement

### Netlify (site statique – recommandé)
1. Connectez le dépôt GitHub sur [netlify.com](https://netlify.com)
2. Publish directory : `public`
3. Les formulaires Netlify sont déjà configurés (`data-netlify="true"`)

### Render.com (backend Flask)
1. "New Web Service" → connectez votre dépôt
2. Root directory : `src`
3. Build command : `pip install flask flask-mail python-dotenv requests`
4. Start command : `gunicorn app:app`
5. Ajoutez les variables d'environnement

---

## 🔗 Routes API (Backend Flask)

| Route | Méthode | Description |
|---|---|---|
| `/` | GET | Page d'accueil (FR ou AR selon session) |
| `/set-lang/<lang>` | GET | Changer la langue (fr/ar) |
| `/send-contact` | POST | Soumettre un devis → email + WhatsApp |
| `/admin/login` | GET/POST | Connexion admin |
| `/admin` | GET | Tableau de bord admin |
| `/api/quotes` | GET | Liste des devis (JSON) |
| `/api/quotes/<id>/status` | PATCH | Modifier le statut d'un devis |
| `/api/quotes/<id>` | DELETE | Supprimer un devis |

---

## ✏️ Personnalisation rapide

| Élément | Fichiers |
|---|---|
| Numéro de téléphone | `public/index.html`, `public/ar.html`, templates |
| Email affiché | Section Contact dans chaque fichier HTML |
| Nom de l'entreprise | Navbar + Footer |
| Zone d'intervention | Section Contact |
| Stats (150 projets, 8 ans...) | Attributs `data-count` |
| Photos galerie | `public/images/` + `src/static/images/` |

---

## 📦 Technologies

- **Flask** – Serveur web Python
- **Flask-Mail** – Envoi d'emails SMTP
- **CallMeBot** – Notifications WhatsApp gratuites
- **Netlify** – Hébergement statique + formulaires
- **Tailwind CSS** – Styles (CDN)
- **GSAP + ScrollTrigger** – Animations scroll
- **Jinja2** – Templates dynamiques (côté Flask)
- **python-dotenv** – Variables d'environnement sécurisées