"""Implements methods shared by Page, or Frame and ElementHandle classes.
"""

from pathlib import Path
from typing import Any, Literal, Union

from playwright.sync_api import ElementHandle, FilePayload, Frame, Page


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

        raise TypeError(f"{self.handle.__repr__()} is not of supported type.")

    def content_frame(self):
        if isinstance(self.handle, ElementHandle):
            return self.handle.content_frame()

        raise TypeError(f"{self.handle.__repr__()} is not of supported type.")

    def evaluate(self, expression: str, arg: Union[Any, None] = None):
        return self.handle.evaluate(expression, arg)

    def fill(self, selector: Union[str, None] = None, value: str = "", **kwargs):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.fill(selector, value, **kwargs)

        return self.handle.fill(value, **kwargs)

    def is_editable(
        self, selector: Union[str, None] = None, timeout: Union[float, None] = None
    ):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.is_editable(selector, timeout=timeout)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and timeout is None
        ):
            return self.handle.is_editable()

        raise RuntimeError(
            "Please check, if you provided correct type for handle arg \
            and if some kwargs are not provided by mistake."
        )

    def is_hidden(
        self, selector: Union[str, None] = None, timeout: Union[float, None] = None
    ):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.is_hidden(selector, timeout=timeout)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and timeout is None
        ):
            return self.handle.is_hidden()

        raise RuntimeError(
            "Please check, if you provided correct type for handle arg \
            and if some kwargs are not provided by mistake."
        )

    def is_enabled(
        self, selector: Union[str, None] = None, timeout: Union[float, None] = None
    ):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.is_enabled(selector, timeout=timeout)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and timeout is None
        ):
            return self.handle.is_enabled()

        raise RuntimeError(
            "Please check, if you provided correct type for handle arg \
            and if some kwargs are not provided by mistake."
        )

    def is_visible(
        self, selector: Union[str, None] = None, timeout: Union[float, None] = None
    ):
        if isinstance(self.handle, (Page, Frame)) and selector is not None:
            return self.handle.is_visible(selector, timeout=timeout)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and timeout is None
        ):
            return self.handle.is_visible()

        raise RuntimeError(
            "Please check, if you provided correct type for handle arg \
            and if some kwargs are not provided by mistake."
        )

    def query_selector(self, selector: str):
        return self.handle.query_selector(selector)

    def query_selector_all(self, selector: str):
        return self.handle.query_selector_all(selector)

    def set_input_files(
        self,
        selector: Union[str, None],
        files: Union[
            str,
            Path,
            FilePayload,
            list[Union[str, Path]],
            list[FilePayload],
        ],
        **kwargs,
    ):
        if (
            isinstance(self.handle, (Page, Frame))
            and selector is not None
            and files is not None
        ):
            return self.handle.set_input_files(selector, files, **kwargs)

        if (
            isinstance(self.handle, ElementHandle)
            and selector is None
            and files is not None
        ):
            return self.handle.set_input_files(files, **kwargs)

        raise RuntimeError(
            "Please check, if you provided correct type for handle arg \
            and if some kwargs are not provided by mistake."
        )

    def screenshot(self, **kwargs):
        return self.handle.screenshot(**kwargs)

    def title(self):
        if isinstance(self.handle, (Page, Frame)):
            return self.handle.title()

    def wait_for_element_state(
        self,
        state: Literal["visible", "hidden", "enabled", "disabled", "editable"],
        **kwargs,
    ):
        if isinstance(self.handle, ElementHandle):
            return self.handle.wait_for_element_state(state, **kwargs)

        raise TypeError(f"{self.handle.__repr__()} is not of supported type.")

    def wait_for_selector(self, selector: str, **kwargs):
        return self.handle.wait_for_selector(selector, **kwargs)
