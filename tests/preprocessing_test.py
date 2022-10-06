import pytest
from src.domain import preprocessing

# Given tworzy sekcję w której tworzymy założenia początkowe. Ustawiamy stan systemu (zwany również stanem świata) na potrzebny do testów.
# When w tej sekcji wykonujemy akcję którą chcemy testować.
# Then wykonujemy sprawdzenia czy aplikacja zachowała się zgodnie z oczekiwaniami. Najczęściej poprzez wykorzystanie asercji lub interakcji z mockami


@pytest.mark.parametrize(
    ["inp_string", "expected"],
    [
        ["<span>Karolcia</span>", "Karolcia"],
        ["<span>Obudź w sobie Olbrzyma</span>", "Obudź w sobie Olbrzyma"],
        ["<span>Zapach Szkła</span>", "Zapach Szkła"],
        [
            "<span>Invictus. Audioserial <i>9</i></span>",
            "Invictus. Audioserial odcinek: 9",
        ],
    ],
)
def test_extract_title_from_string_shuld_return_expected_string(inp_string, expected):
    result = preprocessing.extract_title_from_string(inp_string)
    assert result == expected
