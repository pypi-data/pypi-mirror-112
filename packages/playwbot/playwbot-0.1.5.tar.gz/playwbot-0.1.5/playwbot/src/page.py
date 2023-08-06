"""Implements Playwright's Page.
"""

from typing import Any, Callable, Literal, Pattern, Union
from playwright.sync_api import BrowserContext, Page
from playwbot.src.handle import Handle


class PlaywbotPage(Handle):
    def __init__(self, browser_context: BrowserContext, **kwargs):
        self._browser_context: BrowserContext = browser_context
        self.page = self._start_page(**kwargs)
        super().__init__(self.page)

    def _start_page(self, **kwargs):
        return self._browser_context.new_page(**kwargs)

    @staticmethod
    def bring_to_front(page: Page):
        return page.bring_to_front()

    @staticmethod
    def close_page(page: Page, run_before_unload: Union[bool, None] = None):
        return page.close(run_before_unload=run_before_unload)

    @staticmethod
    def expect_event(
        page: Page,
        event: str,
        action: str,
        action_args: Union[list[dict[str, Any]], None] = None,
        **kwargs,
    ):
        """Same logic as `expect_request()` method.

        Args:
            page (Page): browser context's page instance
            event (str): event to expect, e.g. "request", "load", etc.
            action (str): action to perform when event is detected, e.g. "go to", etc.
            action_args (Union[list[dict[str, Any]], None], optional): args for `action`. Defaults to None.

        Returns:
            [Any]: object representing the event we are waiting/expecting for.
        """
        if action_args:
            args_: list[Any] = []
            kwargs_: dict[str, Any] = {}
            for item in action_args:
                if isinstance(item, list):
                    args_ = item
                else:
                    kwargs_ = item

        with page.expect_event(event, **kwargs) as event_manager:
            if action == "go to":
                page.goto(*args_, **kwargs_)
        return event_manager.value

    @staticmethod
    def expect_request(
        page: Page,
        url_or_predicate: Union[str, Pattern, Callable],
        action: str,
        action_args: Union[list[dict[str, Any]], None] = None,
        **kwargs,
    ):
        """This one is a bit tricky.
        Robot Framework does not allow to pass Keywords (which are essentially
        <Callable> types) as arguments to other Keywords.
        Thus, we have to specify needed action, which triggers awaited request by name
        and provid arguments for that action in list, if needed.

        Supported actions are so far:
            - page.goto() -> "go to"

        Action arguments to be passed as list. This list will contain one <list> for `args` to unpack
        and one <dict> for `kwargs` to unpack.

        See test file in `test/robot/test.robot` for Expect Request keyword for concrete example how
        to implement this in RF syntax.

        Args:
            page (Page): context page instance
            url_or_predicate (Union[str, Pattern, Callable]): url or predicate to be checked against
            action (str): action which triggers awaited request
            action_args (Union[list[dict[str, Any]], None], optional): args for action. Defaults to None.

        Returns:
            [playwright.sync_api.Request]: Request object
        """
        if action_args:
            args_: list[Any] = []
            kwargs_: dict[str, Any] = {}
            for item in action_args:
                if isinstance(item, list):
                    args_ = item
                else:
                    kwargs_ = item

        with page.expect_request(url_or_predicate, **kwargs) as request_manager:
            if action == "go to":
                page.goto(*args_, **kwargs_)
        return request_manager.value

    @staticmethod
    def frame(
        page: Page,
        name: Union[str, None] = None,
        url: Union[str, Pattern, Callable, None] = None,
    ):
        return page.frame(name=name, url=url)

    @staticmethod
    def go_to(page: Page, url: str, **kwargs):
        return page.goto(url, **kwargs)

    @staticmethod
    def reload(page: Page, **kwargs):
        return page.reload(**kwargs)

    @staticmethod
    def wait_for_load_state(
        page: Page,
        state: Union[Literal["load", "domcontentloaded", "networkidle"], None] = "load",
        timeout: Union[float, None] = None,
    ):
        return page.wait_for_load_state(state=state, timeout=timeout)

    @staticmethod
    def wait_for_timeout(page: Page, timeout: float):
        page.wait_for_timeout(timeout)

    @staticmethod
    def wait_for_url(page: Page, url: Union[str, Pattern, Callable], **kwargs):
        return page.wait_for_url(url, **kwargs)
