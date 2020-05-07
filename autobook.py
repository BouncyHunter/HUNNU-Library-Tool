import threading
import datetime
import requests
import json
from threading import Timer
from pip._vendor.distlib.compat import raw_input

cookies = {'ASP.NET_SessionId': ' ', 'txw_cookie_txw_unit_Id': ' ',
           'dt_cookie_user_name_remember': ' '}
header_example = {'Host': 'wx.lib.hunnu.edu.cn', 'Accept': 'application/json', 'Origin': 'http://wx.lib.hunnu.edu.cn',
                  'User-Agent': '7.0.5 WindowsWechat'}
data_book = {'data_type': 'seatDate', 'seatno': '2-032', 'seatdate': '2000-04-24', 'datetime': [0,120]}
urls = {'UserInfo': 'http://wx.lib.hunnu.edu.cn/mobile/ajax/user/UserHandler.ashx'}
data_personal = {'data_type': 'user_info'}
booklist = []
converted_date = []
time_avai = datetime.time(6, 59, 50, 0)
time_forb = datetime.time(23, 0, 0, 0)
tick = 0.5
ima = datetime.datetime.now()


class MainThread (threading.Thread):
    global stopp
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        #print(booklist[self.threadID])
        #print(self.threadID)
        if ima.__gt__(converted_date[self.threadID] - datetime.timedelta(minutes=30)):
            del booklist[self.threadID]
            del converted_date[self.threadID]
            return
        try:
            test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                                 data=booklist[self.threadID], cookies=cookies, headers=header_example)
        except:
            print("Booking Error:Connection Failed")
        else:
            test = test.json()
            #print(test)
            if test['code'] == 0:
                print('OK '),
                print(booklist[self.threadID]),
                print(' booked.')
                del booklist[self.threadID]
                del converted_date[self.threadID]





def timer_main():
    global ima
    ima = datetime.datetime.now()
    #print('\n=================================\n')
    #print(ima)
    #print(ima.time() - time_avai)
    if ima.time().__gt__(time_avai) and ima.time().__lt__(time_forb):
        for i in range(0, len(booklist)):
            #print(i)
            MainThread(i, 'whatever', i).start()
    main_timer = Timer(tick, timer_main)
    main_timer.start()




cookies['ASP.NET_SessionId'] = input('ASP.NET_SessionId:')
cookies['txw_cookie_txw_unit_Id'] = input('txw_cookie_txw_unit_Id:')
cookies['dt_cookie_user_name_remember'] = input('dt_cookie_user_name_remember:')

main_timer = Timer(tick, timer_main)
main_timer.start()

print('Checking...')
try:
    cus_info = requests.post(urls['UserInfo'], data=data_personal, cookies=cookies, headers=header_example)
except:
    print("Error:Connection failed.")
else:
    cus_info = cus_info.json()
    if cus_info['code'] == 0:
        print('Signed up.'),
        cus_info = json.loads(cus_info['data'])
        print('Welcome! ' + cus_info['real_name'])
        comm = raw_input('>')
        comm_slice = []
        slice_mark = 0
        for i in range(0, len(comm)):
            if comm[i] == ' ':
                comm_slice.append(comm[slice_mark:i])
                slice_mark = i + 1
        comm_slice.append(comm[slice_mark:len(comm)])
        while comm_slice[0] != 'quit':
            if comm_slice[0] == 'book':
                if len(comm_slice) >= 5:
                    booklist.append({'data_type': 'seatDate', 'seatno': comm_slice[1], 'seatdate': comm_slice[2],
                                     'datetime': [comm_slice[3], comm_slice[4]]})
                    converted_date.append(datetime.datetime.strptime(comm_slice[2], '%Y-%m-%d') +
                                          datetime.timedelta(hours=int(int(comm_slice[3]) / 60),
                                                             minutes=int(comm_slice[3]) % 60))
                else:
                    print('Invalid input')
            elif comm_slice[0] == 'ls':
                for i in booklist:
                    print(i)
                for i in converted_date:
                    print(i)
            elif comm_slice[0] == 'del':
                if len(comm_slice) >= 2:
                    if comm_slice[1] < len(booklist):
                        del booklist[comm_slice[1]]
            elif comm_slice[0] == 'tick':
                if len(comm_slice) >= 2:
                    tick = float(comm_slice[1])
            comm = raw_input('>')
            comm_slice = []
            slice_mark = 0;
            for i in range(0, len(comm)):
                if comm[i] == ' ':
                    comm_slice.append(comm[slice_mark:i])
                    slice_mark = i + 1
            comm_slice.append(comm[slice_mark:len(comm)])