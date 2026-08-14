from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        """
        Find a user using email.
        """

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )
    @staticmethod
    def get_by_phone_number(
         db: Session,
         phone_number: str
) -> User | None:
       return (
           db.query(User)
           .filter(User.phone_number == phone_number)
           .first()
    )


    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):
        """
        Find user using ID.
        """

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )


    @staticmethod
    def create(
        db: Session,
        user: User
    ):
        """
        Save new user.
        """

        db.add(user)

        db.commit()

        db.refresh(user)

        return user
    @staticmethod
    def count_users(
       db: Session
):
       return db.query(User).count()
    @staticmethod
    def get_all(
      db: Session
):
      return db.query(User).all()
    @staticmethod
    def update(
      db: Session,
      user: User
):
      db.commit()
      db.refresh(user)

      return user
    @staticmethod
    def count_admins(
      db: Session
):
      return (
        db.query(User)
        .filter(User.role == "admin")
        .count()
    )
    @staticmethod
    def get_by_reset_token(
      db: Session,
      token: str
):
      return (
        db.query(User)
        .filter(
            User.password_reset_token == token
        )
        .first()
    )