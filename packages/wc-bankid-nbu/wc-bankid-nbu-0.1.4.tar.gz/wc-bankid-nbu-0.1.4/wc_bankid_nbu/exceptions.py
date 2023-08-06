__all__ = (
    'IDError',
    'SignerError',
    'SignerNotLoaded',
    'SignerPrivateKeyNotRead',
)


class IDError(Exception):
    pass


class SignerError(IDError):
    pass


class SignerNotLoaded(SignerError):
    pass


class SignerPrivateKeyNotRead(SignerError):
    pass
