-- ============================================
-- Création de la base
-- ============================================

CREATE DATABASE IF NOT EXISTS projet_dev_avance
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE projet_dev_avance;


-- ============================================
-- Nettoyage
-- ============================================

DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS motors;


-- ============================================
-- Table des moteurs
-- ============================================

CREATE TABLE motors (
    id INT AUTO_INCREMENT PRIMARY KEY,

    type VARCHAR(20) NOT NULL,
    power INT NOT NULL,

    -- Données thermiques
    consumption_thermic DECIMAL(6,2) NULL,
    capacity_thermic DECIMAL(6,2) NULL,

    -- Données électriques
    consumption_electric DECIMAL(6,2) NULL,
    capacity_electric DECIMAL(6,2) NULL
);


-- ============================================
-- Table des véhicules
-- ============================================

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,

    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT NOT NULL,

    motor_id INT NOT NULL,

    CONSTRAINT fk_vehicle_motor
        FOREIGN KEY (motor_id)
        REFERENCES motors(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- ============================================
-- Moteur thermique
-- ============================================

INSERT INTO motors (
    type,
    power,
    consumption_thermic,
    capacity_thermic
)
VALUES (
    'Thermic',
    130,
    6.5,
    50
);

SET @thermic_motor_id = LAST_INSERT_ID();


-- ============================================
-- Moteur électrique
-- ============================================

INSERT INTO motors (
    type,
    power,
    consumption_electric,
    capacity_electric
)
VALUES (
    'Electric',
    150,
    18.0,
    60
);

SET @electric_motor_id = LAST_INSERT_ID();


-- ============================================
-- Moteur hybride
-- ============================================

INSERT INTO motors (
    type,
    power,
    consumption_thermic,
    capacity_thermic,
    consumption_electric,
    capacity_electric
)
VALUES (
    'Hybrid',
    200,
    6.3,
    45,
    21.0,
    11
);

SET @hybrid_motor_id = LAST_INSERT_ID();


-- ============================================
-- Véhicules
-- ============================================

INSERT INTO vehicles (
    brand,
    model,
    year,
    motor_id
)
VALUES (
    'Peugeot',
    '308',
    2020,
    @thermic_motor_id
);

INSERT INTO vehicles (
    brand,
    model,
    year,
    motor_id
)
VALUES (
    'Tesla',
    'Model 3',
    2024,
    @electric_motor_id
);

INSERT INTO vehicles (
    brand,
    model,
    year,
    motor_id
)
VALUES (
    'Volvo',
    'XC40',
    2025,
    @hybrid_motor_id
);
