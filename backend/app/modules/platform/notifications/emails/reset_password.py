from __future__ import annotations


def render_reset_password(
    name: str | None = None, reset_url: str = ""
) -> tuple[str, str]:
    """Returns (subject, html_body) for password reset."""
    subject = "Reset your password - ADX Platform"
    greeting = f"Hi {name}," if name else "Hello,"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>Password Reset</h2>
        <p>{greeting}</p>
        <p>You requested a password reset. Click the link below to set a new password:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}"
               style="background-color: #000; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px;">
                Reset Password
            </a>
        </p>
        <p style="color: #666; font-size: 14px;">This link will expire in 24 hours. If you didn't request this, you can ignore this email.</p>
    </body>
    </html>
    """
    return subject, html
