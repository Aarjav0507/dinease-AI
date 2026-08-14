from sqlalchemy.orm import Session

from app.models.system_setting import SystemSettings


class SystemSettingsRepository:

    @staticmethod
    def get_settings(
        db: Session
    ):

        return (
            db.query(SystemSettings)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        settings: SystemSettings
    ):

        db.add(settings)
        db.commit()
        db.refresh(settings)

        return settings

    @staticmethod
    def update(
        db: Session,
        settings: SystemSettings
    ):

        db.commit()
        db.refresh(settings)

        return settings