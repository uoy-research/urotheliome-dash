CREATE TABLE NHU (
    NhuDifferentiation TEXT PRIMARY KEY
);

CREATE TABLE DatasetSubset (
    SubsetName TEXT PRIMARY KEY
);

CREATE TABLE Dataset (
    DatasetName TEXT PRIMARY KEY
);

CREATE TABLE Tissue (
    TissueName TEXT PRIMARY KEY
);

CREATE TABLE Substrate (
    SubstrateType TEXT PRIMARY KEY
);

CREATE TABLE Gender (
    Gender TEXT PRIMARY KEY
);

CREATE TABLE TumorStage (
    Stage TEXT PRIMARY KEY
);

CREATE TABLE VitalStatus (
    Status TEXT PRIMARY KEY
);

CREATE TABLE Sample (
    SampleId TEXT PRIMARY KEY,
    SubsetName TEXT,
    DatasetName TEXT,
    TissueName TEXT,
    SubstrateType TEXT,
    Gender TEXT,
    Stage TEXT,
    Status TEXT,
    NhuDifferentiation TEXT,
    TER REAL,
    DaysToDeath INT,
    FOREIGN KEY (SubsetName) REFERENCES DatasetSubset(SubsetName),
    FOREIGN KEY (DatasetName) REFERENCES Dataset(DatasetName),
    FOREIGN KEY (TissueName) REFERENCES Tissue(TissueName),
    FOREIGN KEY (SubstrateType) REFERENCES Substrate(SubstrateType),
    FOREIGN KEY (Gender) REFERENCES Gender(Gender),
    FOREIGN KEY (Stage) REFERENCES TumorStage(Stage),
    FOREIGN KEY (Status) REFERENCES VitalStatus(Status),
    FOREIGN KEY (NhuDifferentiation) REFERENCES NHU(NhuDifferentiation)
);

CREATE TABLE Gene (
    GeneName TEXT PRIMARY KEY
);

CREATE TABLE GeneExpression (   
    SampleId TEXT,
    GeneName TEXT,
    TPM REAL NOT NULL,
    PRIMARY KEY (SampleId, GeneName),
    FOREIGN KEY (SampleId) REFERENCES Sample(SampleId),
    FOREIGN KEY (GeneName) REFERENCES Gene(GeneName)
);
