from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "adx-platform"
    debug: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/adx"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Logging
    log_level: str = "info"

    # JWT
    jwt_private_key_path: str = "keys/dev-private.pem"
    jwt_public_key_path: str = "keys/dev-public.pem"
    jwt_algorithm: str = "RS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 30

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 10
    rate_limit_window_seconds: int = 60

    # Password policy
    password_min_length: int = 8
    password_max_length: int = 128
    password_require_upper: bool = True
    password_require_lower: bool = True
    password_require_digit: bool = True
    password_require_special: bool = False

    # Email / Notifications
    email_provider: str = "console"
    resend_api_key: str = ""
    email_from_address: str = "ADX <noreply@adhyayanx.in>"
