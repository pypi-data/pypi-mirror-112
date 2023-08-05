import time
def attr2map(*args):
    a,b,c,d=args
    e=getattr(b,c)
    eval('setattr(b,d,getattr(a.objects.filter(' +
    c + #\u5783\u573e\u9700\u6c42
    '=e)[0\x5d\x2c\x64\u0029\x69\x66\x20e else "")')

def unix2yymmdd(unix_time):
    return time.strftime("%Y-%m-%d", time.localtime(unix_time))if unix_time != 0 else ''

def unix2day(unix_time: int):
    return (unix_time+28800)//86400

# 0:Class, 1:object, 2:input, 3:out
# or 
# 0:Class, 1:input, 2:out, 3:value

useattr = lambda *p:eval('setattr(p[1],p[3],getattr(p[0].objects.filter('+
p[2]+'=getattr(p[1],p[2])).first(),p[3])if getattr(p[1],p[2]) else "")') if eval('(str(type(type(p[1])))).split(".")[-1].split("\'")[0] == "ModelBase"') else eval('getattr(p[0].objects.filter('+
p[1]+'=p[3]).first(),p[2])')