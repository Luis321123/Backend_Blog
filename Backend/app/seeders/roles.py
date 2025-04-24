from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.Role import Roles  # Asegúrate que la importación sea correcta

def seed_roles():
    db = SessionLocal()
    try:
        # Definimos UUIDs fijos para roles importantes
        ADMIN_UUID = UUID('00000000-0000-0000-0000-000000000001')
        USER_UUID = UUID('00000000-0000-0000-0000-000000000002')
        
        roles_data = [
            {
                "uuid": ADMIN_UUID,
                "name": "admin",
                "description": "Administrator with full access"
            },
            {
                "uuid": USER_UUID,
                "name": "user",
                "description": "Regular user with basic access"
            }
        ]
        
        for role_data in roles_data:
            if not db.query(Roles).filter(Roles.uuid == role_data["uuid"]).first():
                db.add(Roles(**role_data))
        
        db.commit()
        print("✅ Roles creados exitosamente")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando roles: {str(e)}")
        raise
    finally:
        db.close()