from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from auth.models.user import User
from auth.models.auth_provider import AuthProvider


def _unique_username(session: Session, base_username: str) -> str:
    candidate = base_username
    suffix = 1
    while session.exec(select(User).where(User.username == candidate)).first():
        suffix += 1
        candidate = f"{base_username}{suffix}"
    return candidate


def get_or_create_oauth_user(
    session: Session, email: str, provider: str, provider_user_id: str
) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if user:
        return user

    base_username = email.split("@")[0]
    user = User(username=_unique_username(session, base_username), email=email)
    session.add(user)
    session.commit()
    session.refresh(user)

    try:
        provider_record = AuthProvider(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
        )
        session.add(provider_record)
        session.commit()
    except IntegrityError:
        session.rollback()

    return user
