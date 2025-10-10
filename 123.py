class A:
    def greet(self):
        print("Hello from A")

class B:
    def __init__(self, a_sub):
        self.a = a_sub  # 建立 A 的實例

    def call_a(self):
        self.a.greet()  # 呼叫 A 的方法

a = A()
b = B(a)
b.call_a()