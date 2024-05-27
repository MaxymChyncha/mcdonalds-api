import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from items import Product


class BaseScraper:
    """
    Base class for web scrapers.

    Initializes a Chrome WebDriver with specified options for headless browsing
    and a custom user agent.

    Attributes:
        options (Options): WebDriver options for configuring the browser.
        driver (WebDriver): WebDriver instance for interacting with the browser.
    """

    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self._add_options())

    def _add_options(self) -> Options:
        """
        Adds options to the WebDriver for headless browsing and a custom user agent.

        Returns:
            Options: WebDriver options.
        """
        self.options.add_argument("--headless")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )
        return self.options


class ProductScraper(BaseScraper):
    """
    Web scraper for product information from a McDonald's menu page.

    Attributes:
        BASE_URL (str): The base URL of the McDonald's menu page.
    """

    BASE_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"

    def _scrape_single_product(self, url: str) -> Product:
        """
        Scrapes product details from a single product page.

        Args:
            url (str): The URL of the product page.

        Returns:
            Product: The scraped product information.
        """
        self.driver.get(url)
        self._click_detail_product_button()

        calories, fats, carbs, proteins = self._get_product_macronutrients()
        unsaturated_fats, sugar, salt, portion = self._get_product_dietary_components()

        return Product(
            name=self._get_product_name(),
            description=self._get_product_description(),
            calories=self._turn_into_float(calories),
            fats=self._turn_into_float(fats),
            carbs=self._turn_into_float(carbs),
            proteins=self._turn_into_float(proteins),
            unsaturated_fats=self._turn_into_float(unsaturated_fats),
            sugar=self._turn_into_float(sugar),
            salt=self._turn_into_float(salt),
            portion=self._turn_into_float(portion),
        )

    @staticmethod
    def _get_product_detail_url(product: WebElement) -> str:
        """
        Extracts the detail URL of a product from the product element.

        Args:
            product (WebElement): The product element.

        Returns:
            str: The detail URL of the product.
        """
        link = product.find_element(By.TAG_NAME, "a")
        return link.get_attribute("href")

    def _click_detail_product_button(self) -> None:
        """
        Clicks on the detail product button to reveal more information.
        """
        wait = WebDriverWait(self.driver, 10)
        detail_info_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "accordion-29309a7a60-item-9ea8a10642-button")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", detail_info_button
        )
        detail_info_button.click()
        time.sleep(1)

    def scrape_all_products(self) -> list[Product]:
        """
        Scrapes information for all products listed on the McDonald's menu page.

        Returns:
            list[Product]: A list of scraped product information.
        """
        self.driver.get(self.BASE_URL)
        products = self.driver.find_elements(By.CLASS_NAME, "cmp-category__item")

        product_detail_urls = [
            self._get_product_detail_url(product) for product in products
        ]
        return [self._scrape_single_product(url) for url in product_detail_urls]

    @staticmethod
    def _turn_into_float(item: str) -> float | None:
        """
        Converts a string to a float value, handling exceptions.

        Args:
            item (str): The string to convert.

        Returns:
            float | None: The converted float value, or None if conversion fails.
        """
        try:
            return float(
                item.replace("г/g", " ")
                .replace("ккал/kcal", " ")
                .replace("мл/ml", " ")
                .split()[0]
            )
        except ValueError:
            return None

    def _get_product_name(self) -> str:
        """
        Retrieves the name of the product.

        Returns:
            str: The name of the product.
        """
        return self.driver.find_element(
            By.CLASS_NAME, "cmp-product-details-main__heading-title"
        ).text

    def _get_product_description(self) -> str:
        """
        Retrieves the description of the product.

        Returns:
            str: The description of the product.
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "cmp-product-details-main__description")
            )
        )
        return self.driver.find_element(
            By.CLASS_NAME, "cmp-product-details-main__description"
        ).text

    def _get_product_macronutrients(self) -> list[str]:
        """
        Retrieves the macronutrients information of the product.
        (calories, fats, carbs, proteins)

        Returns:
            list[str]: The macronutrients information.
        """
        wait = WebDriverWait(self.driver, 5)
        ul_macronutrients = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".cmp-nutrition-summary__heading-primary")
            )
        )

        li_macronutrients = ul_macronutrients.find_elements(By.TAG_NAME, "li")

        return [
            macronutrient.find_element(
                By.CSS_SELECTOR, ".value > span[aria-hidden='true']"
            ).text.strip()
            for macronutrient in li_macronutrients
        ]

    def _get_product_dietary_components(self) -> list[str]:
        """
        Retrieves the dietary components information of the product.
        (unsaturated_fats, sugar, salt, portion)

        Returns:
            list[str]: The dietary components information.
        """
        wait = WebDriverWait(self.driver, 5)
        ul_dietary_components = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "cmp-nutrition-summary__details-column-view-desktop")
            )
        )
        li_dietary_components = ul_dietary_components.find_elements(By.TAG_NAME, "li")[
            :4
        ]
        return [
            " ".join(
                component.find_element(
                    By.CSS_SELECTOR, ".value > span[aria-hidden='true']"
                )
                .get_attribute("innerText")
                .strip()
                .split()
            )
            for component in li_dietary_components
        ]
