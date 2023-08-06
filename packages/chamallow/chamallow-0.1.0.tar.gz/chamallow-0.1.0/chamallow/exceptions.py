class GracefulExit(SystemExit):
    code = 1


class MessageException(Exception):
    pass
