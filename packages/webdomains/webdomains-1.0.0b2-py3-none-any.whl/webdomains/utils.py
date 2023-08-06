import logging
import os
import threading

import click


class cached_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    A cached property can be made out of an existing method:

        url = cached_property(get_absolute_url)

    Based on `django.utils.functional.cached_property`.
    """

    name = None

    @staticmethod
    def func(instance):
        raise TypeError(
            "Cannot use cached_property instance without calling "
            "__set_name__() on it."
        )

    def __init__(self, func):
        self.real_func = func
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different "
                "names (%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


# LOGGING
# -----------------------------------------------------------------------------


class LogPipe(threading.Thread):
    """
    A pipe which outputs data to a logger.

    It is intended to be used with `subprocess` as the `stdout` or `stderr`
    arguments, i.e.:

        with LogPipe(logging.DEBUG) as stdout:
            subprocess.run(['ls', '-l', '/'], stdout=stdout)
    """

    def __init__(self, level, logger=None):
        super().__init__(daemon=False)

        self.level = level
        self.logger = logger or logging
        self.pread, self.pwrite = os.pipe()
        self.preader = os.fdopen(self.pread)

        self.start()

    def fileno(self):
        """Return the write file descriptor of the pipe."""
        return self.pwrite

    def close(self):
        """Close the write file descriptor of the pipe."""
        os.close(self.pwrite)

    def run(self):
        for line in iter(self.preader.readline, ''):
            self.logger.log(self.level, line.strip('\n'))
        self.preader.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


class ClickHandler(logging.Handler):
    """Handler which sends logging output to `click.echo`."""

    def emit(self, record):
        try:
            click.echo(
                self.format(record), err=record.levelno >= logging.ERROR
            )
        except Exception:
            self.handleError(record)


class ColorFormatter(logging.Formatter):
    """Formatter which extends `LogRecord` attributes with 'levelprefix'.

    The 'levelprefix' attribute is almost a colored version of 'levelname', see
    `ColorFormatter.STYLES` for the styles attributes.
    """

    STYLES = {
        'ERROR': dict(text='Error! ', fg='red'),
        'EXCEPTION': dict(text='Error! ', fg='red'),
        'CRITICAL': dict(text='Error! ', fg='red'),
        'INFO': dict(text=' + ', fg='blue'),
        'WARNING': dict(text='Warning: ', fg='yellow'),
    }

    def formatMessage(self, record):
        style_kwargs = self.STYLES.get(record.levelname, {})
        style_kwargs.setdefault('text', '')
        record.levelprefix = click.style(**style_kwargs)
        return super().formatMessage(record)


def setup_click_logger(logger, fmt=None):
    """Setup a logger to be used with `click`."""
    formatter = ColorFormatter(fmt or '%(levelprefix)s%(message)s')
    handler = ClickHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
