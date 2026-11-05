import pytest

from app.config import to_sqlalchemy_url


@pytest.mark.parametrize("scheme", ["postgres", "postgresql"])
def test_adds_driver_and_keeps_the_rest_of_the_url(scheme: str) -> None:
    url = f"{scheme}://user:pass@host/db?sslmode=require&channel_binding=require"

    assert to_sqlalchemy_url(url) == (
        "postgresql+psycopg://user:pass@host/db?sslmode=require&channel_binding=require"
    )


def test_rejects_a_value_that_is_not_a_url() -> None:
    with pytest.raises(ValueError):
        to_sqlalchemy_url("not-a-url")
