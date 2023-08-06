import datetime
import random
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd
from loguru import logger
from scipy import optimize as sco
from sklearn import metrics

###############################################################################
# utility
###############################################################################


def read_csv(
    fpath: str, index_col: Optional[int] = 0, parse_dates: bool = True
) -> pd.DataFrame:
    return pd.read_csv(fpath, index_col=index_col, parse_dates=parse_dates)


def write_csv(df: pd.DataFrame, fpath: str) -> None:
    df.to_csv(fpath)


def drop_weekends(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.index.dayofweek < 5]


def random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def sco_minimize(*args: Any, **kwargs: Any) -> Any:
    res = sco.minimize(*args, **kwargs)
    if res.success:
        return res.x
    assert False


def div(dividend: Any, divisor: Any) -> Any:
    if divisor == 0:
        return 0
    else:
        return dividend / divisor


def confusion_matrix(
    y_true: npt.NDArray[Any],
    y_pred: npt.NDArray[Any],
) -> Tuple[int, int, int, int]:
    assert y_true.ndim == 1 and y_pred.ndim == 1
    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp


def debug_confusion_matrix(tn: int, fp: int, fn: int, tp: int) -> None:
    ap = tp + fn
    an = fp + tn
    pp = tp + fp
    pn = fn + tn
    al = ap + an
    logger.debug("tp fn ap %d %d %d" % (tp, fn, ap))
    logger.debug("fp tn an %d %d %d" % (fp, tn, an))
    logger.debug("pp pn al %d %d %d" % (pp, pn, al))
    logger.debug("accuracy %f" % div(tp + tn, al))
    logger.debug("tp/pp %f" % div(tp, pp))
    logger.debug("tn/pn %f" % div(tn, pn))
    logger.debug("tp/ap %f" % div(tp, ap))
    logger.debug("tn/an %f" % div(tn, an))
    logger.debug("f-score %f" % div(2 * tp, 2 * tp + fp + fn))


###############################################################################
# datetime
###############################################################################


def date(year: int, month: int, day: int) -> datetime.date:
    return datetime.date(year, month, day)


def date_today() -> datetime.date:
    """
    Return the current local date.
    """
    return datetime.date.today()


def date_add(d: datetime.date, days: int) -> datetime.date:
    """
    days range: -999999999 <= days <= 999999999
    """
    return d + datetime.timedelta(days=days)


def date_weekday(d: datetime.date) -> int:
    """
    Return the day of the week as an integer, Monday is 0 and Sunday is 6.
    """
    return d.weekday()


def date_is_weekend(d: datetime.date) -> bool:
    return date_weekday(d) > 4


def date_str(d: datetime.date) -> str:
    """
    Return a string representing the date in ISO 8601 format, YYYY-MM-DD.
    """
    return d.isoformat()


def date_from_str(datestr: str, fmt: str = "%Y-%m-%d") -> datetime.date:
    return datetime.datetime.strptime(datestr, fmt).date()


def datetime_now() -> datetime.datetime:
    """
    Return the current local datetime.
    """
    return datetime.datetime.now()


###############################################################################
# technical analysis
###############################################################################


def risk(
    df: pd.DataFrame,
    o: str,
    h: str,
    l: str,
    c: str,
    window: int = 20,
    ann_factor: int = 252,
) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["O"] = df[o]
    df1["H"] = df[h]
    df1["L"] = df[l]
    df1["C"] = df[c]
    df1["C1"] = df1["C"].shift()
    df1["TR_HL"] = np.abs(df1["H"] - df1["L"])
    df1["TR_HC"] = np.abs(df1["H"] - df1["C1"])
    df1["TR_LC"] = np.abs(df1["L"] - df1["C1"])
    df1["TR"] = df1[["TR_HL", "TR_HC", "TR_LC"]].max(axis=1, skipna=False)
    df1["ATR"] = df1["TR"].rolling(window).mean()
    df1["PATR"] = df1["ATR"] / df1["C"]
    df1["SR_OC"] = df1["O"] / df1["C1"] - 1
    df1["SR_CO"] = df1["C"] / df1["O"] - 1
    df1["SR_CC"] = df1["C"].pct_change()
    df1["LR_OC"] = np.log(1 + df1["SR_OC"])
    df1["LR_CO"] = np.log(1 + df1["SR_CO"])
    df1["LR_CC"] = np.log(1 + df1["SR_CC"])
    df1["HVOL"] = df1["LR_CC"].rolling(window).std() * np.sqrt(ann_factor)
    return df1


