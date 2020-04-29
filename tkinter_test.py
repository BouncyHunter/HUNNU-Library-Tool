import tkinter as tk
from tkinter import StringVar

import requests
import json
import threading
import os
import datetime
from threading import Timer

cookies = {'ASP.NET_SessionId': ' ', 'txw_cookie_txw_unit_Id': ' ',
           'dt_cookie_user_name_remember': ' '}
data_book = {'data_type': 'seatDate', 'seatno': '2-032', 'seatdate': '2000-04-24', 'datetime': [0, 120]}
data_personal = {'data_type': 'user_info'}
data_record = {'page': 1, 'size': 10, 'data_type': 'seat_date_list'}
data_crawl = {'selected_date': '2020-04-24', 'data_type': 'list'}
header_example = {'Host': 'wx.lib.hunnu.edu.cn', 'Accept': 'application/json', 'Origin': 'http://wx.lib.hunnu.edu.cn',
                  'User-Agent': '7.0.5 WindowsWechat'}
urls = {'UserInfo': 'http://wx.lib.hunnu.edu.cn/mobile/ajax/user/UserHandler.ashx'}

crawl_list = []
fav_list = []
sche_list = []
file_output = open('seat_info.txt', 'w+')
file_favlist = open('liked_seats.config', 'w+')
completed = 1
iid = 1
timer_stat = 0
stopp = 1
time_avai = datetime.time(6, 59, 50, 0)
time_forb = datetime.time(23, 0, 0, 0)


def print_list():
    # print(crawl_list)
    for room in crawl_list:
        # print('===========================')
        for seat in room:
            if seat[1] == '-':
                file_output.write('\n')
                # print()
            file_output.write(seat + '\t')
            # print(seat + '\t'),
    print('Crawl complete. read seat_info.txt')


def favlist_init():
    global fav_list
    raw_data = file_favlist.read()
    slice_mark = 0
    for i in range(0, len(raw_data)):
        if raw_data[i] == ' ' or raw_data[i] == '\n' or raw_data[i] == '\t':
            fav_list.append(raw_data[slice_mark: i])
            slice_mark = i + 1
    if slice_mark < len(raw_data): fav_list.append(raw_data[slice_mark:len(raw_data)])

    for i in fav_list:
        listBox_fav.insert(tk.END, i)


def favlist_write():
    global fav_list, file_favlist
    os.remove(file_favlist.name)
    for i in fav_list:
        file_favlist.write(i + '\n')


class CrawlThread(threading.Thread):  # 继承父类threading.Thread
    mapid = '0-000'

    def __init__(self, threadID, name, counter, mapid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.mapid = mapid

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        global completed
        global iid
        # print('Thread of mapid ' + self.mapid + 'started')
        try:
            raw_data_2 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx',
                                       cookies=cookies,
                                       headers=header_example,
                                       data={'data_type': 'getMapPointInit', 'mapid': self.mapid}).json()
        except:
            print("Failed to request for room " + self.mapid + '\'s info')
        else:
            raw_data_2_2 = json.loads(raw_data_2['data'])
            i = 0
            for seat in raw_data_2_2:
                try:
                    raw_data_3 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                                               cookies=cookies, headers=header_example,
                                               data={'data_type': 'getSeatDate', 'seatno': seat['SeatNo'],
                                                     'seatdate': data_crawl['selected_date']}).json()
                except:
                    # print("Failed to request for seat " + seat['SeatNo'] + '\'s info')
                    crawl_list[self.threadID - 1].append(seat['SeatNo'])
                    crawl_list[self.threadID - 1].append('ERR CONNECTION FAILED')
                else:
                    crawl_list[self.threadID - 1].append(seat['SeatNo'])
                    if raw_data_3['count'] != 0:
                        raw_data_3_3 = json.loads(raw_data_3['data'])
                        crawl_list[self.threadID - 1].append('Occupied')
                        for book in raw_data_3_3:
                            print(book)
                            crawl_list[self.threadID - 1].append(
                                '\t' + book['Id'] + ' ' + book['reader_no'] + ' ' + book['real_name'] + ' ' + book[
                                    'StartTime'] + '--->' + book['EndTime'])
                        print()
                        file_output.write('\n')
                    else:
                        crawl_list[self.threadID - 1].append('spare')
                    i += 1
        completed += 1
        print(iid - completed)
        if completed >= iid:
            print_list()


