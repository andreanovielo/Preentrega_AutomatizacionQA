import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    yield driver 

    driver.quit()



# Funcion de validacion del login
def test_01_login(driver):
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Validacion de login exitoso verificando que haya redirigido a la pagina del inventario
    assert "/inventory.html" in driver.current_url , f'ERROR: No se redirigió a /inventory.html'



# Validar pagina de inventario
def test_02_verificar_inventario(driver):

    driver.get("https://www.saucedemo.com/inventory.html")

    page_title = driver.title
    section_title = driver.find_element(By.CLASS_NAME, "title").text

    # Verificar que el titulo de la pagina sea correcto
    assert page_title == "Swag Labs", f'ERROR: Se esperaba el titulo "Swag Labs", pero se obtuvo "{page_title}"'

    # Verificar que el titulo de la seccion sea correcto
    assert section_title == "Products", f'ERROR: Se esperaba el titulo "Products", pero se obtuvo "{section_title}"'



# Validar productos visibles
def test_03_productos_visibles(driver):

    inventory_item = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    # [] len() => ver que tan largo es una lista

    # Verificar que en la pagina de inventario haya productos visibles
    assert len(inventory_item) > 0 , f'ERROR: No se encontraron productos visibles'



# Validar elementos de la interfaz: icono de menu y de filtro
def test_04_validad_interfaz(driver):
    menu_button = driver.find_element(By.ID, 'react-burger-menu-btn')
    filtro = driver.find_element(By.CLASS_NAME, 'product_sort_container')

    # Verificar que el boton del menu esté visible
    assert menu_button.is_displayed(), f'ERROR: Menu no esta visible'

    # Verificar que el boton de filtro esté visible
    assert filtro.is_displayed(), f'ERROR: filtro no esta visible'



# Validar la funcion de agregar producto al carrito
def test_05_añadir_producto_al_carrito(driver):
    first_item = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]

    boton_agregar = first_item.find_element(By.TAG_NAME, "button")
    boton_agregar.click()

    # Volver a localizar el botón después del click
    boton_remove = first_item.find_element(By.TAG_NAME, "button")

    # Verificar que cambió a Remove
    assert boton_remove.text == "Remove", f'ERROR: el boton no cambio a "Remove"'



# Validar el contador del carrito
def test_06_verificar_contador_carrito(driver):
    contador_carrito = driver.find_element(By.CLASS_NAME,'shopping_cart_badge').text

    # Verificr que el contador carrito se incremente
    assert contador_carrito == "1" , f'ERROR: Se esperaba 1 , obtuvo {contador_carrito}'



# Validar navegacion por el carrito
def test_07_navegar_carrito(driver):

    driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()

    # Verificar que la pagina actual sea la del carrito
    assert "/cart.html" in driver.current_url , f'ERROR: No se redirigió a /cart.html'



# Validar el producto agregado al carrito
def test_08_comprobar_poducto_en_el_carrito(driver):
    producto_nombre_en_carrito = driver.find_element(By.CLASS_NAME, 'inventory_item_name').text

    # Verificar que el producto en el carrito sea el que se agrego
    assert producto_nombre_en_carrito == 'Sauce Labs Backpack' , f'ERROR: No es el mismo nombre'


    