def ma(df: pd.DataFrame, c: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["C"] = df[c]
    for t in terms:
        st = str(t)
        df1[st] = df1["C"].rolling(t).mean()
    return df1


def ema(df: pd.DataFrame, c: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["C"] = df[c]
    for t in terms:
        st = str(t)
        df1[st] = df1["C"].ewm(span=t, adjust=False).mean()
    return df1


def high(df: pd.DataFrame, h: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["H"] = df[h]
    for t in terms:
        st = str(t)
        df1[st] = df1["H"].rolling(t).max()
    return df1


def low(df: pd.DataFrame, l: str, terms: List[int]) -> pd.DataFrame:
    df1 = pd.DataFrame()
    df1["L"] = df[l]
    for t in terms:
        st = str(t)
        df1[st] = df1["L"].rolling(t).min()
    return df1


###############################################################################
# portfolio metric
###############################################################################


def sr2lr(sr: Any) -> Any:
    return np.log(1 + sr)


def lr2sr(lr: Any) -> Any:
    return np.exp(lr) - 1


def lr_cum(lr: npt.NDArray[Any]) -> npt.NDArray[Any]:
    assert lr.ndim == 1
    return np.cumsum(lr)


def lr_mean(lr: npt.NDArray[Any], ann_factor: int = 252) -> float:
    assert lr.ndim == 1
    return float(np.mean(lr) * ann_factor)


def lr_vol(lr: npt.NDArray[Any], ann_factor: int = 252) -> float:
    assert lr.ndim == 1
    return float(np.std(lr, ddof=1) * np.sqrt(ann_factor))


def lr_sharpe(lr: npt.NDArray[Any], ann_factor: int = 252) -> float:
    assert lr.ndim == 1
    m = lr_mean(lr, ann_factor=ann_factor)
    v = lr_vol(lr, ann_factor=ann_factor)
    return float(div(m, v))


def lr_mdd(lr: npt.NDArray[Any]) -> float:
    assert lr.ndim == 1
    lr0 = np.concatenate(([0], lr))
    cum = lr_cum(lr0)
    peak = np.maximum.accumulate(cum)
    dd = cum - peak
    mdd = np.min(dd)
    return float(mdd)


def lr_analysis(
    lr: npt.NDArray[Any],
    column_name: str,
    ann_factor: int,
) -> pd.DataFrame:
    assert lr.ndim == 1
    n = lr.shape[0]
    c = lr_cum(lr)[-1]
    c_sr = lr2sr(c)
    m = lr_mean(lr, ann_factor=ann_factor)
    m_sr = lr2sr(m)
    if n > 1:
        v = lr_vol(lr, ann_factor=ann_factor)
        v_sr = lr_vol(lr2sr(lr), ann_factor=ann_factor)
        sharpe = div(m, v)
        sharpe_sr = div(m_sr, v_sr)
    else:
        v = np.nan
        v_sr = np.nan
        sharpe = np.nan
        sharpe_sr = np.nan
    mdd = lr_mdd(lr)
    mdd_sr = lr2sr(mdd)
    mar = div(m, np.abs(mdd))
    mar_sr = div(m_sr, np.abs(mdd_sr))
    index = [
        "lr_cum",
        "lr_ann_mean",
        "lr_ann_vol",
        "lr_ann_sharpe",
        "lr_mdd",
        "lr_mar",
        "sr_cum",
        "sr_ann_mean",
        "sr_ann_vol",
        "sr_ann_sharpe",
        "sr_mdd",
        "sr_mar",
    ]
    data = [
        c,
        m,
        v,
        sharpe,
        mdd,
        mar,
        c_sr,
        m_sr,
        v_sr,
        sharpe_sr,
        mdd_sr,
        mar_sr,
    ]
    df = pd.DataFrame(data=data, index=index)
    df.columns = [column_name]
    return df


def lr_analysis_terms(
    lr: npt.NDArray[Any], kvs: Dict[str, int], ann_factor: int
) -> pd.DataFrame:
    assert lr.ndim == 1
    n = lr.shape[0]
    dfo = pd.DataFrame()
    for key, term in kvs.items():
        if term <= n:
            dfi = lr_analysis(lr[-term:], key, ann_factor)
            dfo = pd.concat([dfo, dfi], axis=1)
        else:
            dfo[key] = np.nan
    return dfo


def lr_analysis_dterms(lr: npt.NDArray[Any]) -> pd.DataFrame:
    assert lr.ndim == 1
    ann_factor = 252
    D = 1
    W = 5
    M = 21
    Y = M * 12
    n = lr.shape[0]
    kvs = {
        "1D": 1 * D,
        "2D": 2 * D,
        "1W": 1 * W,
        "2W": 2 * W,
        "1M": 1 * M,
        "3M": 3 * M,
        "6M": 6 * M,
        "1Y": 1 * Y,
        "3Y": 3 * Y,
        "5Y": 5 * Y,
        "10Y": 10 * Y,
        "ITD": n,
    }
    return lr_analysis_terms(lr, kvs, ann_factor)


def lr_analysis_mterms(lr: npt.NDArray[Any]) -> pd.DataFrame:
    assert lr.ndim == 1
    ann_factor = 12
    M = 1
    Y = M * 12
    n = lr.shape[0]
    kvs = {
        "1M": 1 * M,
        "3M": 3 * M,
        "6M": 6 * M,
        "1Y": 1 * Y,
        "3Y": 3 * Y,
        "5Y": 5 * Y,
        "10Y": 10 * Y,
        "ITD": n,
    }
    return lr_analysis_terms(lr, kvs, ann_factor)


def analysis_dterms(price: npt.NDArray[Any]) -> pd.DataFrame:
    assert price.ndim == 1
    lr = np.log(price[1:] / price[:-1])
    return lr_analysis_dterms(lr)


def analysis_mterms(price: npt.NDArray[Any]) -> pd.DataFrame:
    assert price.ndim == 1
    lr = np.log(price[1:] / price[:-1])
    return lr_analysis_mterms(lr)


def make_portfolio(
    price: npt.NDArray[Any], weight: npt.NDArray[Any], fee_rate: float
) -> npt.NDArray[Any]:
    assert price.ndim == 2 and weight.ndim == 2 and price.shape == weight.shape

    nr, nc = price.shape
    nav = 1
    position_quantity = np.zeros(nc)
    cash = 1

    navs = np.zeros(nr)
    for i in range(nr):
        pi = price[i]
        wi = weight[i]
        nav = cash + np.sum(position_quantity * pi)
        if not np.any(np.isnan(wi)):
            target_position_dollar = nav * wi
            target_position_quantity = target_position_dollar / pi
            trading_position_quantity = (
                target_position_quantity - position_quantity
            )
            trading_position_dollar = trading_position_quantity * pi
            trading_fee = np.sum(np.abs(trading_position_dollar)) * fee_rate
            nav = (
                cash
                - np.sum(trading_position_dollar)
                + np.sum(target_position_dollar)
                - trading_fee
            )
            position_dollar = nav * wi
            position_quantity = position_dollar / pi
            cash = nav - np.sum(position_dollar)
        navs[i] = nav
    return navs
