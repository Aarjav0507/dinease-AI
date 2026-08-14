from app.utils.email_sender import EmailSender


class NotificationService:

    @staticmethod
    def send_reservation_confirmation(
        email: str,
        reservation_id: int
    ):

        EmailSender.send_email(
            recipient=email,
            subject="Reservation Confirmed",
            body=(
                f"Your reservation #{reservation_id} "
                f"has been confirmed."
            )
        )

    @staticmethod
    def send_refund_confirmation(
        email: str,
        refund_amount: float
    ):

        EmailSender.send_email(
            recipient=email,
            subject="Refund Processed",
            body=(
                f"Refund of ₹{refund_amount} "
                f"has been processed."
            )
        )
    @staticmethod
    def send_password_reset_email(
      email: str,
      reset_link: str
):

     EmailSender.send_email(
        recipient=email,
        subject="Reset Your Password",
        body=(
            f"Click the link below to reset your password:\n\n"
            f"{reset_link}\n\n"
            f"This link will expire in 15 minutes."
        )
    )