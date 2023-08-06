import re
import time

def wrap(cls, *args, **kwargs):
    def inner(*args, **kwargs):
        t_extime = cls()
        ggstart_time = args[0]
        res = t_extime.ext_time(ggstart_time)
        return res

    return inner


def singleton(cls, *args, **kwargs):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@wrap
@singleton

class extime_all(object):
    def __init__(self):
        pass
    def ext_time(self,ggstart_time):
        t1 = ggstart_time
        a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})', t1)

        if a != []:
            y = a[0]
            x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
            return x

        a = re.findall('([1-9][0-9]{3})[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
        if a != []:
            y = a[0]
            x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
            return x

        a = re.findall('^([0-2][0-9])[\-\./\\年]([0-9]{1,2})[\-\./\\月]([0-9]{1,2})', t1)
        if a != []:
            y = a[0]
            x = y[0] + "-" + (y[1] if len(y[1]) == 2 else '0%s' % y[1]) + '-' + (y[2] if len(y[2]) == 2 else '0%s' % y[2])
            x = '20' + x
            return x

        a = re.findall('^(20[0-9]{2})--([0-9]{1,2})-([0-9]{1,2})', t1)

        if a != []:
            x = '-'.join([a[0][0], a[0][1] if a[0][1] != '0' else '1', a[0][2] if a[0][2] != '0' else '1'])

            return x

        if ' CST ' in t1:
            try:
                x = time.strptime(t1, '%a %b %d %H:%M:%S CST %Y')
                x = time.strftime('%Y-%m-%d %H:%M:%S', x)
            except:
                x = ''
            if x != '': return x
        a = re.findall('^(20[0-9]{6})', t1)
        if a != []:
            x = '-'.join([a[0][:4], a[0][4:6], a[0][6:8]])
            return x

        return None

if __name__ == '__main__':
    # extime=extime_all()
    # print(extime.ext_time('2012/1/1'))
    print(extime_all('2012/1/1'))