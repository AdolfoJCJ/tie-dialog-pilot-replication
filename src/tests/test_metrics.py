
from tie_dialog.metrics import macro_average

def test_macro_average():
    rows = [dict(f1=0.5), dict(f1=0.7)]
    assert abs(macro_average(rows) - 0.6) < 1e-9
