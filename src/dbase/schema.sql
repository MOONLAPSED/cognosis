/* 
SCHEMA FOR cognosis by MOONLAPSED@github MIT LICENSE:

// Types_
- Entity_ - A data model defining the system, with relationships to other entities. It represents a definition or blueprint, not an instance of an object.
- Attribute_ - A specific data point that an entity defines itself as having. For example, the dog entity has attributes such as having four legs and being carnivorous, along with unique attributes for individual instances.
- Class_ - A data model defining a specific type of entity, with relationships to other entities.
- Type_ - A data model defining a specific type of attribute, with relationships to other attributes.

// Basic Attributes_
- TEXT - Represents a string of text
- INTEGER - Represents a whole number
- REAL - Represents a decimal number
- BLOB - Represents a binary large object or a file that is too big to fit in a single column
- VARCHAR(255) - Represents a restricted-length character

// Advanced Attributes_
- text_entries - Table containing information about text entries, including text entry name, file name, file path, file type, and text entry ID (primary key).
- embeddings - Table containing information about embeddings, including embedding ID, model ID, and vector (primary key).
- models - Table containing information about models, including model ID, model name, and model description.

// SpecObject_ Store and manage specific entity instances Represents entity attributes and values
- TextEntry (entity_id, attribute_id, text_content, timestamp, etc.)
- Embedding (entity_id, attribute_id, embedding_data, metadata, etc.)
- Model (entity_id, attribute_id, model_data, parameters, etc.)
- UnixFilesystem (entity_id, attribute_id, file_path, permissions, etc.)
    - - unix_filesystem - Table containing information about Unix File System (UFS) objects or states, capturing metadata and attributes related to Unix-like operating system file entities. This table stores details such as inode, PID (Process ID), systemd_host_file, and other relevant attributes associated with files or file-like entities within a Unix file system. The attributes recorded within this table provide crucial information for managing and understanding the properties and states of files or elements within the Unix file system, aiding in system monitoring, administration, or analysis.
    - - inode - Inode is a unique identifier for a file or directory within a Unix file system. Inode is a 64-
    - - PID - Process ID (PID) is a unique identifier for a process within a Unix file system. PID is a 32-bit
    etc.

// Bridge_ Associate entities with other data types or entities Connects entities to blobs, text files, vector representations, and UFS objects
EntityAttributes_blobs: Links entities to blobs.
EntityAttributes_text_files: Links entities to text files.
EntityAttributes_vector_representations: Links entities to vector representations.
EntityAttributes_UFS: Links entities to UFS objects.
*/

/* Tables for Entity Management */

CREATE TABLE Entity_ (
    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_name TEXT,
    entity_type_id INTEGER FOREIGN KEY REFERENCES Type_(type_id)
);

CREATE TABLE Attribute_ (
    attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
    attribute_name TEXT,
    attribute_type_id INTEGER FOREIGN KEY REFERENCES Type_(type_id)
);

CREATE TABLE Type_ (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT,
    parent_type_id INTEGER DEFAULT NULL
);

/* Relationship Table between Entities and Attributes */
CREATE TABLE EntityAttributes (
    entity_id INTEGER FOREIGN KEY REFERENCES Entity_(entity_id),
    attribute_id INTEGER FOREIGN KEY REFERENCES Attribute_(attribute_id),
    PRIMARY KEY (entity_id, attribute_id)
);

/* Tables for Specific Object Data */
CREATE TABLE TextEntry (
    entity_id INTEGER,
    attribute_id INTEGER,
    text_content TEXT,
    timestamp DATETIME,
);

CREATE TABLE Embedding (
    entity_id INTEGER,
    attribute_id INTEGER,
    embedding_data BLOB,
    metadata TEXT,
);

CREATE TABLE Model (
    entity_id INTEGER,
    attribute_id INTEGER,
    model_data BLOB,
    parameters TEXT,
);

/* Bridges between Entities and Specific Object Data */
CREATE TABLE EntityAttributes_blobs (
  entity_id INTEGER FOREIGN KEY REFERENCES Entity_(entity_id),
  blob_id INTEGER FOREIGN KEY REFERENCES blobs(blob_id),
  PRIMARY KEY (entity_id, blob_id)
);

CREATE TABLE EntityAttributes_text_files (
  entity_id INTEGER FOREIGN KEY REFERENCES Entity_(entity_id),
  file_id INTEGER FOREIGN KEY REFERENCES text_files(file_id),
  PRIMARY KEY (entity_id, file_id)
);

CREATE TABLE EntityAttributes_vector_representations (
  entity_id INTEGER FOREIGN KEY REFERENCES Entity_(entity_id),
  vector_id INTEGER FOREIGN KEY REFERENCES vector_representations(vector_id),
  PRIMARY KEY (entity_id, vector_id)
);

CREATE TABLE EntityAttributes_UFS (
  entity_id INTEGER FOREIGN KEY REFERENCES Entity_(entity_id),
  ufs_id INTEGER FOREIGN KEY REFERENCES ufs(ufs_id),
  PRIMARY KEY (entity_id, ufs_id)
  );

/* Relationships between Entities and Specific Object Data/bridges:
The bridge tables serve as a way to connect entities to UFS objects and other advanced entities, such as embeddings and Runtime_Agents. 
`"entity --> UFS ... entity --> bridge <-- UFS ... <--entity"` depicts a representation of the relationships between these entities.
Entity --> UFS: This direct relationship represents the connection between an entity and a UFS object. A UFS object captures information about a specific entity's state or behavior within the Unix File System.

Entity --> Bridge <-- UFS: This indirect relationship is mediated by the bridge table. The bridge table allows you to associate multiple UFS objects with a single entity, providing a more comprehensive view of the entity's interactions with the Unix File System.

Entity --> Bridge <-- Embedding: Similar to the UFS relationship, this indirect connection allows you to link multiple embeddings to a single entity. Embeddings represent the entity's content or features in a vectorized form, enabling efficient processing and analysis.

Entity --> Bridge <-- Runtime_Agent: This relationship associates Runtime_Agents with entities. Runtime_Agents are yet to be coded, but they are expected to represent some type of dynamic or active entity that interacts with the system. */
