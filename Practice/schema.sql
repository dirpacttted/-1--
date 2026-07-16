CREATE TABLE IF NOT EXISTS Configurations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    synonym VARCHAR(255),
    default_download_path VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS ConfigurationVersions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    configuration_id INT NOT NULL,
    version VARCHAR(100) NOT NULL,
    FOREIGN KEY (configuration_id)
        REFERENCES Configurations(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MetadataObjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version_id INT NOT NULL,
    object_type VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    synonym VARCHAR(255),
    object_uuid CHAR(36),
    FOREIGN KEY (version_id)
        REFERENCES ConfigurationVersions(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DataSeparationSettings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metadata_object_id INT NOT NULL,
    auxiliary_data_area VARCHAR(255),
    main_data_area VARCHAR(255),
    FOREIGN KEY (metadata_object_id)
        REFERENCES MetadataObjects(id)
        ON DELETE CASCADE
);