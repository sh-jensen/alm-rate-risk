import io
from pathlib import Path

import pandas as pd
import requests

BASE = "https://data-api.ecb.europa.eu/service/data/YC"
KEY = "B.U2.EUR.4F.G_N_A.SV_C_YM.{prefix}_{mat}"
YEARS = {"3M": 0.25, "6M": 0.5, "1Y": 1, "2Y": 2, "5Y": 5,
         "7Y": 7, "10Y": 10, "20Y": 20, "30Y": 30}
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def fetch_one(prefix: str, mat: str):
    """Henter seneste observation. prefix: SR = spotrente, PY = par yield."""
    r = requests.get(f"{BASE}/{KEY.format(prefix=prefix, mat=mat)}",
                     params={"lastNObservations": 1, "format": "csvdata"},
                     timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    return df["TIME_PERIOD"].iloc[0], df["OBS_VALUE"].iloc[0]


def fetch_curve() -> pd.DataFrame:
    rows = []
    for mat, years in YEARS.items():
        spot_date, spot = fetch_one("SR", mat)
        par_date, par = fetch_one("PY", mat)
        assert spot_date == par_date, f"Forskellige datoer for {mat}"
        rows.append({"date": spot_date, "maturity": mat, "years": years,
                     "spot_pct": spot, "par_pct": par})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    curve = fetch_curve()
    path = DATA_DIR / f"ecb_aaa_curve_{curve['date'].iloc[0]}.csv"
    curve.to_csv(path, index=False)
    print(curve.to_string(index=False))
    print(f"\nGemt: {path}")