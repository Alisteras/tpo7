import pytest
import logging
from config.bmc_config import BmcConfig
from services.redfish_service import redfish_service

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def authenticated_session():
    """ 
    Фикстура PyTest для аутентификации перед выполнением тестов. 
    """
    logger.info("Начало аутентификации...")
    
    credentials = BmcConfig.credentials
    response = redfish_service.auth(credentials.login, credentials.password)
    
    assert response.status_code == 201, f"Ошибка аутентификации: {response.status_code}"
    assert 'X-Auth-Token' in response.headers, "Токен аутентификации отсутствует в ответе"
    assert len(response.headers['X-Auth-Token']) > 0, "Токен аутентификации пустой"
    
    logger.info("Аутентификация успешна")
    yield redfish_service
    
    logger.info("Сессия тестов завершена")

class TestRedfishAPI:
    
    def test_authentication_success(self, authenticated_session):  
        """
        создает сессию и убеждается, что токен сессии присутствует в ответе
        """
        credentials = BmcConfig.credentials
        response = redfish_service.auth(credentials.login, credentials.password)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        
        assert 'X-Auth-Token' in response.headers, "Токен аутентификации отсутствует в заголовках"
        assert isinstance(response.headers['X-Auth-Token'], str), "Токен должен быть строкой"
        assert len(response.headers['X-Auth-Token']) > 0, "Токен не должен быть пустым"
        
        logger.info("Тест аутентификации пройден успешно")

    def test_get_system_info(self, authenticated_session):
        """
        GET-запрос на /redfish/v1/Systems/system
        """
        response = redfish_service.get_system_info()

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        
        assert 'PowerState' in data, "Поле PowerState отсутствует в ответе"
        assert isinstance(data['PowerState'], str), "PowerState должен быть строкой"
        assert data['PowerState'] != "", "PowerState не должен быть пустым"
        
        assert 'Status' in data, "Поле Status отсутствует в ответе"
        assert isinstance(data['Status'], dict), "Status должен быть объектом"
        assert 'Health' in data['Status'], "Поле Health отсутствует в Status"
        assert data['Status']['Health'] == 'OK', f"Ожидался Health='OK', получен '{data['Status']['Health']}'"
        
        logger.info("Тест получения информации о системе пройден успешно")

    def test_power_management_on(self, authenticated_session): 
        """
        включение сервера, ответ содержит 204 (No Content)(мол успешно, но данные никакие тебе не отправлю
        """
        response = redfish_service.toggle_server_status('On')
        
        assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"
        
        import time
        time.sleep(2)
        
        redfish_service.toggle_server_status('ForceOff')
        
        logger.info("Тест управления питанием пройден успешно")

    def test_cpu_temperature_empty(self, authenticated_session):
        """
        Проверяет, что массив температур процессора пустой
        Всегда проваливается, т.к. датчиков нет
        (ok, не работало, я умудрился все сделать)
        """
        response = redfish_service.get_thermal_info()
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        
        assert 'TemperatureReadingsCelsius' in data, "Поле TemperatureReadingsCelsius отсутствует в ответе"
        assert isinstance(data['TemperatureReadingsCelsius'], list), "TemperatureReadingsCelsius должен быть массивом"
        assert len(data['TemperatureReadingsCelsius']) == 0, f"Ожидался пустой массив TemperatureReadingsCelsius, получено {len(data['TemperatureReadingsCelsius'])} элементов"
        
        logger.info("Тест температуры CPU пройден успешно")

    def test_cpu_sensors_empty(self, authenticated_session): 
        """
        проверяет, что информация о процессорах отсутствует 
        """
        response = redfish_service.get_processors()

        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        
        assert 'Members' in data, "Поле Members отсутствует в ответе"
        assert isinstance(data['Members'], list), "Members должен быть массивом"
        assert len(data['Members']) == 0, f"Ожидался пустой массив Members, получено {len(data['Members'])} элементов"
        
        logger.info("Тест датчиков CPU пройден успешно")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
