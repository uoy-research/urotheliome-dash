CREATE TABLE NHU (
    nhu_differentiation TEXT PRIMARY KEY
);


CREATE TABLE Subset (
    subset_name TEXT PRIMARY KEY,
    nhu_differentiation TEXT NOT NULL,
    FOREIGN KEY (nhu_differentiation) REFERENCES NHU(nhu_differentiation)
);


CREATE TABLE Dataset (
    dataset_name TEXT PRIMARY KEY
);


CREATE TABLE Tissue (
    tissue_name TEXT PRIMARY KEY
);


CREATE TABLE Substrate (
    substrate_type TEXT PRIMARY KEY
);


CREATE TABLE Gender (
    gender TEXT PRIMARY KEY CHECK (LENGTH(gender) = 1)
);


CREATE TABLE Tumor_Stage (
    stage TEXT PRIMARY KEY
);


CREATE TABLE Vital_Status (
    status TEXT PRIMARY KEY
);


CREATE TABLE Samples (
    sample_id TEXT PRIMARY KEY,
    subset_name TEXT,
    dataset_name TEXT,
    tissue_name TEXT,
    substrate_type TEXT,
    TER FLOAT,
    gender TEXT,
    tumor_stage TEXT,
    vital_status TEXT,
    days_to_death INT,
    FOREIGN KEY (subset_name) REFERENCES Subset(subset_name),
    FOREIGN KEY (dataset_name) REFERENCES Dataset(dataset_name),
    FOREIGN KEY (tissue_name) REFERENCES Tissue(tissue_name),
    FOREIGN KEY (substrate_type) REFERENCES Substrate(substrate_type),
    FOREIGN KEY (gender) REFERENCES Gender(gender),
    FOREIGN KEY (tumor_stage) REFERENCES Tumor_Stage(stage),
    FOREIGN KEY (vital_status) REFERENCES Vital_Status(status)
);


CREATE TABLE Genes (
    gene_name TEXT PRIMARY KEY
);


CREATE TABLE Gene_Expression (
    sample_id TEXT,
    gene_name TEXT,
    TPM FLOAT NOT NULL,
    PRIMARY KEY (sample_id, gene_name),
    FOREIGN KEY (sample_id) REFERENCES Samples(sample_id),
    FOREIGN KEY (gene_name) REFERENCES Genes(gene_name)
);