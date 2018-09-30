import os
import time,datetime
import json
from typing import Set

ping_result = 0
network_result = 0


def ping_qq():
    result = os.system('ping www.qq.com -n 3')
    if result == 0:
        print('network is connected')
    else:
        print('network disconnected')
    return result

if __name__ == '__main__':
    lt = datetime.datetime
    day_record = lt.now().day
    day = '{}_{}_{}'.format(lt.now().year, lt.now().month, lt.now().day)
    con_dict = {day: []}
    while True:
        lt = datetime.datetime.now()
        if lt.minute ==0 or lt.minute ==30:
            start_time = time.time()
            ping_result = ping_qq()
            print(time.time()-start_time)
            if ping_result == 0:
                con_dict[day].append({'{}_{}'.format(lt.hour,lt.minute):1})
                print('OK')
            else:
                con_dict[day].append({'{}_{}'.format(lt.hour, lt.minute):0})
                print('disconnected')
            if lt.day-day_record:
                day_record = lt.day
                with open("./log/record.json", "r+") as dump_f:
                    dump_f.readline()
                    json.dump(con_dict, dump_f)
                    dump_f.write('\n')
                    dump_f.close()
                day = '{}_{}_{}'.format(lt.year, lt.month, lt.day)
                con_dict = {day:[]}
        while datetime.datetime.now().minute == lt.minute:
            time.sleep(1)
        time.sleep(30)




