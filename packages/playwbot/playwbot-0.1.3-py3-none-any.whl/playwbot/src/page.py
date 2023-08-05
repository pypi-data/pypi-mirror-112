"""Implements Playwright's Page.
"""

from typing import Callable, Literal, Pattern, Union
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
