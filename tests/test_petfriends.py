import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_all_my_pets():
   """Проверяем присутствие всех питомцев пользователя на странице."""
   # Устанавливаем явное ожидание
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//body/div[1]/div[1]/div[1]")))

   # количество питомцев по статистике
   number_stat = int(pytest.driver.find_element(By.XPATH, '//body/div[1]/div/div[1]').text.split()[2])
   print()
   print('количество питомцев по статистике=', str(number_stat))

   # Устанавливаем явное ожидание (ожидаем в течение 10 секунд драйвером driver)
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))

   # Сохраняем в переменную элементы карточек питомцев
   number_pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
   print('количество питомцев в таблице=', len(number_pets))

   assert number_stat == len(number_pets), "Количество питомцев не совпадает со статистикой пользователя"


def test_pets_have_photo():
   """Проверяем наличие фото у всех питомцев пользователя"""
   # активируем неявное ожидание 10sec
   pytest.driver.implicitly_wait(10)

   # количество питомцев пользователя из статистики
   number_stat = int(pytest.driver.find_element(By.XPATH, '//body/div[1]/div/div[1]').text.split()[2])
   print()
   print('количество питомцев по статистике=', str(number_stat))

   # активируем неявное ожидание 10sec
   pytest.driver.implicitly_wait(10)

   # количество карточек без фото
   number_pets_without_photo = len(pytest.driver.find_elements(By.XPATH, '//img[@src=""]'))
   print('количество питомцев без фото=', str(number_pets_without_photo))

   assert (number_stat) == number_pets_without_photo, "Количество питомцев без фото больше общего количества"


def test_all_pets_have_name_ages_breeds():
   """Проверяем наличие имени, породы и возраста у всех питомцев пользователя"""
   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)
   # все имена
   names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')


   # активируем неявное ожидание 5sec
   pytest.driver.implicitly_wait(5)
   # все породы
   breeds = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')

   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)
   # все возрасты
   ages = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')


   for i in range(len(names)):
      print(names[i].text + ',' + breeds[i].text + ',' + ages[i].text)
      assert names[i].text != '', "Не у всех питомцев есть имя"
      assert breeds[i].text != '', "Не у всех питомцев есть порода"
      assert ages[i].text != '', "Не у всех питомцев есть возраст"




def test_duplicate_name():
   """Проверяем отсутствие дубликатов имен у питомцев пользователя"""
   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)

   # все имена
   names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

   # Задаем пустой список и счетчик
   pets_names = []
   r = 0

   # Добавляем имена в список
   for name in names:
      name = name.text
      pets_names.append(name)
      print()
      print(pets_names)
      print('name=', name)

      # проверяем количество питомцев с таким же именем среди уже имеющихся элементов
      # При r != 1 выходим из цикла для быстроты
      r = pets_names.count(name)
      if r != 1:
         break


   # Проверяем, если r == 1, то повторяющихся имен нет.
   assert r == 1, "Есть питомцы с одинаковыми именами"


def test_duplicate_pets():
   """Проверяем отсутствие дубликата питомцев (имя, порода, возраст)"""
   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)
   # все имена
   names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)
   # все породы
   breeds = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')

   # активируем неявное ожидание
   pytest.driver.implicitly_wait(5)
   # все возрасты
   ages = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

   # Создаем пустой список и счетчик
   pets = []
   r = 0
   print()

   for i in range(len(names)):
      # Собираем полученные данные в массив
      pets.append({
         'name': names[i].text,
         'breed': breeds[i].text,
         'age': ages[i].text
      })

      print('pets[', str(i), ']=', pets[i])

      # проверяем количество питомцев с такими же данными среди имеющихся элементов
      # при повторе питомца выходим из цикла для быстроты
      r = pets.count(pets[i])
      print('количество вхождений =', str(r))
      if r != 1:
         break

   assert r == 1, "Есть повторяющиеся питомцы (с одинаковыми именами, породой и возрастом)"