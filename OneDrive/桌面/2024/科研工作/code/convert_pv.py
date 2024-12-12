from pcaspy import Driver, SimpleServer

# 定义 PV 名称和属性
pvDB = {
    'test:pv': {
        'prec': 3,       # 精度 (小数点位数)
        'unit': 'C',     # 单位
        'type': 'float', # 数据类型
        'value': 25.0,   # 初始值
    },
}

class MyDriver(Driver):
    def __init__(self):
        super().__init__()

    def write(self, reason, value):
        if reason in self.pvDB:
            self.setParam(reason, value) 
            print(f"PV {reason} updated to {value}")
            return True
        return False


if __name__ == '__main__':
    server = SimpleServer()
    server.createPV('mypv:', pvDB)  
    
    driver = MyDriver()

    print("EPICS PV Server is running...")
    while True:
        server.process(0.1)  
