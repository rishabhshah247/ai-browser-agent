from langchain.tools import tool
from playwright.sync_api import Page

class BrowserTools:
    def __init__(self, page: Page):
        self.page = page

    @tool
    def navigate_to(self, url: str):
        """Use this tool to navigate the browser to a specific URL."""
        self.page.goto(url)
        return f"Successfully navigated to {url}"

    @tool
    def click_element(self, selector: str):
        """Use this tool to click on a specific CSS element on the page."""
        self.page.click(selector)
        return f"Clicked on {selector}"

    @tool
    def type_text(self, selector: str, text: str):
        """Use this tool to type text into a specific CSS element/input field."""
        self.page.fill(selector, text)
        return f"Typed '{text}' into {selector}"