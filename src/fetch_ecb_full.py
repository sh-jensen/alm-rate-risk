import io
from pathlib import Path

import pandas as pd
import requests

BASE = "https://data-api.ecb.europa.eu/service/data/YC"
KEY = "B.U2.EUR.4F.G_N_A.SV_C_YM.{prefix}_{mat}"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def fetch_one(prefix: str, mat: str):
    r = requests.get(f"{BASE}/{KEY.format(prefix=prefix, mat=mat)}",
                     params={"lastNObservations": 1, "format": "csvdata"},
                     timeout=30)
    if r.status_code != 200:
        return None, None
    df = pd.read_csv(io.StringIO(r.text))
    return df["TIME_PERIOD"].iloc[0], df["OBS_VALUE"].iloc[0]


if __name__ == "__main__":
    rows = []
    for n in range(1, 31):
        mat = f"{n}Y"
        spot_date, spot = fetch_one("SR", mat)
        par_date, par = fetch_one("PY", mat)
        print(f"{mat:>4}  spot={spot}  par={par}")
        rows.append({"date": spot_date or par_date, "maturity": mat,
                     "years": n, "spot_pct": spot, "par_pct": par})
    df = pd.DataFrame(rows)
    date = df["date"].dropna().iloc[0]
    path = DATA_DIR / f"ecb_aaa_curve_full_{date}.csv"
    df.to_csv(path, index=False)
    print(f"\nGemt: {path}")