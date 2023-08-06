import functools


def async_wrappers(report_name, timer, skip_if, original, wrapped):
    async def timed_original(parent_duration, *args, **kwargs):
        # Here we exclude just the time spent in the original
        with timer(report_name="%s.orig" % report_name,
                   exclude_from=parent_duration):
            return await original(*args, **kwargs)

    @functools.wraps(original)
    async def new_wrapped(*args, **kwargs):
        # Here we time the whole duration
        with timer(report_name) as parent_duration:
            if skip_if and skip_if():
                return await timed_original(
                    parent_duration, *args, **kwargs)
            else:
                orig = functools.partial(timed_original,
                                         parent_duration)
                return await wrapped(orig, *args, **kwargs)
    return timed_original, new_wrapped
