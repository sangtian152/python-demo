import json


# 读取测试数据
def get_data():
    result = []
    with open("json/login.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for d in data:
            username = d.get("username")
            password = d.get("password")
            expect = d.get("expect")
    with open("json/sql.json", "r", encoding="utf-8") as s:
        data1 = json.load(s)
        for d in data1:
            host = d.get("host")
            user = d.get("user")
            paword = d.get("paword")
            db = d.get("db")
            port = d.get("port")
            charset = d.get("charset")
            # sql = d.get("sql")
            # sql1 = d.get("sql1")
    result.append((username, password, expect, host, user, paword, db, port, charset))
    # 返回构造好的结果列表
    print("构造好的测试数据结果列表:", result)
    # logging.info("构造好的测试数据结果列表:{}".format(result))
    return result


get_data()
