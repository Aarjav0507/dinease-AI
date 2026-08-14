from sqlalchemy.orm import Session

from app.models.system_setting import SystemSettings

from app.repositories.system_setting_repository import (
    SystemSettingsRepository
)


class SystemSettingsService:

    @staticmethod
    def get_settings(
        db: Session
    ) -> SystemSettings:

        settings = (
            SystemSettingsRepository.get_settings(
                db
            )
        )

        if not settings:

            settings = SystemSettings()

            settings = (
                SystemSettingsRepository.create(
                    db,
                    settings
                )
            )

        return settings