activite_update_schema = {
    'type': 'object',
    'required': ['type_installation', 'nom'],
    'properties': {
        'type_installation': {
            'type': 'string'
        },
        'nom': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
