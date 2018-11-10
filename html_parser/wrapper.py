class Wrapper(object):
    def __init__(self, wrapped_class):
        self.wrapped_class = wrapped_class()

    def __getattr__(self, attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.wrapped_class:
                    return self
                return result
            return hooked
        else:
            return orig_attr

    def run(self, html):
        self.feed(html)
        self.remove_initial_blank_records()

    def remove_initial_blank_records(self):
        del self.records[0]
        del self.records[0]