window = tk.Tk()
window.title('HUNNU Library Tool V0.1')
window.geometry('1000x300')

label_asp = tk.Label(window, text='ASP:', font=('Arial', 10))
label_asp.place(x=10, y=10)
label_txw = tk.Label(window, text='txw:', font=('Arial', 10))
label_txw.place(x=10, y=40)
label_dt = tk.Label(window, text='dt:', font=('Arial', 10))
label_dt.place(x=10, y=70)

var_asp = tk.StringVar()
entry_asp = tk.Entry(window, textvariable=var_asp, font=('Arial', 10))
entry_asp.place(x=80, y=10)

var_txw = tk.StringVar()
entry_txw = tk.Entry(window, textvariable=var_txw, font=('Arial', 10))
entry_txw.place(x=80, y=40)

var_dt = tk.StringVar()
entry_dt = tk.Entry(window, textvariable=var_dt, font=('Arial', 10))
entry_dt.place(x=80, y=70)

label_terminal = tk.Label(window, text='--Terminal--', font=('Arial', 8))

var_terminal = tk.StringVar()
message_terminal = tk.Message(window, textvariable=var_terminal, font=('Microsoft YaHei', 14), width=300)

var_seatNo = tk.StringVar()
entry_seatNo = tk.Entry(window, textvariable=var_seatNo, width=10, font=('Arial', 10))

var_date = tk.StringVar()
entry_date = tk.Entry(window, textvariable=var_date, width=10, font=('Arial', 10))

var_strtt = tk.StringVar()
entry_strtt = tk.Entry(window, textvariable=var_strtt, width=10, font=('Arial', 10))

var_endt = tk.StringVar()
entry_endt = tk.Entry(window, textvariable=var_endt, width=10, font=('Arial', 10))

label_seatNo = tk.Label(window, text='Seat No:', font=('Arial', 10))
label_date = tk.Label(window, text='Date:', font=('Arial', 10))
label_from = tk.Label(window, text='from ', font=('Arial', 10))
label_to = tk.Label(window, text='to ', font=('Arial', 10))

label_favlist = tk.Label(window, text='Liked Seats', font=('Arial', 10))

listBox_fav = tk.Listbox(window, width=30)
listBox_booked = tk.Listbox(window, width=40)


def transf():
    favlist_init()

    label_asp.place_forget()
    label_txw.place_forget()
    label_dt.place_forget()
    entry_asp.place_forget()
    entry_txw.place_forget()
    entry_dt.place_forget()
    button_log.place_forget()

    label_terminal.place(x=10, y=110)
    message_terminal.place(x=10, y=130)
    label_seatNo.place(x=10, y=10)
    label_date.place(x=200, y=10)
    label_from.place(x=10, y=40)
    label_to.place(x=200, y=40)
    entry_seatNo.place(x=80, y=10)
    entry_date.place(x=260, y=10)
    entry_strtt.place(x=80, y=40)
    entry_endt.place(x=260, y=40)
    button_check.place(x=10, y=70)
    button_addfav.place(x=100, y=70)
    button_book.place(x=190, y=70)
    button_sche.place(x=280, y=70)
    label_favlist.place(x=400, y=10)
    listBox_fav.place(x=400, y=40)
    button_delfav.place(x=400, y=240)
    button_bomb.place(x=500, y=240)
    listBox_booked.place(x=630, y=40)
    button_record.place(x=630, y=240)
    button_cancel.place(x=730, y=240)


def log():
    #cookies['ASP.NET_SessionId'] = var_asp.get()
    #cookies['txw_cookie_txw_unit_Id'] = var_txw.get()
    #cookies['dt_cookie_user_name_remember'] = var_dt.get()
    try:
        cus_info = requests.post(urls['UserInfo'], data=data_personal, cookies=cookies)
    except:
        var_terminal.set('Connection failed.')
    else:
        print(cus_info)
        cus_info = cus_info.json()
        if cus_info['code'] == 0:
            cus_info = json.loads(cus_info['data'])
            window.title(window.title() + ' Hello! ' + cus_info['real_name'])
            transf()


