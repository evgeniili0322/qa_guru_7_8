"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


CART = Cart()


@pytest.fixture
def list_of_products():
    book = Product("book", 100, "This is a book", 1000)
    pen = Product('pen', 15, 'This is pen', 500)
    pencil = Product('pencil', 10, 'This is pencil', 500)
    return {'book': book, 'pen': pen, 'pencil': pencil}


@pytest.fixture()
def cart_with_products(list_of_products):
    CART.add_product(list_of_products['book'], 10)
    CART.add_product(list_of_products['pen'], 20)
    CART.add_product(list_of_products['pencil'], 15)
    return CART


def after_buy_quantity(product, quantity):
    product.buy(quantity)
    return product.quantity


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

        assert after_buy_quantity(list_of_products['book'], 1) == 999
        assert after_buy_quantity(list_of_products['book'], 500) == 499
        assert after_buy_quantity(list_of_products['book'], 499) == 0

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
        CART.add_product(list_of_products['pen'])
        CART.add_product(list_of_products['pen'], 2)
        CART.add_product(list_of_products['pencil'], 10)

        assert CART.products[list_of_products['book']] == 1
        assert CART.products[list_of_products['pen']] == 3
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
            print(CART.products[list_of_products['book']])
        with pytest.raises(KeyError):
            print(CART.products[list_of_products['pen']])
        with pytest.raises(KeyError):
            print(CART.products[list_of_products['pencil']])

    def test_cart_clear(self, cart_with_products):
        CART.products.clear()
        assert CART.products == {}
