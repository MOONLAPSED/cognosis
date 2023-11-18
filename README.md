# cognosis
## kernel-level agentic LLM RLHF OS -- under development.


### db example:
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
