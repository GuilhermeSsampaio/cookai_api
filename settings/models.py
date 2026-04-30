def setup_models() -> None:
    from auth.models.user import User  # noqa: F401
    from auth.models.auth_provider import AuthProvider  # noqa: F401
    from models.recipe import Recipe  # noqa: F401
