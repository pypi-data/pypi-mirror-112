"""Implements Playwright's browser's Context.
"""

from typing import Any, Union

from playwright.sync_api import Browser, BrowserContext, Page
from playwbot.src.page import PlaywbotPage


class PlaywbotContext:
    def __init__(self, browser_type_instance: Browser, **kwargs):
        self._browser_type_instance = browser_type_instance
        self.context = self._start_context(**kwargs)

    def _start_context(self, **kwargs):
        return self._browser_type_instance.new_context(**kwargs)

    @staticmethod
    def close_context(context: BrowserContext):
        context.close()

    @staticmethod
    def cookies(context: BrowserContext, urls: Union[str, list[str], None] = None):
        return context.cookies(urls)

    @staticmethod
    def expect_page(
        context: BrowserContext,
        current_page: Page,
        action: str,
        action_args: list[Union[list[Any], dict[str, Any]]] = None,
        **kwargs
    ):
        """Performs supported `action` and returns new page represented by <PlaywbotPage> object.

        See https://playwright.dev/python/docs/multi-pages#handling-new-pages for
        documentation.

        Args:
            context (BrowserContext): context of the browser instance.
            current_page (PlaywbotPage): current page we are initiating the `action` on.
            action (str): [description]: type of supported action, e.g. 'click', 'submit', 'wait'.
            action_args (list[Union[list[Any], dict[str, Any]]], optional): args and kwargs for `action`. Defaults to None.

        Returns:
            [PlaywbotPage]: instance of the new <PlaywbotPage> object.
        """

        if action_args:
            args_: list[Any] = []
            kwargs_: dict[str, Any] = {}
            for arg in action_args:
                if isinstance(arg, list):
                    args_ = arg
                else:
                    kwargs_ = arg

        with context.expect_page(**kwargs) as new_page_manager:
            if action == "click":
                current_page.click(*args_, **kwargs_)

        new_page: Page = new_page_manager.value
        new_playwbot_page: PlaywbotPage = PlaywbotPage(context)
        # modify property = add new page
        new_playwbot_page.page = new_page
        return new_playwbot_page
