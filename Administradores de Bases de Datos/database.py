import accounts as login
import products


def disconnectAll():
    login.disconnect()
    products.disconnect()
