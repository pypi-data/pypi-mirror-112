"""Implements methods shared by Page, or Frame and ElementHandle classes.
"""


from typing import Any, Literal, Union
from playwright.sync_api import Page, ElementHandle, Frame


class Handle:
    def __init__(self, handle: Union[Page, ElementHandle, Frame]) -> None:
        self.handle: Union[Page, ElementHandle, Frame] = handle

    def check(self, selector: Union[str, None] = None, **kwargs):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.check(selector, **kwargs)

        return self.handle.check(**kwargs)

    def click(self, selector: Union[str, None] = None, **kwargs):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.click(selector=selector, **kwargs)

        if isinstance(self.handle, ElementHandle) and selector is None:
            return self.handle.click(**kwargs)

    def content_frame(self):
        if isinstance(self.handle, ElementHandle):
            return self.handle.content_frame()

    def evaluate(self, expression: str, arg: Union[Any, None] = None):
        return self.handle.evaluate(expression, arg)

    def fill(self, selector: Union[str, None] = None, value: str = "", **kwargs):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.fill(selector, value, **kwargs)

        return self.handle.fill(value, **kwargs)

    def is_visible(
        self, selector: Union[str, None] = None, timeout: Union[float, None] = None
    ):
        if isinstance(self.handle, Page) and selector is not None:
            return self.handle.is_visible(selector, timeout=timeout)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and timeout is None
        ):
            return self.handle.is_visible()

    def query_selector(self, selector: str):
        return self.handle.query_selector(selector)

    def query_selector_all(self, selector: str):
        return self.handle.query_selector_all(selector)

    def screenshot(self, **kwargs):
        return self.handle.screenshot(**kwargs)

    def title(self):
        if isinstance(self.handle, (Page, Frame)):
            return self.handle.title()

    def wait_for_element_state(
        self,
        state: Literal["visible", "hidden", "enabled", "disabled", "editable"],
        **kwargs
    ):
        if isinstance(self.handle, ElementHandle):
            return self.handle.wait_for_element_state(state, **kwargs)

    def wait_for_selector(self, selector: str, **kwargs):
        return self.handle.wait_for_selector(selector, **kwargs)
