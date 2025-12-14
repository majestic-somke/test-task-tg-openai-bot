from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import DATABASE_URL
from db.models import Base, User, Message



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def add_user(telegram_id: int) -> None:
    print(f"[add_user]: {telegram_id}")
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user is None:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()


def save_message(telegram_id: int, role: str, text: str) -> None:
    print(f"[save_message] {telegram_id}: {text}")
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user is None:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
        msg = Message(user_id=user.id, role=role, text=text)
        session.add(msg)
        session.commit()


def get_context(telegram_id: int, limit: int = 10) -> list[dict]:
    print(f"[get_context] {telegram_id}")
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user is None:
            return []
        messages = (
            session.query(Message)
            .filter(Message.user_id == user.id)
            .order_by(Message.id.desc())
            .limit(limit)
            .all()
        )
        messages = list(reversed(messages))
        return [{"role": m.role, "content": m.text} for m in messages]


def reset_context(telegram_id: int) -> None:
    print(f"[reset_context] {telegram_id}")

    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        if user is None:
            return
        session.query(Message).filter(Message.user_id == user.id).delete()
        session.commit()
