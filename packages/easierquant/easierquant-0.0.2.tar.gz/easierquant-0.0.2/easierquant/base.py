import tushare as ts

def get_tushare_api():
    ts.set_token('6742860fc59b2b510d5894c24385053ab0e03fc595b4d9ff38586333')
    pro = ts.pro_api()
    return pro

def get_tushare():
    ts.set_token('6742860fc59b2b510d5894c24385053ab0e03fc595b4d9ff38586333')
    return ts
    