button_log = tk.Button(window, text='Login', width=6, height=1, command=log)
button_log.place(x=30, y=120)


def check():
    global var_terminal
    try:
        raw_data_3 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', cookies=cookies,
                                   headers=header_example, data={'data_type': 'getSeatDate', 'seatno': var_seatNo.get(),
                                                                 'seatdate': var_date.get()}).json()
    except:
        var_terminal.set('Error: Connection failed')
    else:
        var_terminal.set(raw_data_3['msg'])


button_check = tk.Button(window, text='Check', width=8, height=1, command=check)


def favadd():
    listBox_fav.insert(tk.END, [var_seatNo.get(), '||', var_date.get(), '||', var_strtt.get(), '||', var_endt.get()])


button_addfav = tk.Button(window, text='Like', width=8, height=1, command=favadd)


def favdel():
    print(listBox_fav.curselection())
    listBox_fav.delete(listBox_fav.curselection())


button_delfav = tk.Button(window, text='Remove', width=8, height=1, command=favdel)


def timer_main():
    global stopp
    ima = datetime.datetime.now()
    #print(ima)
    #print(ima.time() - time_avai)
    if ima.__gt__(time_avai) and ima.__lt__(time_forb):
        #print('timer triggered!')
        for i in range(0, listBox_fav.size()):
            pss = listBox_fav.get(i)
            data_book['seatno'] = pss[0]
            data_book['seatdate'] = pss[2]
            data_book['datetime'] = [pss[4], pss[6]]
            try:
                test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                                     data=data_book, cookies=cookies)
            except:
                var_terminal.set("Error:Connection Failed")
            else:
                try:
                    print(test.json())
                    var_terminal.set(test.json()['msg'])
                except:
                    var_terminal.set('Error not JSON')
                else:
                    if test.json()['code'] == '0':
                        stopp = 0
    if stopp == 1:
        main_timer = Timer(0.5, timer_main)
        main_timer.start()
    else:
        timer_stat = 0
        print('timer stopped.')



main_timer = Timer(0.5, timer_main)


def start_timer():
    global timer_stat, stopp
    if timer_stat == 0:
        timer_stat = 1
        stopp = 1
        main_timer.start()
    else:
        stopp = 0


button_bomb = tk.Button(window, text='Round', width=8, height=1, command=start_timer)

def book():
    data_book['seatno'] = var_seatNo.get()
    data_book['seatdate'] = var_date.get()
    data_book['datetime'] = [var_strtt.get(), var_endt.get()]
    try:
        test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                             data=data_book, cookies=cookies)
    except:
        var_terminal.set("Error:Connection Failed")
    else:
        try:
            var_terminal.set(test.json()['msg'])
        except:
            var_terminal.set('Error not JSON')


button_book = tk.Button(window, text='Book Now', width=8, height=1, command=book)


def sche():
    data_book['seatno'] = var_seatNo.get()
    data_book['seatdate'] = var_date.get()
    data_book['datetime'] = [var_strtt.get(), var_endt.get()]
    sche_list.append(data_book)


button_sche = tk.Button(window, text='Schedule', width=8, height=1, command=sche)


def get_personal():
    try:
        test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatRecordHandler.ashx',
                             data=data_record, cookies=cookies)
    except:
        var_terminal.set("Error:Connection Failed")
    else:
        #print(test)
        listBox_booked.delete(0, tk.END)
        for i in test.json():
            listBox_booked.insert(tk.END, [i['SeatInfo_Code'], i['StartTime'], i['EndTime'], i['StatusCN'], i['Id']])


button_record = tk.Button(window, text='Refresh', width=8, height=1, command=get_personal)


def cancel_book():
    print(listBox_booked.get(listBox_booked.curselection())[4])
    try:
        test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                            data={'data_type': 'cancel_seat_date',
                                'id': listBox_booked.get(listBox_booked.curselection())[4]}, cookies=cookies)
    except:
        var_terminal.set("Error:Connection Failed")
    else:
        var_terminal.set(test.json()['msg'])
        get_personal()


button_cancel = tk.Button(window, text='Cancel', width=8, height=1, command=cancel_book)


window.mainloop()
