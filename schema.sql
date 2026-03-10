-- ════════════════════════════════════════════════════════
-- SCHÉMA COMPLET POUR POINTAGEPRO V2
-- À exécuter dans le "SQL Editor" de Supabase
-- ════════════════════════════════════════════════════════

-- 1. Départements
CREATE TABLE IF NOT EXISTS departements (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(100) NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Employés
CREATE TABLE IF NOT EXISTS employes (
    id              SERIAL PRIMARY KEY,
    matricule       VARCHAR(20) NOT NULL UNIQUE,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100) NOT NULL,
    email           VARCHAR(254) NOT NULL UNIQUE,
    telephone       VARCHAR(20) DEFAULT '',
    poste           VARCHAR(100) NOT NULL,
    departement_id  INTEGER REFERENCES departements(id) ON DELETE SET NULL,
    date_embauche   DATE NOT NULL,
    statut          VARCHAR(20) DEFAULT 'actif' CHECK (statut IN ('actif', 'inactif', 'conge')),
    heures_contrat  NUMERIC(4,1) DEFAULT 8.0,
    photo_url       VARCHAR(500) DEFAULT '',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Pointages
CREATE TABLE IF NOT EXISTS pointages (
    id                  SERIAL PRIMARY KEY,
    employe_id          INTEGER NOT NULL REFERENCES employes(id) ON DELETE CASCADE,
    type_pointage       VARCHAR(10) NOT NULL CHECK (type_pointage IN ('entree', 'sortie')),
    horodatage          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    motif               VARCHAR(20) DEFAULT 'normal' CHECK (motif IN ('normal', 'mission', 'heures_sup', 'rattrapage')),
    note                TEXT DEFAULT '',
    latitude_pointage   NUMERIC(9,6),
    longitude_pointage  NUMERIC(9,6),
    distance_bureau     INTEGER,
    dans_zone           BOOLEAN DEFAULT TRUE,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Séances de travail (Calcul auto durées)
CREATE TABLE IF NOT EXISTS seances_travail (
    id                  SERIAL PRIMARY KEY,
    employe_id          INTEGER NOT NULL REFERENCES employes(id) ON DELETE CASCADE,
    pointage_entree_id  INTEGER NOT NULL REFERENCES pointages(id) ON DELETE CASCADE,
    pointage_sortie_id  INTEGER REFERENCES pointages(id) ON DELETE SET NULL,
    date                DATE NOT NULL,
    heure_entree        TIME NOT NULL,
    heure_sortie        TIME,
    duree_minutes       INTEGER,
    est_complete        BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Données initiales (Départements spécifiques)
INSERT INTO departements (nom, description) VALUES 
('Direction Générale', 'Direction et pilotage stratégique'),
('Ressources Humaines', 'Gestion du personnel et paie'),
('Service Plus', 'Service client premium'),
('Service Réabo', 'Réabonnements et fidélisation'),
('Comptabilité', 'Gestion financière'),
('Phoning', 'Centre d''appels et prospection'),
('Activatrices', 'Équipe d''activation terrain')
ON CONFLICT (nom) DO NOTHING;

-- Employé de test (lié à la Direction Générale)
INSERT INTO employes (matricule, nom, prenom, email, poste, departement_id, date_embauche) VALUES
('ADMIN01', 'Admin', 'Pointage', 'admin@entreprise.ci', 'Superviseur', 
 (SELECT id FROM departements WHERE nom = 'Direction Générale'), 
 CURRENT_DATE)
ON CONFLICT (matricule) DO NOTHING;
