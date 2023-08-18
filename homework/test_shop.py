"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


CART = Cart()


@pytest.fixture(scope='function')
def list_of_products():
    book = Product("book", 100, "This is a book", 1000)
    pen = Product('pen', 15, 'This is pen', 500)
    pencil = Product('pencil', 5.5, 'This is pencil', 500)
    return {'book': book, 'pen': pen, 'pencil': pencil}


@pytest.fixture(scope='function')
def cart_with_products(list_of_products):
    CART.add_product(list_of_products['book'], 10)
    CART.add_product(list_of_products['pen'], 20)
    CART.add_product(list_of_products['pencil'], 15)
    return CART


@pytest.fixture(scope='function')
def cart_with_more_products_than_available(list_of_products, cart_with_products):
    CART.products[list_of_products['book']] = 1001
    CART.products[list_of_products['pen']] = 501
    CART.products[list_of_products['pencil']] = 550


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
        CART.add_product(list_of_products['book'])
        CART.add_product(list_of_products['pen'], 3)
        CART.add_product(list_of_products['pen'], 4)
        CART.add_product(list_of_products['pencil'], 10)

        assert CART.products[list_of_products['book']] == 1
        assert CART.products[list_of_products['pen']] == 7
        assert CART.products[list_of_products['pencil']] == 10

    def test_cart_remove_product(self, cart_with_products, list_of_products):
        CART.remove_product(list_of_products['book'], 1)
        CART.remove_product(list_of_products['pen'], 1)
        CART.remove_product(list_of_products['pen'], 2)
        CART.remove_product(list_of_products['pencil'], 14)

        assert CART.products[list_of_products['book']] == 9
        assert CART.products[list_of_products['pen']] == 17
        assert CART.products[list_of_products['pencil']] == 1

    def test_cart_remove_product_not_in_cart(self, cart_with_products, list_of_products):
        CART.remove_product(list_of_products['book'], 10)
        CART.remove_product(list_of_products['pen'], 21)
        CART.remove_product(list_of_products['pencil'])

        with pytest.raises(KeyError):
            CART.remove_product(list_of_products['book'])
        with pytest.raises(KeyError):
            CART.remove_product(list_of_products['pen'])
        with pytest.raises(KeyError):
            CART.remove_product(list_of_products['pencil'])

    def test_cart_clear(self, cart_with_products):
        CART.clear()

        assert CART.products == {}

    def test_cart_get_total_price(self, cart_with_products):
        assert CART.get_total_price() == 1382.5

    def test_cart_buy(self, cart_with_products, list_of_products):
        CART.buy()

        assert list_of_products['book'].quantity == 990
        assert list_of_products['pen'].quantity == 480
        assert list_of_products['pencil'].quantity == 485

    def test_cart_buy_more_than_available(self, cart_with_more_products_than_available):
        with pytest.raises(ValueError):
            CART.buy()
