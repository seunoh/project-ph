from fastapi import APIRouter

router = APIRouter()


@router.post('/create')
async def create():
    """
    가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
    :return:
    """
    return ''


@router.put('/modify')
async def modify():
    """
    가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
    :return:
    """
    return ''


@router.post('/delete')
async def delete():
    """
    가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
    :return:
    """
    return ''


@router.get('/history')
async def history():
    """
    가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다.
    :return:
    """
    return ''


@router.get('/detail')
async def detail():
    """
    가계부에서 상세한 세부 내역을 볼 수 있습니다.
    :return:
    """
    return ''


@router.post('/copy')
async def copy():
    """
    가계부의 세부 내역을 복제할 수 있습니다.
    :return:
    """
    return ''


@router.post('/share')
async def share():
    """
    가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
    (단축 URL은 특정 시간 뒤에 만료되어야 합니다.)
    :return:
    """
    return ''
