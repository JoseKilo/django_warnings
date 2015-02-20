from functools import partial


class register_warning(object):
    """
    A Decorator for model methods, When used it generates a warning for the
    output that the method returns
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
        When called, if a result is returned (either a string, or an iterable
        of strings), generate a warning for it
        """
        result = self.func(obj, *args, **kwargs)

        if result:
            if hasattr(result, '__iter__'):
                for message in result:
                    obj.generate_warning(message, method=self.func.func_name)
            else:
                obj.generate_warning(result, method=self.func.func_name)

        return result
