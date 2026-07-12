from __future__ import annotations


def render_verify_email(name: str, verification_url: str) -> tuple[str, str]:
    """Returns (subject, html_body) for email verification."""
    subject = "Verify your email - ADX Platform"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>Welcome to ADX Platform</h2>
        <p>Hi {name},</p>
        <p>Please verify your email address by clicking the link below:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{verification_url}"
               style="background-color: #000; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px;">
                Verify Email
            </a>
        </p>
        <p style="color: #666; font-size: 14px;">If you didn't create an account, you can ignore this email.</p>
    </body>
    </html>
    """
    return subject, html
