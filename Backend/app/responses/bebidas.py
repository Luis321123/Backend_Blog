from typing import Dict

def bebida_response_create(bebida_current) -> Dict:
    return {
        "uuid": bebida_current.uuid,
        "name": bebida_current.name,
        "coste": bebida_current.coste,
        "status": bebida_current.status,
        "time_get": bebida_current.time_get,
        "deleted_at": bebida_current.deleted_at
    }