import accounts as login
import employees
import products


def disconnectAll():
    login.disconnect()
    products.disconnect()
    employees.disconnect()
