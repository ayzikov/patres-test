# Тесты для проверки JWT
def test_all_books(test_app):
    """ Эндпоинт без авторизации """
    response = test_app.get("/books")
    assert response.status_code == 200


def test_book(test_app):
    """ Эндпоинт с авторизации """
    response = test_app.get("/books/1")
    assert response.status_code == 401