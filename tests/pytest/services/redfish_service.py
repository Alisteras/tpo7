import requests
import logging
from config.bmc_config import BmcConfig
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #игнор SSL сертов

class RedfishService:
    def __init__(self):
        self.base_url = BmcConfig.BASE_URL
        self.session = requests.Session()
        self.session.verify = False  # Игнорируем SSL ошибки для тестов
        self.auth_token = None
        self.logger = logging.getLogger(__name__)

    def auth(self, login: str, password: str) -> requests.Response:
        url = f"{self.base_url}/redfish/v1/SessionService/Sessions"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "UserName": login,
            "Password": password
        }
        
        self.logger.info(f"Аутентификация пользователя: {login}")
        response = self.session.post(url, json=data, headers=headers)
        
        if response.status_code == 201 and 'X-Auth-Token' in response.headers:         # Сохраняем токен аутентификации раз увпешно
            self.auth_token = response.headers['X-Auth-Token']
            self.session.headers.update({'X-Auth-Token': self.auth_token})
        
        return response

    def get_system_info(self) -> requests.Response:
        url = f"{self.base_url}/redfish/v1/Systems/system"
        self.logger.info("Получение информации о системе")
        return self.session.get(url)

    def toggle_server_status(self, reset_type: str) -> requests.Response:
        url = f"{self.base_url}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
        
        data = {
            "ResetType": reset_type # Используем ресет, тк криво работает бмс, нормально не включается, фиксируем попытку запустить
        }
        
        self.logger.info(f"Изменение статуса сервера: {reset_type}")
        return self.session.post(url, json=data)

    def get_thermal_info(self) -> requests.Response:

        url = f"{self.base_url}/redfish/v1/Chassis/chassis/ThermalSubsystem/ThermalMetrics"
        self.logger.info("Получение thermal информации")
        return self.session.get(url)

    def get_processors(self) -> requests.Response:

        url = f"{self.base_url}/redfish/v1/Systems/system/Processors"
        self.logger.info("Получение информации о процессорах")
        return self.session.get(url)

# Создаем экземпляр сервиса для использования в тестах
redfish_service = RedfishService()
