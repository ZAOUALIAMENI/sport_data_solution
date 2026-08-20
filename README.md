# Sport Data Solution

## Tableau de bord — Avantages salariés

Projet de mise en place d'une architecture de données permettant de centraliser, automatiser et analyser les données liées à la pratique sportive des salariés, aux déplacements domicile-travail, aux dispositifs de bien-être et aux avantages financiers associés.

L'objectif est de remplacer les traitements manuels par une chaîne de données automatisée, testée et restituée dans un tableau de bord Power BI.

---

## Objectifs du projet

La solution permet de :

- centraliser les données RH et sportives ;
- générer et historiser les activités sportives ;
- calculer les déplacements domicile-travail associés ;
- appliquer les règles métier liées aux avantages salariés ;
- automatiser les traitements avec Kestra ;
- transformer et tester les données avec DBT ;
- produire un modèle analytique destiné à Power BI ;
- suivre les indicateurs sportifs, bien-être et financiers ;
- simuler l'impact budgétaire d'une augmentation du nombre de bénéficiaires.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   Données sources   │
                    │                     │
                    │ RH.xlsx             │
                    │ Sportive.xlsx       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Python        │
                    │                     │
                    │ Ingestion            │
                    │ Génération activités │
                    │ Génération trajets   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │                     │
                    │       RAW           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        DBT          │
                    │                     │
                    │ STAGING             │
                    │ INTERMEDIATE        │
                    │ MARTS               │
                    │ TESTS               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Kestra        │
                    │                     │
                    │ Orchestration       │
                    │ Automatisation      │
                    │ Notifications Slack │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Power BI       │
                    │                     │
                    │ KPI                 │
                    │ Analyses            │
                    │ Simulation financière│
                    └─────────────────────┘
