"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


cart = Cart()


@pytest.fixture(scope='function')
def list_of_products():
    book = Product("book", 100, "This is a book", 1000)
    pen = Product('pen', 15, 'This is pen', 500)
    pencil = Product('pencil', 5.5, 'This is pencil', 500)
    return {'book': book, 'pen': pen, 'pencil': pencil}


@pytest.fixture(scope='function')
def cart_with_products(list_of_products):
    cart.add_product(list_of_products['book'], 10)
    cart.add_product(list_of_products['pen'], 20)
    cart.add_product(list_of_products['pencil'], 15)
    return cart


@pytest.fixture(scope='function')
def cart_with_more_products_than_available(list_of_products, cart_with_products):
    cart.products[list_of_products['book']] = 1001
    cart.products[list_of_products['pen']] = 501
    cart.products[list_of_products['pencil']] = 550


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, list_of_products):
        # TODO напишите проверки на метод check_quantity

        assert list_of_products['book'].check_quantity(500)
        assert list_of_products['book'].check_quantity(999)
        assert list_of_products['book'].check_quantity(1000)
        assert not list_of_products['book'].check_quantity(1001)
        assert not list_of_products['book'].check_quantity(1500)

    def test_product_buy(self, list_of_products):
        # TODO напишите проверки на метод buy

        list_of_products['book'].buy(1)
        list_of_products['pen'].buy(250)
        list_of_products['pencil'].buy(500)

        assert list_of_products['book'].quantity == 999
        assert list_of_products['pen'].quantity == 250
        assert list_of_products['pencil'].quantity == 0

    @pytest.mark.parametrize("param", [1001, 1500])
    def test_product_buy_more_than_available(self, list_of_products, param):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError):
            list_of_products['book'].buy(param)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, list_of_products):
        cart.add_product(list_of_products['book'])
        cart.add_product(list_of_products['pen'], 3)
        cart.add_product(list_of_products['pen'], 4)
        cart.add_product(list_of_products['pencil'], 10)

        assert cart.products[list_of_products['book']] == 1
        assert cart.products[list_of_products['pen']] == 7
        assert cart.products[list_of_products['pencil']] == 10

    def test_cart_remove_product(self, cart_with_products, list_of_products):
        cart.remove_product(list_of_products['book'], 1)
        cart.remove_product(list_of_products['pen'], 1)
        cart.remove_product(list_of_products['pen'], 2)
        cart.remove_product(list_of_products['pencil'], 14)

        assert cart.products[list_of_products['book']] == 9
        assert cart.products[list_of_products['pen']] == 17
        assert cart.products[list_of_products['pencil']] == 1

    def test_cart_remove_product_not_in_cart(self, cart_with_products, list_of_products):
        cart.remove_product(list_of_products['book'], 10)
        cart.remove_product(list_of_products['pen'], 21)
        cart.remove_product(list_of_products['pencil'])

        assert list_of_products['book'] not in cart.products
        assert list_of_products['pen'] not in cart.products
        assert list_of_products['pencil'] not in cart.products

        with pytest.raises(KeyError):
            cart.remove_product(list_of_products['book'])
        with pytest.raises(KeyError):
            cart.remove_product(list_of_products['pen'])
        with pytest.raises(KeyError):
            cart.remove_product(list_of_products['pencil'])

    def test_cart_clear(self, cart_with_products):
        cart.clear()

        assert cart.products == {}

    def test_cart_get_total_price(self, cart_with_products):
        assert cart.get_total_price() == 1382.5

    def test_cart_buy(self, cart_with_products, list_of_products):
        cart.buy()

        assert cart.products == {}
        assert list_of_products['book'].quantity == 990
        assert list_of_products['pen'].quantity == 480
        assert list_of_products['pencil'].quantity == 485

    def test_cart_buy_more_than_available(self, cart_with_more_products_than_available):
        with pytest.raises(ValueError):
            cart.buy()
