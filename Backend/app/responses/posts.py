from typing import Dict

def post_response_create(post_current) -> Dict:
    return {
        "uuid": post_current.uuid,
        "title": post_current.title,
        "slug": post_current.slug,
        "desc": post_current.desc,
        "content": post_current.content,
        "img": post_current.img,  
        "created_at": post_current.created_at,
        "deleted_at": post_current.deleted_at
    }

def post_response_get(post_current) -> Dict:
    return {
        "uuid": post_current.uuid,
        "title": post_current.title,
        "desc": post_current.desc,
        "content": post_current.content,
        "img": post_current.img,  
        "slug": post_current.slug,
        "created_at": post_current.created_at,
        "deleted_at": post_current.deleted_at
    }