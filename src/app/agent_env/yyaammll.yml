data = {
    "entity": {
        "id": "unique_identifier",
        "name": "entity_name",
        "description": "entity_description",
        "attributes": [
            {
                "name": "attribute_name",
                "type": "attribute_type",
                "description": "attribute_description",
                "required": True
            },
            # ... more attributes
        ],
        "relationships": [
            {
                "entity_id": "related_entity_id",
                "relationship_type": "relationship_type"
            },
            # ... more relationships
        ]
    }
}

yaml_string = ""
for key, value in data.items():
    yaml_string += f"{key}:\n"
    if isinstance(value, dict):
        for inner_key, inner_value in value.items():
            yaml_string += f"  {inner_key}: {inner_value}\n"
    elif isinstance(value, list):
        for item in value:
            yaml_string += "  -\n"
            for inner_key, inner_value in item.items():
                yaml_string += f"    {inner_key}: {inner_value}\n"

print(yaml_string)