from typing import Dict

def blog_response_create(bebida_current: Dict) -> Dict:
    return {
        "uuid": bebida_current.uuid,
        "name": bebida_current.name,
        "title": bebida_current.title,
        "desc": bebida_current.desc,
        "img": bebida_current.img,
        "created_at": bebida_current.created_at,
        "deleted_at": bebida_current.deleted_at
    }