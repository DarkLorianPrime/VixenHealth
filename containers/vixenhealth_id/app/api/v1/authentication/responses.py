class Exceptions:
    NOT_VALID_CYRILLIC_OR_LENGTH = (
        "Password must be longer than 8 characters and contain only english symbols, "
        "nums and special symbols."
    )
    ACCOUNT_EXISTS = "Account with this username or email already exists"
    LOGIN_OR_PASSWORD_NF = "Account with this login or password not exists"
    USERNAME_NOT_VALID = "Username not valid. Valid scheme: /^[A-Za-z0-9]{4,32}$/"
    EMAIL_NOT_VALID = "Email not valid. Valid scheme: /^\\S+@\\S+\\.\\S+$/"
    NOT_EMAIL_NOT_USERNAME = "Email or username was not shared"
    INVALID_TOKEN_REFRESH = "Refresh token is invalid"
    INVALID_TOKEN_ACCESS = "Authorization token is invalid"
    REFRESH_TOKEN_EXPIRED = "Refresh token is expired"
    BEARER_SCHEME_ERROR = "Authentication scheme is not supported. Valid scheme: Bearer"
    TOKEN_NOT_AVAILABLE = "Token is not available"
    TOKEN_IS_EXPIRED = "Token is expired"
    ACCOUNT_NOT_RELATED = "Oauth account not related to accounts"
