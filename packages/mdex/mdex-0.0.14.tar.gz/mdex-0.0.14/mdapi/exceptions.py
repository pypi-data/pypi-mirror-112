class MdException(Exception):
    pass


class NotLoggedIn(MdException):
    pass


class ActionForbidden(MdException):
    pass


class RefreshTokenFailed(MdException):
    pass


class DownloadException(MdException):
    pass


class NoFollowRedirect(DownloadException):
    pass


class InvalidStatusCode(DownloadException):
    pass


class InvalidFileLength(DownloadException):
    pass
