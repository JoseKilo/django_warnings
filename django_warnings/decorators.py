from functools import partial

from .warnings import DjangoWarning


class register_warning(object):
    """
    A Decorator for model methods, When used it catches Warnings raised by
    the method its wrapping, its geared to work with an instance
    """

    def __init__(self, func):
        """
        save the original method and mark it as a warning_method
        """
        self.func = func
        self.func.is_warning = True

    def __get__(self, obj, objtype=None):
        """
        If we are unbound, return our function as is, otherwise use partial
        to wrap our function
        """
        if obj is None:
            return self.func

        return partial(self, obj)

    def __call__(self, obj, *args, **kwargs):
        """
        If the function raises a DjangoWarning, generate a warning
        instance for it
        """

        result = None

        try:
            result = self.func(obj, *args, **kwargs)
        except DjangoWarning as warning:
            obj.generate_warning(
                warning.message,
                method=self.func.func_name,
                identifier=warning.identifier,
                url_params=warning.url_params
            )

        return result
