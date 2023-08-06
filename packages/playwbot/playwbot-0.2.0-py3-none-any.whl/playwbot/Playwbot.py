# pylint: disable=invalid-name, line-too-long, no-self-use, too-many-lines

"""Playbot provides operations/keywords
by playwright/python library to the robotframework.
"""

from pathlib import Path
from typing import Any, Callable, Literal, Pattern, Union

from playwright.sync_api import Browser, ElementHandle, FilePayload, Frame
from robot.api.deco import keyword, library

from playwbot.src.browser import PlaywbotBrowser
from playwbot.src.context import PlaywbotContext
from playwbot.src.page import PlaywbotPage


@library
class Playwbot:
    """Represents the library for robot framework.

    This library wraps selected methods of https://playwright.dev/python/
    which can be used as Robot Framework Keywords.

    It is strongly recommended to check https://playwright.dev/python/docs/core-concepts
    to get familiar with concept of playwright.
    """

    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, browser: str = "chromium"):
        """
        When importing the library, you have to specify, which supported browser you want to use.
        Later, when launching browser, this specified browser will be used.

        == Example ==

        === Importing library file directly ===

        |       =A=      |               =B=                   |              =C=                    |
        | ***Settings*** |                                     |                                     |
        | Library        | ${EXECDIR}${/}playwbot${/}Playwbot.py | browser=<chromium|firefox|webkit> |

        === Importing installed library ===

        |       =A=      |               =B=                   |              =C=                    |
        | ***Settings*** |                                     |                                     |
        | Library        | playwbot.Playwbot                   | browser=<chromium|firefox|webkit>   |
        """
        self._selected_browser: str = browser
        self._playbot_browser: Union[None, Browser] = None

    @keyword
    def start_browser(self, **kwargs):
        """Starts browser. Since library has default scope set to SUITE,
        user is expected to start the browser only ONCE, ideally using
        *Suite Setup* and close the browser using *Suite Teardown*.

        Starting browser is time and memory expensive. For isolated test runs,
        user wants to use browser contexts.

        See https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch for
        all available keyword arguments.

        == Example ==

        | =A=            | =B=           | =C=               |
        | ***Settings*** |               |                   |
        | Suite Setup    | Start Browser |                   |
        | Suite Setup    | Start Browser | headless=${False} |
        """
        self._playbot_browser = PlaywbotBrowser(self._selected_browser, **kwargs)

    @keyword
    def close_browser(self):
        """Closes the browser.
        This keyword should be used together with *Suite Teardown*.

        See https://playwright.dev/python/docs/api/class-browser#browser-close
        for documentation of this method.

        == Example ==

        | =A=            | =B=           |
        | ***Settings*** |               |
        | Suite Teardown | Close Browser |
        """
        self._playbot_browser.close_browser()

    @keyword
    def new_context(self, **kwargs):
        """Starts a new context of the browser.
        Contexts are incognito-like isolated sessions of the browser.
        They are fast and cheap to create and should be used for running the
        tests in the suite, NOT multiple browser instances.

        See https://playwright.dev/python/docs/api/class-browser#browser-new-context for
        all available options.

        This keyword returns *PlaywbotContext* class instance, which contains _context_
        property with created browser context.

        == Example ==

        | =A=         | =B=         |
        | ${context}= | New Context |

        === Create context with setting viewport ===

        | =A=          | =B=           | =C=                  |
        | &{viewport}= | width=${1920} | height=${1080}       |
        | ${context}=  | New Context   | viewport=&{viewport} |

        === Create multiple contexts in one browser ===

        You can create several contexts - as many as you like.
        These contexts are completely isolated, and you can reference them directly
        via variables. This may be useful for example testing some chat applications
        or for parallel test execution.

        | =A=           | =B=           | =C=                  |
        | &{viewport}=  | width=${1920} | height=${1080}       |
        | ${context1}=  | New Context   | viewport=&{viewport} |
        | ${context2}=  | New Context   |                      |
        """
        return PlaywbotContext(self._playbot_browser.browser, **kwargs)

    @keyword
    def close_context(self, context: PlaywbotContext):
        """Closes given browser context, which is represented by
        wrapper class *PlaywbotContext*.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-close for
        the command documentation.

        == Example ==

        | =A=           | =B=         |
        | Close Context | ${context}  |
        """
        context.close_context(context.context)

    @keyword
    def cookies(
        self, context: PlaywbotContext, urls: Union[str, list[str], None] = None
    ):
        """Returns list of cookies of the given browser context.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-cookies
        for command options.

        == Example ==

        === Return all cookies ===

        | =A=         | =B=     | =C= |
        | @{cookies}= | Cookies |     |

        === Return cookies which affect given url ===

        | =A=         | =B=     | =C=                   |
        | @{cookies}= | Cookies | https://some/url.com |

        === Return cookies which affect multiple urls ===

        | =A=         | =B=              | =C=              |
        | @{urls}=    | https://url1.com | https://url2.com |
        | @{cookies}= | Cookies          | ${urls}          |
        """
        return context.cookies(context.context, urls)

    @keyword
    def expect_page(
        self,
        context: PlaywbotContext,
        current_page: PlaywbotPage,
        action: str,
        action_args: list[Union[list[Any], dict[str, Any]]] = None,
        **kwargs,
    ):
        """Do the specified `action` and waits for the new <PlaywbotPage> to be created. This object
        is returned and can be assigned to the variable and used in the future.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-wait-for-page for
        the documentation.

        == Example ==
        | ==A==           | ==B==             | ==C==                            | ==D==                      |
        | ${context}=     | New Context       | viewport=&{VP_1920_1080}         |                            |
        | ${page}=        | New Page          | ${context}                       |                            |
        | ${url}=         | Convert To String | https://www.tesena.com/en        |                            |
        | @{args}=        | Create List       | //a[contains(@title, "Youtube")] |                            |
        | @{action_args}= | Create List       | ${args}                          |                            |
        | Go To           | ${page}           | ${url}                           | wait_until=networkidle     |
        | ${new_page}=    | Expect Page       | ${context}                       | ${page}                    |
        | ...             |                   | click                            | action_args=${action_args} |
        | ...             |                   | timeout=${10000}                 |                            |
        | ${check}=       | Is Type           | ${new_page}                      | playwbotPage               |
        | Should Be True  | ${check}==True    |                                  |                            |
        | Close Context   | ${context}        |                                  |                            |
        """
        return context.expect_page(
            context.context,
            current_page.page,
            action,
            action_args=action_args,
            **kwargs,
        )

    @keyword
    def new_page(self, context: PlaywbotContext, **kwargs):
        """Opens new page and returns its instance.
        It is represented by wrapper class *PlaywbotPage*, which
        contains property _page_, which represents browser context's
        page.

        See https://playwright.dev/python/docs/api/class-browsercontext#browser-context-new-page

        You can have multiple pages opened in one context. These pages are
        then accessible directly via variables they are assigned to.

        == Example ==

        === Open one page ===

        | =A=         | =B=         | =C=        |
        | ${context}= | New Context |            |
        | ${page}=    | New Page    | ${context} |

        === Open two pages ===

        | =A=         | =B=         | =C=        |
        | ${context}= | New Context |            |
        | ${page1}=   | New Page    | ${context} |
        | ${page2}=   | New Page    | ${context} |
        """
        return PlaywbotPage(context.context, **kwargs)

    @keyword
    def close_page(
        self, page: PlaywbotPage, run_before_unload: Union[bool, None] = None
    ):
        """Closes the given page.

        See https://playwright.dev/python/docs/api/class-page#page-close for
        documentation.

        == Example ==

        | =A=        | =B=      | =C=                  |
        | ${page}=   | New Page | ${context}           |
        | Go To      | ${page}  | https://some/url.com |
        | Close Page | ${page}  |                      |
        """
        return page.close_page(page.page, run_before_unload=run_before_unload)

    @keyword
    def bring_to_front(self, page: PlaywbotPage):
        """Brings given page to front - activates the tab.

        See https://playwright.dev/python/docs/api/class-page/#page-bring-to-front for
        documentation.

        == Example ==

        | =A=            | =B=      | =C=        |
        | ${page}=       | New Page | ${context} |
        | Bring To Front | ${page}  |            |
        """
        return page.bring_to_front(page.page)

    @keyword
    def check(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        **kwargs,
    ):
        """Checks an element.

        This keyword is usable with *<PlaywbotPage>*, *<ElementHandle>* and *<Frame>*.

        See https://playwright.dev/python/docs/api/class-page#page-check for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-check for
        element variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-check for
        frame variant documentation.

        == Example ==

        === Check element by Page and selector ===

        | =A=         | =B=         | =C=       |
        | Check       | ${page}     | #id=my-id |

        === Check element by Frame and selector ===

        | =A=         | =B=         | =C=       | =D=           |
        | ${frame}=   | Frame       | ${page}   | name=my-frame |
        | Check       | ${frame}    | #id=my-id |               |

        === Check element by ElementHandle ===

        | =A=         | =B=           | =C=     | =D=       |
        | ${element}= | ElementHandle | ${page} | #id=my-id |
        | Check       | ${element}    |         |           |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.check(selector, **kwargs)

        return handle.check(**kwargs)

    @keyword
    def click(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        **kwargs,
    ):
        """Click element.

        This keyword can be used either with *<PlaywbotPage>*, *<Frame>* or with *<ElementHandle>*.

        See https://playwright.dev/python/docs/api/class-page#page-click for
        click with page.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-click for
        click with element.

        See https://playwright.dev/python/docs/api/class-frame/#frame-click for
        click with frame.

        == Example ==

        === Click using page and selector ===

        | =A=          | =B=               | =C=                   |
        | ${page}=     | New Page          | ${context}            |
        | ${selector}= | Convert to string | xpath=//some-selector |
        | Click        | ${page}           | ${selector}           |

        === Click using element ===

        | =A=          | =B=               | =C=                   | =D=         |
        | ${page}=     | New Page          | ${context}            |             |
        | ${selector}= | Convert to string | xpath=//some-selector |             |
        | ${element}=  | Query Selector    | ${page}               | ${selector} |
        | Click        | ${element}        |                       |             |

        === Click using Frame ===

        | =A=                   | =B=               | =C=                   | =D=            |
        | ${page}=              | New Page          | ${context}            |                |
        | ${frame}=             | Frame             | ${page}               | name=some_name |
        | ${in_frame_selector}= | Convert To String | xpath=//some-selector |                |
        | Click                 | ${frame}          | ${in_frame_selector}  |                |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.click(selector=selector, **kwargs)
        return handle.click(**kwargs)

    @keyword
    def content_frame(self, handle: ElementHandle):
        """Returns the content frame for given <ElementHandle>. Else returns <None>.

        This keyword is very usefull, when the iframe element does not have _name_ attribute and/or
        dynamic url, so keyword *Frame* is not usable.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-content-frame for
        documentation.

        == Example ==

        | =A=                | =B=               | =C=                   |                   |
        | ${page}=           | New Page          | ${context}            |                   |
        | ${iframe_locator}= | Convert To String | xpath=//some-selector |                   |
        | ${iframe_element}= | Query Selector    | ${page}               | ${iframe_locator} |
        | ${frame}=          | Content Frame     | ${iframe_element}     |                   |
        """
        return handle.content_frame()

    @keyword
    def evaluate(
        self,
        handle: Union[PlaywbotPage, Frame],
        expression: str,
        arg: Union[Any, None] = None,
    ):
        """Evaluates the provided JavaScript expression in the browser context.
        Returns the result of the expression.

        Can be used with *<PlaywbotPage>* or *<Frame>*.

        See https://playwright.dev/python/docs/api/class-page#page-evaluate for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-evaluate for
        frame variant documentation.

        == Example ==

        === Evaluate expression in page context ===

        | =A=       | =B=      | =C=     | =D=             |
        | ${title}= | Evaluate | ${page} | document.title  |

        === Evaluate expression in frame context ===
        | =A=       | =B=      | =C=      | =D=            |
        | ${title}= | Evaluate | ${frame} | document.title |
        """
        if isinstance(handle, PlaywbotPage):
            return handle.evaluate(expression, arg=arg)
        return handle.evaluate(expression, arg=arg)

    @keyword
    def expect_event(
        self,
        page: PlaywbotPage,
        event: str,
        action: Literal["go to"],
        action_args: Union[list[dict[str, Any]], list[Any]] = None,
        **kwargs,
    ):
        """Waits for given `event` to fire. Returns object representing the event.

        See https://playwright.dev/python/docs/api/class-page#page-wait-for-event for
        documentation.

        NOTICE: You cannot provide `predicate` kwarg for this keyword, as it is possible in the
        playwright python library. This argument expects <Callable> type and to my knowledge,
        there is no (easy) way to do that in RF.

        Supported events are all those, that are available for playwrights `page.on()` method.

        The logic of this keyword is the same, as in the case of `Expect Request` keyword.

        Currently, supported actions for this keyword are:
        - Go To -> "go to"

         == Example ==

        | =A=             | =B=               | =C=                      | =D=                        |
        | ${context}=     | New Context       |                          |                            |
        | ${page}=        | New Page          | ${context}               |                            |
        | ${request_url}= | Convert To String | some_request_url         |                            |
        | @{args}=        | Create List       | https://url/to/visit.com |                            |
        | &{kwargs}=      | Create Dictionary | wait_until=networkidle   | timeout=${10000}           |
        | @{action_args}= | Create List       | ${args}                  | ${kwargs}                  |
        | ${request}=     | Expect Event      | ${page}                  | request                    |
        | ...             |                   | go to                    | action_args=${action_args} |

        """

        return page.expect_event(
            page.page, event, action, action_args=action_args, **kwargs
        )

    @keyword
    def expect_request(
        self,
        page: PlaywbotPage,
        url_or_predicate: Union[str, Pattern, Callable],
        action: Literal["go to"],
        action_args: Union[list[dict[str, Any]], list[Any]] = None,
        **kwargs,
    ):
        """Waits for the request and returns the object of the request.

        See https://playwright.dev/python/docs/api/class-page/#page-wait-for-request for
        documentation.

        Since RobotFramework does not support passing keywords as arguments
        to other keywords (essentialy that is passing a <Callable> type as an argument),
        we are doing a bit of trick.

        You have to specify the action, which triggers the awaited request, by assigned name.

        Currently, supported actions are:

        - Go To -> "go to"

        You have to also specify, if needed, `action_args` keyword argument options, which may contain:

        - <list> of args to be unpacked for *args
        - <dict> of kwargs to be unpacked for **kwargs

        == Example ==

        | =A=             | =B=               | =C=                      | =D=                        |
        | ${context}=     | New Context       |                          |                            |
        | ${page}=        | New Page          | ${context}               |                            |
        | ${request_url}= | Convert To String | some_request_url         |                            |
        | @{args}=        | Create List       | https://url/to/visit.com |                            |
        | &{kwargs}=      | Create Dictionary | wait_until=networkidle   | timeout=${10000}           |
        | @{action_args}= | Create List       | ${args}                  | ${kwargs}                  |
        | ${request}=     | Expect Request    | ${page}                  | ${request_url}             |
        | ...             |                   | go to                    | action_args=${action_args} |
        """
        return page.expect_request(
            page.page, url_or_predicate, action, action_args=action_args, **kwargs
        )

    @keyword
    def fill(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        value: str = "",
        **kwargs,
    ):
        """Fills an element.

        This keyword is usable with *<PlaywbotPage>*, *<ElementHandle>* and *<Frame>*.

        See https://playwright.dev/python/docs/api/class-page#page-fill for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-fill for
        frame variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-fill for
        element variant documentation.

        == Example ==

        === Fill element by Page and selector ===

        | =A=  | =B=     | =C=       | =D=                        |
        | Fill | ${page} | #id=my-id | some value to be filled in |

        === Fill element by Frame and selector ===

        | =A=  | =B=      | =C=       | =D=                        |
        | Fill | ${frame} | #id=my-id | some value to be filled in |

        === Fill element by ElementHandle ===

        | =A=  | =B=        | =C=                        |
        | Fill | ${element} | some value to be filled in |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.fill(selector, value, **kwargs)

        return handle.fill(value, **kwargs)

    @keyword
    def frame(
        self,
        page: PlaywbotPage,
        name: Union[str, None] = None,
        url: Union[str, Pattern, Callable, None] = None,
    ):
        """Returns frame matching the given arguments.

        You have to provide either _name_ or _url_.

        See https://playwright.dev/python/docs/api/class-page#page-frame for
        documentation.

        Returns *<Frame>* object.

        == Example ==

        | =A=       | =B=      | =C=        | =D =                       |
        | ${page}=  | New Page | ${context} |                            |
        | ${frame}= | Frame    | ${page}    | https://some/url/of/iframe |
        | ${frame}= | Frame    | ${page}    | url=**/some/pattern        |
        | ${frame}= | Frame    | ${page}    | name=frame_name            |
        """
        return page.frame(page.page, name=name, url=url)

    @keyword
    def go_to(self, page: PlaywbotPage, url: str, **kwargs):
        """Navigates to given url. Returns the response of the last redirect.

        See https://playwright.dev/python/docs/api/class-page#page-goto for
        the documentation.

        == Example ==

        | =A=          | =B=      | =C=                  | =D=                    | =E=                    |
        | ${page}=     | New Page | ${context}           |                        |                        |
        | Go To        | ${page}  | https://some/url.com |                        |                        |
        | ${response}= | Go To    | ${page}              | https://some/url.com   | wait_until=networkidle |
        """
        return page.go_to(page.page, url, **kwargs)

    @keyword
    def is_editable(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Predicate. Verifies, whether element is enabled.

        See https://playwright.dev/python/docs/api/class-page#page-is-enabled for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-is-enabled for
        frame variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-is-enabled for
        element variant documentation.

        == Example ==

        === Is Editable with page and selector ===

        | =A=            | =B=               | =C=                  | =D=         | =E=          |
        | ${page}=       | New Page          | ${context}           |             |              |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |              |
        | ${status}=     | Is Editable       | ${page}              | ${selector} | timeout=5000 |
        | Should Be True | ${status}==True   |                      |             |              |

        === Is Editable with element ===

        | =A=            | =B=               | =C=                  | =D=         |
        | ${page}=       | New Page          | ${context}           |             |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |
        | ${element}=    | Query Selector    | ${page}              | ${selector} |
        | ${status}=     | Is Editable       | ${element}           |             |
        | Should Be True | ${status}==True   |                      |             |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.is_editable(selector=selector, timeout=timeout)
        if isinstance(handle, ElementHandle):
            return handle.is_editable()

    @keyword
    def is_enabled(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Predicate. Verifies, whether element is enabled.

        See https://playwright.dev/python/docs/api/class-page#page-is-enabled for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-is-enabled for
        frame variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-is-enabled for
        element variant documentation.

        == Example ==

        === Is Enabled with page and selector ===

        | =A=            | =B=               | =C=                  | =D=         | =E=          |
        | ${page}=       | New Page          | ${context}           |             |              |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |              |
        | ${status}=     | Is Enabled        | ${page}              | ${selector} | timeout=5000 |
        | Should Be True | ${status}==True   |                      |             |              |

        === Is Hidden with element ===

        | =A=            | =B=               | =C=                  | =D=         |
        | ${page}=       | New Page          | ${context}           |             |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |
        | ${element}=    | Query Selector    | ${page}              | ${selector} |
        | ${status}=     | Is Enabled        | ${element}           |             |
        | Should Be True | ${status}==True   |                      |             |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.is_enabled(selector=selector, timeout=timeout)
        if isinstance(handle, ElementHandle):
            return handle.is_enabled()

    @keyword
    def is_hidden(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Predicate. Verifies, whether element is hidden.

        See https://playwright.dev/python/docs/api/class-page#page-is-hidden for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-is-hidden for
        element variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-is-hidden for
        frame variant documentation.

        == Example ==

        === Is Hidden with page and selector ===

        | =A=            | =B=               | =C=                  | =D=         | =E=          |
        | ${page}=       | New Page          | ${context}           |             |              |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |              |
        | ${status}=     | Is Hidden         | ${page}              | ${selector} | timeout=5000 |
        | Should Be True | ${status}==True   |                      |             |              |

        === Is Hidden with element ===

        | =A=            | =B=               | =C=                  | =D=         |
        | ${page}=       | New Page          | ${context}           |             |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |
        | ${element}=    | Query Selector    | ${page}              | ${selector} |
        | ${status}=     | Is Hidden         | ${element}           |             |
        | Should Be True | ${status}==True   |                      |             |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.is_hidden(selector=selector, timeout=timeout)
        if isinstance(handle, ElementHandle):
            return handle.is_hidden()

    @keyword
    def is_visible(
        self,
        handle: Union[PlaywbotPage, ElementHandle, Frame],
        selector: Union[str, None] = None,
        timeout: Union[float, None] = None,
    ):
        """Predicate. Verifies, whether element is visible.

        Can be used with *PlaywbotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page#page-is-visible for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-is-visible for
        element variant documentation.

        == Example ==

        === Is Visible with page and selector ===

        | =A=            | =B=               | =C=                  | =D=         | =E=          |
        | ${page}=       | New Page          | ${context}           |             |              |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |              |
        | ${status}=     | Is Visible        | ${page}              | ${selector} | timeout=5000 |
        | Should Be True | ${status}==True   |                      |             |              |

        === Is Visible with element ===

        | =A=            | =B=               | =C=                  | =D=         |
        | ${page}=       | New Page          | ${context}           |             |
        | ${selector}=   | Convert To String | xpath=/some-selector |             |
        | ${element}=    | Query Selector    | ${page}              | ${selector} |
        | ${status}=     | Is Visible        | ${element}           |             |
        | Should Be True | ${status}==True   |                      |             |
        """
        if isinstance(handle, (PlaywbotPage, Frame)) and selector is not None:
            return handle.is_visible(selector=selector, timeout=timeout)
        if isinstance(handle, ElementHandle):
            return handle.is_visible()

    @keyword
    def query_selector(self, handle: Union[PlaywbotPage, ElementHandle], selector: str):
        """Finds and returns element that matches the given selector. If no element is found, returns _None_.

        Can be used with *PlaywbotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page/#page-query-selector for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-query-selector for
        element variant documentation.

        == Example ==

        === Query Selector with page and selector ===

        | =A=              | =B=               | =C=                    | =D=             |
        | ${page}=         | New Page          | ${context}             |                 |
        | ${selector_one}= | Convert To String | xpath=//some-selector1 |                 |
        | ${element_one}=  | Query Selector    | ${page}                | ${selector_one} |

        === Query Selector from the element ===

        | =A=              | =B=               | =C=                    | =D=             |
        | ${page}=         | New Page          | ${context}             |                 |
        | ${selector_one}= | Convert To String | xpath=//some-selector1 |                 |
        | ${selector_two}= | Convert To String | xpath=//some-selector2 |                 |
        | ${element_one}=  | Query Selector    | ${page}                | ${selector_one} |
        | ${element_two}=  | Query Selector    | ${element_one}         | ${selector_two} |
        """
        return handle.query_selector(selector)

    @keyword
    def query_selector_all(
        self, handle: Union[PlaywbotPage, ElementHandle], selector: str
    ):
        """Finds all elements matching given selector and returns them in _list_. If no
        elements are found, returns an empty _list_.

        This keyword can be used with *PlaywbotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page#page-query-selector-all for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-query-selector-all for
        element variant documentation.

        == Example ==

        === With Page ===

        | =A=          | =B=                | =C=                   | =D=         |
        | ${page}=     | New Page           | ${context}            |             |
        | ${selector}= | Convert To String  | xpath=//some-selector |             |
        | @{elements}= | Query Selector All | ${page}               | ${selector} |

        === With Element ===

        | =A=            | =B=                | =C=                    | =D=           |
        | ${page}=       | New Page           | ${context}             |               |
        | ${selector_1}= | Convert To String  | xpath=//some-selector1 |               |
        | ${selector_2}= | Convert To String  | xpath=//some-selector2 |               |
        | ${element}=    | Query Selector     | ${page}                | ${selector_1} |
        | @{elements}=   | Query Selector All | ${element}             | ${selector_2} |
        """
        return handle.query_selector_all(selector)

    @keyword
    def reload(self, page: PlaywbotPage, **kwargs):
        """Reloads the page.

        Can be used with *<PlaywbotPage>*.

        See https://playwright.dev/python/docs/api/class-page/#page-reload for
        documentation.

        == Example ==

        | =A=    | =B=     | =C=                         | =D=              |
        | Reload | ${page} | wait_until=domcontentloaded | timeout=${10000} |
        """
        return page.reload(page.page, **kwargs)

    @keyword
    def set_input_files(
        self,
        page: Union[PlaywbotPage, ElementHandle, Frame],
        files: Union[
            str,
            Path,
            FilePayload,
            list[Union[str, Path]],
            list[FilePayload],
        ],
        selector: Union[str, None] = None,
        **kwargs,
    ):
        """Searches for the element by provided selector (except the case, when this keyword is called
        with <ElementHandle>) and sets the value(s) of the provided file(s).

        See https://playwright.dev/python/docs/api/class-page#page-set-input-files for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-set-input-files for
        frame variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-set-input-files for
        element variant documentation.

        == Example ==

        === With Page ===

        | =A=             | =B=         | =C=                | =D=                     |
        | ${page}=        | New Page    | ${context}         |                         |
        | Set Input Files | ${page}     | path/to/file1.txt  | //input-button-selector |
        | @{file_paths}=  | Create List | path/one/file1.png | path/two/file2.pdf      |
        | Set Input Files | ${page}     | ${file_paths}      | //input-button-selector |

        === With Element ===

        | =A=               | =B=              | =C=                | =D=                      |
        | ${input_element}= | Query Selector   | ${page}            | //input-element-selector |
        | Set Input Files   | ${input_element} | path/to/file1.txt  |                          |
        """
        if isinstance(page, (PlaywbotPage, Frame)) and selector is not None:
            return page.set_input_files(selector, files, **kwargs)

        if isinstance(page, ElementHandle) and selector is None:
            return page.set_input_files(files, **kwargs)

    @keyword
    def screenshot(self, handle: Union[PlaywbotPage, ElementHandle], **kwargs):
        """Saves screenshot of the page or element.

        Can be used with *<PlaywbotPage>* or *<ElementHandle>*.

        Take care - some kwargs are not available for _<ElementHandle>_ variant.
        See documentation.

        See https://playwright.dev/python/docs/api/class-page/#page-screenshot for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle/#element-handle-screenshot for
        element variant documentation.

        == Example ==

        === With Page ===

        | =A=        | =B=     | =C=              | =D=                    |
        | Screenshot | ${page} | path=path/to/file.png | full_page=${True} |

        === With Element ===
        | =A=        | =B=        | =C=                   |
        | Screenshot | ${element} | path=path/to/file.png |

        """
        return handle.screenshot(**kwargs)

    @keyword
    def title(self, handle: Union[PlaywbotPage, Frame]):
        """Returns the title of the page or frame.

        Can be used with *<PlaywbotPage>* or *<Frame>*.

        See https://playwright.dev/python/docs/api/class-page#page-title for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-frame/#frame-title for
        frame variant documentation.

        == Example ==

        === With Page ===

        | =A=       | =B=      | =C=        |
        | ${page}=  | New Page | ${context} |
        | ${title}= | Title    | ${page}    |

        === With Frame ===

        | =A=       | =B=   | =C=             |
        | ${frame}= | Frame | name=frame_name |
        | ${title}= | Title | ${frame}        |
        """
        if isinstance(handle, PlaywbotPage):
            return handle.page.title()

        return handle.title()

    @keyword
    def wait_for_element_state(
        self,
        handle: ElementHandle,
        state: Literal["visible", "hidden", "enabled", "disabled", "editable"],
        **kwargs,
    ):
        """Waits, until given state is satisfied. If state is not satisfied until given timeout, the
        keyword will throw an error.

        Returns None.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-wait-for-element-state for
        documentation.

        == Example ==

        | =A=                    | =B=               | =C=                   | =D=         | =E=            |
        | ${page}=               | New Page          | ${context}            |             |                |
        | ${selector}=           | Convert To String | xpath=//some-selector |             |                |
        | ${element}=            | Wait For Selector | ${page}               | ${selector} | state=attached |
        | Wait For Element State | ${element}        | visible               |             |                |
        """
        return handle.wait_for_element_state(state, **kwargs)

    @keyword
    def wait_for_load_state(
        self,
        page: PlaywbotPage,
        state: Union[Literal["load", "domcontentloaded", "networkidle"], None] = "load",
        timeout: Union[float, None] = None,
    ):
        """Returns, when the given load state of the page was reached.

        Default state is set to _load_.

        See https://playwright.dev/python/docs/api/class-page#page-wait-for-load-state for
        documentation.

        == Example ==

        | =A=                 | =B=      | =C=                  | =D=           |
        | ${page}=            | New Page | ${context}           |               |
        | Go To               | ${page}  | https://some/url.com |               |
        | Wait For Load State | ${page}  | state=networkidle    | timeout=10000 |
        """
        return page.wait_for_load_state(page.page, state=state, timeout=timeout)

    @keyword
    def wait_for_selector(
        self, handle: Union[PlaywbotPage, ElementHandle], selector: str, **kwargs
    ):
        """Returns element, if matches the given selector and if satisfies the state option (in **kwargs).
        Default options for state is _visible_.

        If the element is not returned withing given timeout, the keyword will throw.

        This keyword can be used with *PlaywbotPage* or *ElementHandle*.

        See https://playwright.dev/python/docs/api/class-page/#page-wait-for-selector for
        page variant documentation.

        See https://playwright.dev/python/docs/api/class-elementhandle#element-handle-wait-for-selector for
        element variant documentation.

        == Example ==

        === Wait For Selector with page and selector ===

        | =A=          | =B=               | =C=                   | =D=         | =E=            |
        | ${page}=     | New Page          | ${context}            |             |                |
        | ${selector}= | Convert To String | xpath=//some-selector |             |                |
        | ${element}=  | Wait For Selector | ${page}               | ${selector} |                |
        | ${element}=  | Wait For Selector | ${page}               | ${selector} | state=attached |

        === Wait For Selector with element and selector ===

        | =A=           | =B=               | =C=                    | =D=         | =E=            |
        | ${page}=      | New Page          | ${context}             |             |                |
        | ${selector}=  | Convert To String | xpath=//some-selector  |             |                |
        | ${selector_2} | Convert To String | xpath=//some-selector2 |             |                |
        | ${element}=   | Wait For Selector | ${page}                | ${selector} |                |
        | ${element2}=  | Wait For Selector | ${element}             | ${selector} | state=visible  |
        """
        return handle.wait_for_selector(selector, **kwargs)

    @keyword
    def wait_for_timeout(self, page: PlaywbotPage, timeout: float):
        """Waits for given timeout provided in miliseconds.

        See https://playwright.dev/python/docs/api/class-page/#page-wait-for-timeout for
        documentation.

        == Example ==

        | =A=              | =B=      | =C=        |
        | ${page}=         | New Page | ${context} |
        | Wait For Timeout | ${page}  | 5000       |
        """
        page.wait_for_timeout(page.page, timeout)

    @keyword
    def wait_for_url(
        self, page: PlaywbotPage, url: Union[str, Pattern, Callable], **kwargs
    ):
        """Waits until the navigation to the given _url_ is completed.

        This keyword can be used, when interaction (e.g. click) with some element of
        the page leads to indirect navigation.

        See https://playwright.dev/python/docs/api/class-page#page-wait-for-url for
        documentation.

        == Example ==

        | =A=          | =B=               | =C=                   | =D=                    | =E=           |
        | ${selector}= | Convert To String | xpath=//some-selector |                        |               |
        | ${page}=     | New Page          | ${context}            |                        |               |
        | Click        | ${page}           | ${selector}           |                        |               |
        | Wait For Url | ${page}           | **/page.html          | wait_until=networkidle | timeout=30000 |
        """
        return page.wait_for_url(page.page, url, **kwargs)
