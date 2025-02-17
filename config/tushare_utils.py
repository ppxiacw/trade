import tushare as ts
import pandas as pd
from dto.StockDataDay import StockDataDay
from dto.RealTimeStockData import RealTimeStockData
from datetime import datetime  # 正确导入 datetime 类
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
from dbconfig import engine,db_config

# 获取当前脚本的完整路径
current_path = os.path.abspath(__file__)

# 获取当前脚本的目录
dir_path = os.path.dirname(current_path)

# 获取当前脚本的上级目录
parent_dir_path = os.path.dirname(dir_path)

# 构造相对路径
relative_path = os.path.join(parent_dir_path, 'files')



token  = '410070664c78124d98ca5e81c3921530bd27534856b174c702d698a5'
ts.set_token(token)
pro = ts.pro_api(token)

stock_list = pd.read_csv(f'{relative_path}/stock_list.csv',dtype={'symbol':str})
class IndexAnalysis:
    def __init__(self):
        pass


    @staticmethod
    def get_stock_daily(ts_code, start_date, end_date=None):
        if end_date is None:
            end_date = start_date
        if len(ts_code)==6:
            ts_code = stock_list[stock_list['symbol'] == ts_code]['ts_code'].tolist()[0]
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')
        v= ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
        if v is None or  v.empty:
            return None
        # 将日期列转换为 datetime 类型，并设置为索引
        return StockDataDay.from_daily_dataframe(v)

    @staticmethod
    def calculate_pct(ts_code, start_date, end_date):
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
        change_pct =df['pct_chg'].sum()
        return change_pct

    @staticmethod
    def realtime_quote(ts_code):
        print(ts_code)
        v:pd = ts.realtime_quote(ts_code=ts_code)
        print(v)
        arr = []
        for item in v.iterrows():
            arr.append(RealTimeStockData.from_dataframe(item[1].to_frame().T))
        return arr





# 使用类进行分析
if __name__ == "__main__":

    # 读取原始文件
    all_data = []
    df = pd.read_csv('../files/stock_list_filter.csv', dtype={'symbol': str})
    for i,v in df.iterrows():
        print(v['ts_code'])
        v = ts.pro_bar(ts_code=v['ts_code'], adj='qfq', start_date='20240924', end_date='20250214')
        if not v.empty:  # 检查返回的 DataFrame 是否为空
            v.to_sql(name='market', con=engine, if_exists='append', index=False)




