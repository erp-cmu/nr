import pandas as pd
from nr.nr_utils.checkin import createCheckin


def formatExcelP1(row):
    name = row["ชื่อ-นามสกุล"]
    id = name
    dateStr = row["Date"]
    sp = dateStr.split("/")
    day = sp[0]
    month = sp[1]
    year = int(sp[2])
    times = row.iloc[3:].dropna()
    if len(times) == 0:
        return pd.Series({"name": name, "id": id, "min": pd.NaT, "max": pd.NaT})
    times = times.apply(
        lambda t: pd.to_datetime(f"{year}/{month}/{day} {t}", format="%Y/%m/%d %H:%M")
    )
    res = times.agg(["min", "max"])
    res["name"] = name
    res["id"] = id
    return res


def formatExcelP2(row):
    datas = []
    for i in ["IN", "OUT"]:
        data = {
            "attendance_device_id": row["name"],
            "log_type": i,
            "time": row[i].strftime("%Y/%m/%d %X"),
        }
        datas.append(data)
    return pd.DataFrame.from_records(datas)


def processExcelNakorn(filepath, default_shift_type):
    sheetname = "รายวัน"
    skiprows = 1
    dft = pd.read_excel(filepath, sheet_name=sheetname, skiprows=skiprows)
    df1 = dft.iloc[:, :].apply(formatExcelP1, axis=1)
    df1.dropna(inplace=True)
    df1.rename(columns={"min": "IN", "max": "OUT"}, inplace=True)
    temp = df1.iloc[:, :].apply(formatExcelP2, axis=1)
    df2 = pd.concat(temp.values).reset_index(drop=True)
    df2.apply(
        lambda row: createCheckin(
            **row.to_dict(), default_shift_type=default_shift_type
        ),
        axis=1,
    )
    return df2
