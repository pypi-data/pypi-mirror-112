# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2021/1/26 10:39
Desc: 宽客在线-阿尔戈斯全网监控预警系统
https://www.quantinfo.com/Argus/
此接口的目标网站稳定性较差, 可能造成部分时间段无法访问
"""
import pandas as pd
import requests
import urllib3


def watch_argus():
    """
    宽客在线-阿尔戈斯全网监控预警系统
    https://www.quantinfo.com/Argus/
    :return: 阿尔戈斯全网监控预警系统的监控数据
    :rtype: pandas.DataFrame
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://www.quantinfo.com/API/Argus/predict"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    }
    r = requests.get(url, headers=headers, verify=False)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json)
    temp_df["time"] = pd.to_datetime(temp_df["time"], unit="s", utc=True).dt.tz_convert('Asia/Shanghai')
    return temp_df


if __name__ == '__main__':
    watch_argus_df = watch_argus()
    print(watch_argus_df)
