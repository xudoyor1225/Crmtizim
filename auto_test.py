import time
from colorama import init, Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Ranglarni yoqish
init(autoreset=True)

BASE_URL = "http://127.0.0.1:8000"
ADMIN_PHONE = "998900000000"
ADMIN_PASS = "admin"


class RobustTester:
    def __init__(self):
        print(f"{Fore.CYAN}🛡️ MUSTAHKAM TEST BOSHLANDI...{Style.RESET_ALL}")

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Orqa fonda ishlashi uchun
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 3)  # 3 sekund kutadi xolos
        self.errors = []
        self.success_count = 0

    def log_success(self, msg):
        print(f"{Fore.GREEN}✅ [OK] {msg}")
        self.success_count += 1

    def log_fail(self, msg, error_details=""):
        print(f"{Fore.RED}❌ [FAIL] {msg}")
        if error_details:
            print(f"   Original Error: {str(error_details)[:100]}...")  # Xatoni qisqartirib ko'rsatish
        self.errors.append(msg)

    def safe_action(self, description, action_func):
        """
        Xatolik yuz bersa ham dasturni to'xtatmaydigan "Himoya qobig'i"
        """
        try:
            action_func()
            self.log_success(description)
        except Exception as e:
            self.log_fail(description, e)
            # Skrinshot olish (ixtiyoriy)
            # self.driver.save_screenshot(f"error_{int(time.time())}.png")

    # --- ACTIONLAR ---

    def _login(self):
        self.driver.get(f"{BASE_URL}/login/")
        self.driver.find_element(By.NAME, "username").send_keys(ADMIN_PHONE)
        self.driver.find_element(By.NAME, "password").send_keys(ADMIN_PASS)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        if "login" in self.driver.current_url:
            raise Exception("Login url o'zgarmadi")

    def _check_dashboard(self):
        self.driver.get(f"{BASE_URL}/")
        # Sahifada 'Dashboard' yoki 'Xush kelibsiz' so'zi borligini tekshirish
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        if "Xush kelibsiz" not in body_text and "Dashboard" not in body_text:
            raise Exception("Dashboard matni topilmadi")

    def _check_users_page(self):
        self.driver.get(f"{BASE_URL}/users/")
        # Jadval bormi?
        self.driver.find_element(By.TAG_NAME, "table")

    def _check_finance_page(self):
        self.driver.get(f"{BASE_URL}/finance/transactions/")
        self.driver.find_element(By.TAG_NAME, "table")

    def _create_course(self):
        self.driver.get(f"{BASE_URL}/edu/courses/add/")
        self.driver.find_element(By.NAME, "name").send_keys("Test Robust Kurs")
        self.driver.find_element(By.NAME, "price").send_keys("500000")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        if "Test Robust Kurs" not in self.driver.page_source:
            raise Exception("Kurs ro'yxatda ko'rinmadi")

    def _check_dark_mode(self):
        # Tugmani ID orqali topishga harakat qilamiz
        try:
            btn = self.driver.find_element(By.ID, "theme-toggle")
            btn.click()
        except NoSuchElementException:
            # Agar ID bo'lmasa, XPath bilan
            self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'toggleTheme')]").click()

    # --- ASOSIY START ---

    def run(self):
        # 1. Login (Bu eng muhimi, agar bu o'xshmasa qolgani bekor)
        try:
            self._login()
            self.log_success("Tizimga kirish")
        except Exception as e:
            self.log_fail("Tizimga kirish (Critical)", e)
            self.driver.quit()
            return

        # 2. Sahifalarni kezib chiqish (To'xtamasdan)
        steps = [
            ("Dashboard sahifasi", self._check_dashboard),
            ("Foydalanuvchilar sahifasi", self._check_users_page),
            ("Moliya sahifasi", self._check_finance_page),
            ("Kurs yaratish funksiyasi", self._create_course),
            ("Dark Mode tugmasi", self._check_dark_mode),
        ]

        for desc, func in steps:
            self.safe_action(desc, func)

        # Yakuniy hisobot
        print(f"\n{Fore.CYAN}📊 HISOBOT:{Style.RESET_ALL}")
        print(f"Muvaffaqiyatli: {self.success_count}")
        print(f"Xatolar: {len(self.errors)}")

        if self.errors:
            print(f"{Fore.RED}⚠️ TUZATISH KERAK:{Style.RESET_ALL}")
            for err in self.errors:
                print(f" - {err}")
        else:
            print(f"{Fore.GREEN}🎉 AJOYIB! TIZIM BARQAROR ISHLAYAPTI.{Style.RESET_ALL}")

        self.driver.quit()


if __name__ == "__main__":
    tester = RobustTester()
    tester.run()