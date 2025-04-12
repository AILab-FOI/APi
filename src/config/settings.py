from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the orchestration.
    """

    xmpp_host: str
    examples_dir: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
