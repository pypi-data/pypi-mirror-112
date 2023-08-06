from trend_app_protect.exceptions import TrendAppProtectOverrideResponse
from trend_app_protect.logger import log
from trend_app_protect.patcher import monkeypatch

from . import plugin_tornado
from .plugin_tornado import _block_request, _hook_agent


def hook_tornado_http1connection_async(get_agent_func, http_adapter):
    import tornado.http1connection

    agent = get_agent_func()

    # Because the transaction is started in this function
    # we're unable to pass a timer
    @monkeypatch(
        tornado.http1connection.HTTP1Connection,
        "_read_message",
        report_name="plugin.tornado._read_message",
    )
    async def _read_message(orig, self, delegate):
        if self.is_client:
            return await orig(self, delegate)

        if not plugin_tornado.PATCHED_AGENT:
            plugin_tornado.PATCHED_AGENT = True
            _hook_agent(get_agent_func)

        agent.start_transaction()
        log.trace("Tornado transaction start: {}".format(
            agent.get_transaction_uuid()))
        try:
            return await orig(self, http_adapter(delegate, self))
        finally:
            # remove transaction from the context so it won't get copied
            # to the context of the next request, but don't finish it
            # in case some async functions are still running
            agent.clear_transaction()


def hook_tornado_web_async(timer):
    import tornado.web

    @monkeypatch(
        tornado.web.RequestHandler,
        "_execute",
        timer=timer,
        report_name="plugin.tornado.web.execute",
    )
    async def _execute(orig, self, *args, **kwargs):
        # Wrap but handle what is normally done in the exception
        # handler at the end of execute

        try:
            return await orig(self, *args, **kwargs)
        except TrendAppProtectOverrideResponse as exc:
            status, headers, body = exc.args
            _block_request(self, status, headers, body)
        return
