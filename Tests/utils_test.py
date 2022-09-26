import pytest
import Utils

def test_interval_to_seconds():
    values = {
        'm':60,
        'H':60*60,
        'D':60*60*24,
        'W':60*60*24*7,
        'M':60*60*24*7*4,
        'Y':60*60*24*365
    }

    valid_test = ['1m','50m','120m','5H','30H','2D','10D','1W','50W','1000W','1Y','5Y','1000Y']
    invalid_test = ['0m','0D','0W','1s','0.5H','0.1D','A','500000']

    for val in valid_test:
        assert Utils.interval_to_seconds(val), 'The function did return an error upon valid interval string.'

    for val in invalid_test:
        with pytest.raises(ValueError):
            Utils.interval_to_seconds(val)

def test_stylize():
    with pytest.raises(ValueError):
        Utils.stylize('test','invalid')
    src = 'test'
    assert Utils.stylize(src,'bold') == f'\033[1m{src}\033[0m'