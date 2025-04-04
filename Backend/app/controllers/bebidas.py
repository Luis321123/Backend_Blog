from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.bebidas import BebidasCreate,BebidasUpdate
from app.services.base import CRUDBase
from app.models.Bebida import Bebida
from app.responses.bebidas import bebida_response_create
class BebidaController(CRUDBase[Bebida, BebidasCreate, BebidasUpdate]):
    async def get_bebida(self, db:Session, uuid: str = None):
        if uuid:
            bebida_uuid = db.query(self.model).filter(self.model.uuid == uuid).filter(self.model.deleted_at == None).first()
            if not bebida_uuid:
                    raise HTTPException(status_code=404, detail="uuid of management_area not found.")
            return bebida_uuid
        else:
            return db.query(self.model).filter(self.model.deleted_at == None).order_by(self.model.name.asc()).all()

    async def create_bebida(self, data: BebidasCreate, session: Session):
        try:
            bebida_current = self.create(db=session, obj_in=data)
            return bebida_response_create(bebida_current)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error: {str(e)}")
    
    async def update_bebida(self, data: BebidasUpdate, user_uuid: str, session: Session):
        try:
            bebida_current = await self.get_bebida(db=session, uuid=user_uuid)
            if not bebida_current:
                raise HTTPException(status_code=404, detail="uuid of user not found.")
            
            bebida_update=self.update(db=session, db_obj=bebida_current, obj_in=data)
            return bebida_update
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")
    
    async def delete_bebida(self, bebida_uuid:str, session: Session):
        try:
            self.get(session, bebida_uuid)
            self.remove(db=session, uuid=bebida_uuid)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hay un error:{str(e)}")

bebida_controller=BebidaController(Bebida)