from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from shield34_reporter.model.csv_rows.dynamic_element_locator_csv_row import DynamicElementLocatorCsvRow


def _web_driver_dynamic_find_element(element_locator_alternatives, driver):
    for locator in element_locator_alternatives:
        try:
            web_element = WebDriver.org_find_element(driver, locator.by, locator.expression)
            from shield34_reporter.container.run_report_container import RunReportContainer
            RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(locator.by, locator.expression))
            return web_element, locator.by, locator.expression
        except Exception:
            pass
    return None, None, None


def _web_driver_dynamic_find_elements(element_locator_alternatives, driver):
    for locator in element_locator_alternatives:
        try:
            web_elements = WebDriver.org_find_elements(driver, locator.by, locator.expression)
            if len(web_elements) > 0:
                from shield34_reporter.container.run_report_container import RunReportContainer
                RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(locator.by, locator.expression))
                return web_elements, locator.by, locator.expression
        except Exception:
            pass
    return None, None, None


def _web_element_dynamic_find_element(element_locator_alternatives, parent_web_element):
    for locator in element_locator_alternatives:
        try:
            web_element = WebElement.org_find_element(parent_web_element, locator.by, locator.expression)
            from shield34_reporter.container.run_report_container import RunReportContainer
            RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(locator.by, locator.expression))
            return web_element, locator.by, locator.expression
        except Exception:
            pass
    return None, None, None


def _web_element_dynamic_find_elements(element_locator_alternatives, parent_web_element):
    for locator in element_locator_alternatives:
        try:
            web_elements = WebElement.org_find_element(parent_web_element, locator.by, locator.expression)
            if len(web_elements) > 0:
                from shield34_reporter.container.run_report_container import RunReportContainer
                RunReportContainer.add_report_csv_row(DynamicElementLocatorCsvRow(locator.by, locator.expression))
                return web_elements, locator.by, locator.expression
        except Exception:
            pass
    return None, None, None


def locate_element_by_element_descriptor(driver_or_element, by, value):
    from shield34_reporter.container.run_report_container import RunReportContainer
    current_element_alternatives = RunReportContainer \
        .get_current_block_run_holder() \
        .get_dynamic_element_locator() \
        .current_locator_alternatives(by, locator=value)
    if isinstance(driver_or_element, WebDriver):
        return _web_driver_dynamic_find_element(
            current_element_alternatives, driver_or_element)
    else:
        return _web_element_dynamic_find_element(
            current_element_alternatives, driver_or_element)


def locate_elements_by_element_descriptor(driver_or_element, by, value):
    from shield34_reporter.container.run_report_container import RunReportContainer
    current_element_alternatives = RunReportContainer \
        .get_current_block_run_holder() \
        .get_dynamic_element_locator() \
        .current_locator_alternatives(by, locator=value)
    if isinstance(driver_or_element, WebDriver):
        return _web_driver_dynamic_find_elements(
            current_element_alternatives, driver_or_element)
    else:
        return _web_element_dynamic_find_elements(
            current_element_alternatives, driver_or_element)


def web_element_found(web_element, by, locator):
    from shield34_reporter.container.run_report_container import RunReportContainer
    RunReportContainer \
        .get_current_block_run_holder() \
        .get_dynamic_element_locator() \
        .web_element_found(web_element, by, locator)


def web_elements_found(web_elements, by, locator):
    from shield34_reporter.container.run_report_container import RunReportContainer
    if len(web_elements) > 0:
        RunReportContainer \
            .get_current_block_run_holder() \
            .get_dynamic_element_locator() \
            .web_element_found(web_elements[0], by, locator)