```

## Technologies utilisées
- Python : Ingestion et génération des données 
- PostgreSQL : Stockage des données 
- DBT : Transformation, modélisation et tests 
- Kestra : Orchestration des traitements
- Docker : Conteneurisation de l'environnement
- Power BI : Visualisation et analyse 
- Slack : Notifications liées aux activités sportives 
- Git / GitHub : versionnement du projet

## Structure du projet

sport_data_solution/
│
├── database/
│   └── schema.sql
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   │
│   ├── tests/
│   │   └── business_rules/
│   │
│   └── dbt_project.yml
│
├── docker/
│   ├── Dockerfile.kestra
│   └── docker-compose.yml
│
├── kestra/
│   └── flows/
│       ├── main_sport_data_main_pipeline.yml
│       ├── main_sport_data_load_data.yml
│       ├── main_sport_data_generate_activities.yml
│       ├── main_sport_data_generate_commute.yml
│       ├── main_sport_data_dbt_pipeline.yml
│       └── main_sport_data_sport_slack_comment.yml
│
├── powerbi/
│   └── sport_data_dashboard.pbix
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── load_data.py
│   ├── generate_commute_distances.py
│   └── generate_activities.py
│
├── requirements.txt
├── .gitignore
└── README.md

## Règles métier principales

Les règles métier sont centralisées dans DBT afin de séparer la génération des données des calculs métier.

### Prime sportive
La prime sportive correspond à :
Prime sportive = 5 % du salaire brut
Elle est attribuée selon les conditions définies dans les modèles DBT.

### Jours de bien-être
Un salarié devient éligible lorsqu'il atteint :
Minimum : 15 activités sportives
Le dispositif prévoit :
5 journées de bien-être

### Déplacements
Des règles de cohérence sont appliquées aux déplacements :
Marche : distance maximale de 15 km
Vélo   : distance maximale de 25 km

Ces paramètres sont centralisés dans dbt_project.yml.

## Modèle analytique
Le modèle principal destiné à Power BI est :

mart_dashboard

Il regroupe notamment :

informations salariés ;
business unit ;
activités sportives ;
nombre d'activités ;
distance totale ;
durée totale ;
prime sportive ;
bénéficiaires ;
jours de bien-être ;
informations liées aux déplacements.

Ce modèle constitue la source principale du tableau de bord.

## Tableau de bord Power BI
Le fichier : powerbi/sport_data_dashboard.pbix

présente notamment :

### KPI
Nombre de salariés
Nombre de sportifs
Taux de salariés sportifs
Nombre total d'activités
Distance cumulée
Durée cumulée
Montant total des bonus sportifs
Nombre de bénéficiaires
Nombre de jours de bien-être

### Analyses
Bonus sportifs par Business Unit
Bénéficiaires bien-être par Business Unit
Répartition des activités par sport
Simulation de l'impact financier

### Simulation financière

La simulation permet d'estimer l'évolution du budget si le nombre de bénéficiaires augmente, en conservant le bonus moyen par bénéficiaire.

Exemple de scénarios :

Situation actuelle
+10 bénéficiaires
+20 bénéficiaires
+30 bénéficiaires

## Tests DBT
Des tests spécifiques aux règles métier sont présents dans : dbt/tests/business_rules/

Ils couvrent notamment :

test_commute_bike.sql
test_commute_walk_running.sql
test_sport_bonus.sql
test_sport_bonus_amount.sql
test_wellbeing_days.sql
test_wellbeing_eligibility.sql

L'objectif est de vérifier automatiquement la cohérence des calculs métier et de détecter les anomalies avant la restitution analytique.

## Installation
1. Cloner le projet
git clone https://github.com/ZAOUALIAmeni/sport_data_solution.git
cd sport_data_solution
2. Créer l'environnement Python
python -m venv .venv

Activation sous Windows :

.venv\Scripts\activate
3. Installer les dépendances
pip install -r requirements.txt
4. Configurer les variables d'environnement

Les informations sensibles ne sont pas versionnées.

Créer les fichiers .env nécessaires avec les paramètres de connexion PostgreSQL et les secrets utilisés par Kestra.

Les fichiers .env sont exclus du dépôt via .gitignore.

## Démarrage avec Docker

Depuis la racine du projet :

docker compose -f docker/docker-compose.yml up -d

Vérifier les conteneurs :

docker ps

Pour arrêter l'environnement :

docker compose -f docker/docker-compose.yml down

## Exécution des scripts Python

L'ingestion des données RH et sportives peut être exécutée avec :

python src/load_data.py

La génération des activités sportives :

python src/generate_activities.py

Les traitements sont ensuite orchestrés dans le pipeline Kestra.

## Orchestration Kestra

Les workflows sont disponibles dans :

kestra/flows/

Le pipeline principal permet d'enchaîner les différentes étapes :

Chargement des données
        ↓
Génération des activités
        ↓
Génération des déplacements
        ↓
Transformations DBT
        ↓
Tests métier
        ↓
Marts analytiques

Un workflow dédié permet également la génération de commentaires et de notifications Slack à partir des nouvelles activités sportives.

## DBT

Depuis le dossier DBT :

cd dbt

Installation des dépendances DBT si nécessaire :

dbt deps

Exécution des modèles :

dbt run

Exécution des tests :

dbt test

Exécution complète :

dbt build

## Gestion des secrets

Les informations sensibles ne sont pas stockées dans le dépôt.

Sont notamment exclus du versionnement :

.env
docker/.env

Les secrets utilisés par Kestra, notamment les identifiants PostgreSQL et le webhook Slack, sont récupérés via les mécanismes de secrets de Kestra.

## Résultat

La solution permet de passer d'un traitement manuel à une chaîne de données automatisée :

Données sources
      ↓
Ingestion
      ↓
Stockage PostgreSQL
      ↓
Transformations DBT
      ↓
Tests métier
      ↓
Marts analytiques
      ↓
Power BI

L'architecture permet ainsi de fiabiliser les calculs, automatiser les traitements et fournir une vision synthétique de la pratique sportive, des dispositifs de bien-être et de leur impact financier potentiel.