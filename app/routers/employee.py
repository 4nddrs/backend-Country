from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud import employee as crud_employee
from app.schemas import employee as schemas_employee
from pydantic import BaseModel, EmailStr
from app.supabase_client import get_supabase_admin_client
from datetime import datetime

router = APIRouter(prefix="/employees", tags=["employees"])

class EmployeeAccountCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    fullName: str

@router.post("/create-account", status_code=status.HTTP_201_CREATED)
def create_employee_account(account_data: EmployeeAccountCreate):  # <- Cambié 'async def' a 'def'
    """
    Crea una cuenta de usuario en Supabase Auth y en erp_user para un empleado.
    La cuenta se crea pre-aprobada con rol de Caballerizo (rol 9).
    """
    try:
        supabase_admin = get_supabase_admin_client()
        
        # Validar longitud de contraseña
        if len(account_data.password) < 6:
            raise HTTPException(
                status_code=400, 
                detail="La contraseña debe tener al menos 6 caracteres"
            )
        
        # 1. Crear usuario en Supabase Auth
        try:
            auth_response = supabase_admin.auth.admin.create_user({
                "email": account_data.email,
                "password": account_data.password,
                "email_confirm": True,
                "user_metadata": {
                    "full_name": account_data.fullName,
                    "username": account_data.username
                }
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo crear el usuario en Supabase Auth"
                )
            
            user_uid = auth_response.user.id
            
        except HTTPException:  # <- Agregué esto para re-lanzar HTTPException
            raise
        except Exception as auth_error:
            error_message = str(auth_error)
            if "already registered" in error_message.lower() or "already exists" in error_message.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"El correo {account_data.email} ya está registrado"
                )
            raise HTTPException(
                status_code=400,
                detail=f"Error al crear usuario en Supabase: {error_message}"
            )
        
        # 2. Crear registro en erp_user con rol de Caballerizo (9)
        try:
            erp_user_data = {
                "uid": user_uid,
                "username": account_data.username,
                "email": account_data.email,
                "isapproved": True,
                "fk_idUserRole": 9,
                "approved_at": datetime.utcnow().isoformat(),
                "created_at": datetime.utcnow().isoformat()
            }
            
            erp_user_response = supabase_admin.table("erp_user").insert(erp_user_data).execute()
            
            if not erp_user_response.data:
                try:
                    supabase_admin.auth.admin.delete_user(user_uid)
                except:
                    pass
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo crear el registro en erp_user"
                )
                
        except HTTPException:  # <- Agregué esto también
            raise
        except Exception as db_error:
            try:
                supabase_admin.auth.admin.delete_user(user_uid)
            except:
                pass
            
            error_message = str(db_error)
            if "duplicate key" in error_message.lower() or "unique" in error_message.lower():
                raise HTTPException(
                    status_code=400,
                    detail=f"El usuario '{account_data.username}' ya existe"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear registro en base de datos: {error_message}"
            )
        
        return {
            "uid": user_uid,
            "username": account_data.username,
            "email": account_data.email,
            "message": "Cuenta de empleado creada exitosamente",
            "role": "Caballerizo"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al crear cuenta: {str(e)}"
        )


@router.post(
    "/",
    response_model=schemas_employee.Employee,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(employee_in: schemas_employee.EmployeeCreate):
    try:
        employee = await crud_employee.create_employee(employee_in)
        if not employee:
            raise HTTPException(status_code=400, detail="No se pudo crear el empleado.")
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=List[schemas_employee.Employee])
async def list_employees(skip: int = 0, limit: int = 100):
    employees = await crud_employee.get_employees(skip=skip, limit=limit)
    return employees


@router.get("/{idEmployee}", response_model=schemas_employee.Employee)
async def get_employee(idEmployee: int):
    employee = await crud_employee.get_employee(idEmployee)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    return employee


@router.put("/{idEmployee}", response_model=schemas_employee.Employee)
async def update_employee(
    idEmployee: int,
    employee_in: schemas_employee.EmployeeUpdate,
):
    try:
        updated = await crud_employee.update_employee(idEmployee, employee_in)
        if not updated:
            raise HTTPException(status_code=404, detail="Empleado no encontrado.")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{idEmployee}", response_model=schemas_employee.Employee)
async def delete_employee(idEmployee: int):
    deleted = await crud_employee.delete_employee(idEmployee)
    if not deleted:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    return deleted
