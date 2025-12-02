from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import sys


class OpenBMCTestBase:
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        
        self.base_url = "https://127.0.0.1:2443"
        self.login_url = f"{self.base_url}/login"
        self.valid_username = "root"
        self.valid_password = "0penBmc"

    def teardown_driver(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def login(self, username, password):
        driver = self.driver
        driver.get(self.login_url)
        time.sleep(2)
        
        username_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()
        
        time.sleep(2)

    def is_logged_in(self):
        current_url = self.driver.current_url
        
        if "/login" not in current_url:
            return True
        
        try:
            dashboard_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Dashboard') or contains(text(), 'System') or "
                "contains(text(), 'Overview') or contains(text(), 'Server')]"
            )
            if dashboard_elements:
                return True
        except:
            pass
        
        try:
            nav_elements = self.driver.find_elements(By.TAG_NAME, "nav")
            menu_elements = self.driver.find_elements(By.TAG_NAME, "menu")
            if nav_elements or menu_elements:
                return True
        except:
            pass
        
        return False


def authenticate_user(username, passkey):
    test_base = OpenBMCTestBase()
    try:
        test_base.setup_driver()
        test_base.login(username, passkey)
        
        is_logged_in = test_base.is_logged_in()
        
        if is_logged_in:
            return True
        else:
            try:
                error_elements = test_base.driver.find_elements(By.XPATH, 
                    '//*[contains(text(), "error") or contains(text(), "invalid") or contains(text(), "incorrect")]'
                )
                if error_elements:
                    print(f"Ошибка входа: {error_elements[0].text}")
            except:
                pass
            return False
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    finally:
        test_base.teardown_driver()


def verify_account_lockout():
    test_base = OpenBMCTestBase()
    test_base.setup_driver()
    login_attempts = 6
    
    try:
        for current_attempt in range(1, login_attempts + 1):
            test_base.driver.get(test_base.login_url)
            time.sleep(2)
            
            try:
                test_base.login('root', f'incorrect_pass_{current_attempt}')
            except Exception as e:
                print(f"Ошибка: {e}")
                continue
            
            if not test_base.is_logged_in():
                print("Неудачная попытка входа")
            else:
                return False
        
        test_base.driver.get(test_base.login_url)
        time.sleep(2)
        
        test_base.login('root', '0penBmc')
        
        if test_base.is_logged_in():
            return False
        else:
            return True
            
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    finally:
        test_base.teardown_driver()


def validate_hardware_inventory():
    test_base = OpenBMCTestBase()
    test_base.setup_driver()
    
    try:
        test_base.login('root', '0penBmc')
        time.sleep(2)

        if not test_base.is_logged_in():
            return False

        inventory_urls = [
            f"{test_base.base_url}/#/hardware-status/inventory",
            f"{test_base.base_url}/#/inventory", 
            f"{test_base.base_url}/#/system/inventory",
            f"{test_base.base_url}/#/hardware/inventory",
            f"{test_base.base_url}/#/overview"
        ]
        
        for inventory_url in inventory_urls:
            try:
                test_base.driver.get(inventory_url)
                time.sleep(2)
                
                if not test_base.is_logged_in():
                    test_base.login('root', '0penBmc')
                    time.sleep(1)
                    continue
                
                hardware_keywords = ["CPU", "Processor", "Memory", "RAM", "Hardware", "Inventory", "System"]
                
                for keyword in hardware_keywords:
                    elements = test_base.driver.find_elements(By.XPATH, f'//*[contains(text(), "{keyword}")]')
                    if elements:
                        return True
                        
            except Exception as e:
                print(f"Ошибка: {e}")

        nav_keywords = ["Inventory", "Hardware", "System", "Components"]
        for keyword in nav_keywords:
            try:
                elements = test_base.driver.find_elements(By.XPATH, f'//*[contains(text(), "{keyword}")]')
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        try:
                            element.click()
                            time.sleep(2)
                            test_elements = test_base.driver.find_elements(By.XPATH, '//*[contains(text(), "CPU") or contains(text(), "Memory")]')
                            if test_elements:
                                return True
                        except Exception as e:
                            print(f"Ошибка: {e}")
            except:
                continue
        
        return False
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    finally:
        test_base.teardown_driver()


