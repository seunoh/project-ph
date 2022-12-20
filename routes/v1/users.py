from fastapi import APIRouter

router = APIRouter()


@router.post('/register')
async def register():
    return ''


@router.post('/logout')
async def logout():
    return ''
