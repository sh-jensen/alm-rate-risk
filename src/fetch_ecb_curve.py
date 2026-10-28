import io
import pandas as pd
import requests

BASE = "https://data-api.ecb.europa.eu/service/data/YC"
KEY = "B.U2.EUR.4F.G_N_A.SV_C_YM.SR_{mat}"
MATURITIES = ["3M", "6M", "1Y", "2Y", "5Y", "7Y", "10Y", "20Y", "30Y"]

def fetch_one(mat: str) -> pd.DataFrame:
    r = requests.get(f"{BASE}/{KEY.format(mat=mat)}",
                     params={"lastNObservations": 1, "format": "csvdata"},
                     timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    return df[["DATA_TYPE_FM", "TIME_PERIOD", "OBS_VALUE"]]

def fetch_spot_latest() -> pd.DataFrame:
    return pd.concat([fetch_one(m) for m in MATURITIES], ignore_index=True)

if __name__ == "__main__":
    print(fetch_spot_latest().to_string(index=False))
