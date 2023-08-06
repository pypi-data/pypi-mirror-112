import tushare as ts

def get_tushare_api():
    ts.set_token('c4010d5477cd21b532ca42d8c151d433dde1316cafc3d398f0334361')
    pro = ts.pro_api()
    return pro


