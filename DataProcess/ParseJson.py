import datetime
import pandas as pd
import requests

def get_holidays():
    year = datetime.datetime.now().year.__str__()
    try:
        url = 'https://www.shuyz.com/githubfiles/china-holiday-calender/master/holidayAPI.json'
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError异常
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = None

    if data:
        public_holidays = []
        makeup_workdays = []

        for holiday in data['Years'][year]:
            start_date = holiday['StartDate']
            end_date = holiday['EndDate']
            comp_days = holiday['CompDays']

            # 添加放假日期
            current_date = start_date
            while current_date <= end_date:
                public_holidays.append(current_date)
                current_date = str(pd.to_datetime(current_date) + pd.Timedelta(days=1))[:10]

            # 添加补班日期
            makeup_workdays.extend(comp_days)

        holidays_df = pd.DataFrame(public_holidays, columns=["date"])
        makeup_workdays_df = pd.DataFrame(makeup_workdays, columns=["date"])

        holidays_df.to_csv(f"HolidayData/public_holidays_{year}.csv", index=False, encoding="utf-8")
        makeup_workdays_df.to_csv(f"HolidayData/makeup_workdays_{year}.csv", index=False, encoding="utf-8")
    else:
        raise Exception("获取节假日和补班日期失败，请检查网络连接")