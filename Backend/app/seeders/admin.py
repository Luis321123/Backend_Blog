from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.User import User  # Asegúrate que la importación sea correcta
from app.core.security import get_password_hash
from app.core.settings import get_settings

settings = get_settings()

def seed_admin():
    db = SessionLocal()
    try:
        # UUID fijo para el rol admin (debe coincidir con el del seeder de roles)
        ADMIN_ROLE_UUID = UUID('00000000-0000-0000-0000-000000000001')
        
        admin = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
        
        if not admin:
            admin_user = User(
                email=settings.FIRST_ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                role_uuid=ADMIN_ROLE_UUID,  # Usamos el UUID del rol admin
                is_active=True
                # Añade otros campos requeridos por tu modelo User
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuario admin creado exitosamente")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando admin: {str(e)}")
        raise
    finally:
        db.close()