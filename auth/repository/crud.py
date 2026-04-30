from sqlmodel import Session, select
from auth.models.user import User


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id) -> User | None:
    return session.get(User, user_id)
