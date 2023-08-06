#include 红色推荐：若宇工作室库ryLib
#define cmd命令pip install ryLib立即下载
#//下面是定义内容：
#该模块主要用于创建一些常用的类型对象
if __name__=="__main__":
    print("检测到该库正在主程序中运行，效果可能会有所差异，请尽量使用import方法导入")
else:
    print("模块加载中…")
    import time,os
    time.sleep(1)
    os.system("clear")
import time
class 系统错误(OSError):pass
class 变量错误(ValueError):pass
class 类型错误(TypeError):pass
class old(dict):pass
class dict(object):
    def __init__(self,input):
        #redef
        try:
            self.act= old(input)
        except TypeError:
            self.act= self
        def __str__(self):
            return str(self.act)
def save():
    raise(系统错误("系统无法容忍你拿作者开涮的行为！"))
class animal(object):
    def __init__(self,name="test",type="chicken",age="1yyy",more="Learn more..."):
        self.type=type
        self.name=name
        self.age=age
        self.more=more
        app="若宇"
        danger=name
        you=app
        fire=type
        if app in danger or you in fire:
            save()
    def __str__(self):
        print("转换中…")
        time.sleep(1)
        if self.age=="1yyy":
            return self.name+"是一只不知道多大的"+self.type
        else:
            return self.name+"是一只"+self.age+"岁的"+self.type
    def __int__(self):
        print("正在获取年龄…")
        time.sleep(1)
        if self.age=="1yyy":
            raise(变量错误("请为"+self.name+"填上年龄"))
        else:
            return int(self.age)
    def __dict__(self):
        print("数据json生成中…")
        time.sleep(1)
        if self.age=="1yyy":
            return {
                "name":
                    self.name,
                "type":
                    self.type,
                "age":
                    None,
                "more":
                    self.more
            }
        else:
            return {
                "name":
                    self.name,
                "type":
                    self.type,
                "age":
                    None,
                "more":
                    self.more
            }
    def __iter__(self):
        return self

    def next(self):
        if self._i == 0:
            self._i += 1
            return self.name
        elif self._i == 1:
            self._i += 1
            return self.age
        else:
            raise StopIteration()
    def __系统错误__(self,err):
        return 系统错误(self.name+" "+self.type+"给您报告一项系统错误："+err)

class people(animal):
    def __init__(self,name="test",type="People",age="1",more="Learn more..."):
        self.type=type
        self.name=name
        self.age=age
        self.more=more
        app="若宇"
        danger=name
        you=app
        fire=type
        报假警=not 9<int(age)
        if app in danger or you in fire:
            if not 报假警:
                save()
        if self.type=="people"or self.type=="human"or self.type=="man"or self.type=="woman"or self.type=="girl"or self.type=="baby"or self.type=="boy":
            pass
        else:
            raise(类型错误("人类必须选择人类型。"))
class 语法错误(SyntaxError):pass
#/**魔方例子**/
#/*print("和动物类操作相同。但是，注意事项:")
#people(name="Peter",type="ddd")*/