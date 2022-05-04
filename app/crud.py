from .models import Target, Group, Category, Status
from datetime import datetime
from typing import List
from sqlmodel import Session, select

def exception_handle(msg: str):
    def wrapper_1(fn):
        def wrapper_2(*args, **kargs):
            try:
                return fn(*args, **kargs)
            except Exception as e:
                print(f'At {msg}: {e}')

        return wrapper_2
    return wrapper_1


@exception_handle('addTargets')
def addTargets(target_list: List[Target], session: Session):
    now = datetime.now()

    for item in target_list:
        item.added_time = now
        target = Target(**item.dict())
        session.add(target)
    
    session.commit()


@exception_handle('getTargets')
def getTargets(status: int, session: Session):
    return session.exec(select(Target).where(Target.status_id == status)).all()



@exception_handle('addGroup')
def addGroup(group_name: str, session: Session):
    new_group = Group(group=group_name)
    session.add(new_group)
    session.commit()


@exception_handle('addCategory')
def addCategory(cat_name: str, session: Session):
    new_cat = Category(category=cat_name)
    session.add(new_cat)
    session.commit()