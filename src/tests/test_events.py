
import pandas as pd
from tie_dialog.events import detect_events

def test_detect_events_empty():
    df = pd.DataFrame(dict(dialogue_id=[1,1], turn=[1,2], human_ct=[0.0,0.0], model_ct=[0.0,0.0]))
    ev = detect_events(df, prominence=1.0, min_distance=1)
    assert set(ev.columns)=={'dialogue_id','turn','human_peak','human_valley','machine_peak','machine_valley'}