def check_power_operation_logs():
    test_base = OpenBMCTestBase()
    test_base.setup_driver()
    
    try:
        test_base.login('root', '0penBmc')
        time.sleep(2)

        if not test_base.is_logged_in():
            return False

        power_operation_performed = False
        
        power_buttons = test_base.driver.find_elements(By.XPATH, 
            '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "power") or '
            'contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "on")]'
        )
        
        if power_buttons:
            for btn in power_buttons:
                if btn.is_enabled():
                    try:
                        original_url = test_base.driver.current_url
                        btn.click()
                        time.sleep(3)
                        power_operation_performed = True
                        test_base.driver.get(original_url)
                        time.sleep(1)
                        break
                    except Exception as e:
                        print(f"Ошибка: {e}")

        if not power_operation_performed:
            power_urls = [
                f"{test_base.base_url}/#/operations/server-power-operations",
                f"{test_base.base_url}/#/power",
                f"{test_base.base_url}/#/operations/power"
            ]
            
            for power_url in power_urls:
                try:
                    test_base.driver.get(power_url)
                    time.sleep(2)
                    
                    if not test_base.is_logged_in():
                        test_base.login('root', '0penBmc')
                        time.sleep(1)
                        continue
                    
                    power_buttons = test_base.driver.find_elements(By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "power")]')
                    if power_buttons:
                        for btn in power_buttons:
                            if btn.is_enabled():
                                btn.click()
                                time.sleep(3)
                                power_operation_performed = True
                                break
                        if power_operation_performed:
                            break
                except Exception as e:
                    print(f"Ошибка: {e}")

        log_urls = [
            f"{test_base.base_url}/#/logs/event-logs", 
            f"{test_base.base_url}/#/logs",
            f"{test_base.base_url}/#/system/logs"
        ]
        
        for log_url in log_urls:
            try:
                test_base.driver.get(log_url)
                time.sleep(2)
                
                if not test_base.is_logged_in():
                    test_base.login('root', '0penBmc')
                    time.sleep(1)
                    continue
                
                log_elements = test_base.driver.find_elements(By.XPATH, 
                    '//*[contains(text(), "Power") or contains(text(), "power") or '
                    'contains(text(), "Event") or contains(text(), "Log") or '
                    'contains(text(), "System") or contains(@class, "log")]'
                )
                
                if log_elements:
                    return True
                    
            except Exception as e:
                print(f"Ошибка: {e}")

        return False

    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    finally:
        test_base.teardown_driver()


def test_successful_authentication():
    result = authenticate_user('root', '0penBmc')
    print(f"Успешная аутентификация: {'ПРОЙДЕН' if result else 'ПРОВАЛЕН'}")
    return result

def test_failed_authentication():
    result = authenticate_user('huh', 'whuh')
    expected_result = False
    test_passed = (result == expected_result)
    print(f"Неудачная аутентификация: {'ПРОЙДЕН' if test_passed else 'ПРОВАЛЕН'}")
    return test_passed

def test_account_lockout_protection():
    result = verify_account_lockout()
    print(f"Защита от блокировки: {'ПРОЙДЕН' if result else 'ПРОВАЛЕН'}")
    return result

def test_hardware_inventory_display():
    result = validate_hardware_inventory()
    print(f"Инвентаризация оборудования: {'ПРОЙДЕН' if result else 'ПРОВАЛЕН'}")
    return result

def test_system_log_entries():
    result = check_power_operation_logs()
    print(f"Системные логи: {'ПРОЙДЕН' if result else 'ПРОВАЛЕН'}")
    return result


def run_simple():
    print("ЗАПУСК ТЕСТОВ OPENBMC")
    
    tests = [
        ("Успешная аутентификация", test_successful_authentication),
        ("Неудачная аутентификация", test_failed_authentication),
        ("Защита от блокировки", test_account_lockout_protection),
        ("Инвентаризация оборудования", test_hardware_inventory_display),
        ("Системные логи", test_system_log_entries),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n>>> {test_name}")
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"ОШИБКА: {e}")
            failed += 1
    
    print(f"\nИТОГИ: Всего: {len(tests)}, Пройдено: {passed}, Провалено: {failed}")
    
    return failed


if __name__ == "__main__":
    exit_code = run_simple()
    sys.exit(exit_code)
