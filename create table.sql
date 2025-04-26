-- Not one single line, just a list of various commands that I ran to get the table working
-- Mostly here so its easy to reference schema

CREATE TABLE rxnconso (
   RXCUI             VARCHAR(8) NOT NULL,
   LAT               VARCHAR (3) DEFAULT 'ENG' NOT NULL,
   TS                VARCHAR (1),
   LUI               VARCHAR(8),
   STT               VARCHAR (3),
   SUI               VARCHAR (8),
   ISPREF            VARCHAR (1),
   RXAUI             VARCHAR (20) NOT NULL, 
   SAUI              VARCHAR (50),
   SCUI              VARCHAR (50),
   SDUI              VARCHAR (50),
   SAB               VARCHAR (20) NOT NULL,
   TTY               VARCHAR (20) NOT NULL,
   CODE              VARCHAR (50) NOT NULL,
   STR               VARCHAR (3000) NOT NULL,
   SRL               VARCHAR (10),
   SUPPRESS          VARCHAR (1),
   CVF               VARCHAR(50),
   PRIMARY KEY(RXAUI, RXCUI)
)

CREATE TABLE Interactions (
    RXCUI1 VARCHAR(8),
    drug_1_concept_name VARCHAR(150),
    RXCUI2 VARCHAR(8),
    drug_2_concept_name VARCHAR(150),
    condition_meddra_id VARCHAR(8),
    condition_concept_name VARCHAR(100),
    A VARCHAR(15),
    B VARCHAR(15),
    C VARCHAR(15),
    D VARCHAR(15),
    PRR VARCHAR(15),
    PRR_error VARCHAR(15),
    mean_reporting_frequency FLOAT,
    PRIMARY KEY(RXCUI1, RXCUI2, condition_meddra_id)
);

CREATE TABLE rxnrel (
    RXCUI1 VARCHAR(10) NOT NULL,
    RXAUI1 VARCHAR(10) NOT NULL,
    STYPE1 VARCHAR(50),
    REL VARCHAR(4),
    RXCUI2 VARCHAR(10) NOT NULL,
    RXAUI2 VARCHAR(10) NOT NULL,
    STYPE2 VARCHAR(50),
    RELA VARCHAR(100),
    RUI VARCHAR(10),
    SRUI VARCHAR(50),
    SAB VARCHAR(20) NOT NULL,
    SL VARCHAR(1000),
    DIR VARCHAR(3),
    RG VARCHAR(10),
    SUPPRESS VARCHAR(1),
    CVF VARCHAR(50),
    PRIMARY KEY(RUI),
    FOREIGN KEY (RXCUI1) REFERENCES rxnconso(RXCUI),
    FOREIGN KEY (RXAUI1) REFERENCES rxnconso(RXAUI)
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100),
    password_hash VARCHAR(100)
);

CREATE TABLE Results (
    dt_generated DATETIME,
    result_name VARCHAR(50),
    result_id INT,
    PRIMARY KEY (result_id)
);

CREATE TABLE Junction (
    RXCUI1 VARCHAR(10) NOT NULL,
    RXCUI2 VARCHAR(10) NOT NULL,
    result_id INT NOT NULL,
    condition_meddra_id VARCHAR(8) NOT NULL,
    PRIMARY KEY (RXCUI1, RXCUI2, result_id),
    FOREIGN KEY (RXCUI1, RXCUI2, condition_meddra_id) REFERENCES Interactions(RXCUI1, RXCUI2, condition_meddra_id),
    FOREIGN KEY (result_id) REFERENCES Results(result_id) ON DELETE CASCADE
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/TWOSIDES_appended.csv'
INTO TABLE Interactions
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
();