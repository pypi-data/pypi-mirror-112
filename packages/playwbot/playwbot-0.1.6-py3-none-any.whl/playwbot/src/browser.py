"""Implements Playwright's Browser.
"""

from playwright.sync_api import sync_playwright


class PlaywbotBrowser:
    def __init__(self, browser: str = "chromium", **kwargs):
        self._playwright = self._start_playwright()
        self.browser = self._start_browser(browser, **kwargs)

    @staticmethod
    def _start_playwright():
        return sync_playwright().start()

    def _start_browser(self, browser: str, **kwargs):
        if browser == "chromium":
            return self._playwright.chromium.launch(**kwargs)

        if browser == "firefox":
            return self._playwright.firefox.launch(**kwargs)

        if browser == "webkit":
            return self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    def close_browser(self):
        self.browser.close()
        self._playwright.stop()
