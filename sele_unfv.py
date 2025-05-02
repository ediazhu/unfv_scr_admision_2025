from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import csv

# Ruta al ejecutable de Chromium y ChromeDriver
chromium_path = '/home/eduardo/Programas/scrap_unfv/sele_unfv/chrome-linux/chrome'  # Cambia esto a la ruta de tu ejecutable de Chromium
chromedriver_path = '/home/eduardo/Programas/scrap_unfv/sele_unfv/chromedriver-linux64/chromedriver'  # Cambia esto a la ruta de tu ChromeDriver

# Configuración de opciones para Chromium
options = webdriver.ChromeOptions()
options.binary_location = chromium_path  # Establecer la ubicación del ejecutable de Chromium

# Crear una instancia del servicio de ChromeDriver
service = Service(chromedriver_path)

# Crear una instancia del controlador de Chrome
driver = webdriver.Chrome(service=service, options=options)

# Navegar a la URL deseada
driver.get("https://aplicaciones.unfv.edu.pe/App_Publicador_De_Resultados/")  # Cambia esta URL por la que desees

## Definir el rango de números
start_number = 30000
end_number = 30010  # Cambia este número al final que desees

## Abrir el archivo CSV en modo append
with open('resultados.csv', mode='a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Escribir la cabecera si el archivo está vacío
    if csvfile.tell() == 0:
        csv_writer.writerow(['nombre', 'esc_prof', 'puntaje', 'condicion'])

    # Repetir el proceso para cada número en el rango
    for number in range(start_number, end_number + 1):
        # Localizar el menú desplegable por su ID (cambia 'dropdownId' por el ID real)
        dropdown = driver.find_element(By.ID, "tipoBusqueda")  # Cambia 'dropdownId' por el ID real

        # Crear un objeto Select
        select = Select(dropdown)

        # Seleccionar la segunda opción (índice 1)
        select.select_by_index(1)

        # Localizar el campo de texto por su ID (cambia 'textFieldId' por el ID real)
        text_field = driver.find_element(By.ID, "valorBusqueda")  # Cambia 'textFieldId' por el ID real

        # Ingresar el número en el campo de texto
        text_field.clear()  # Limpiar el campo de texto antes de ingresar un nuevo número
        text_field.send_keys(str(number))

        # Localizar el botón por su ID (cambia 'buttonId' por el ID real)
        button = driver.find_element(By.XPATH, "/html/body/div/main/div/form/div/div[3]/button")  # Cambia 'buttonId' por el ID real

        # Hacer clic en el botón
        button.click()

        # Esperar un momento para ver el resultado
        time.sleep(2)  # Puedes ajustar el tiempo de espera según sea necesario

        # Obtener los valores usando XPath
        nombre = driver.find_element(By.XPATH, '/html/body/div/main/div/div[3]/div/div/div[2]/dl/dd[3]').text  # Cambia 'xpath_del_nombre' por el XPath real
        esc_prof = driver.find_element(By.XPATH, '/html/body/div/main/div/div[3]/div/div/div[2]/dl/dd[4]').text  # Cambia 'xpath_del_esc_prof' por el XPath real
        puntaje = driver.find_element(By.XPATH, '/html/body/div/main/div/div[3]/div/div/div[2]/dl/dd[6]').text  # Cambia 'xpath_del_puntaje' por el XPath real
        condicion = driver.find_element(By.XPATH, '/html/body/div/main/div/div[3]/div/div/div[2]/dl/dd[7]').text  # Cambia 'xpath_del_condicion' por el XPath real

        # Escribir los valores en el archivo CSV
        csv_writer.writerow([nombre, esc_prof, puntaje, condicion])


# Cerrar el navegador
driver.quit()