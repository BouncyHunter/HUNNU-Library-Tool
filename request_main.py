import requests
import json
import threading

from pip._vendor.distlib.compat import raw_input

cookies = {'ASP.NET_SessionId': ' ', 'txw_cookie_txw_unit_Id': ' ',
           'dt_cookie_user_name_remember': ' '}
data_book = {'data_type': 'seatDate', 'seatno': '2-032', 'seatdate': '2000-04-24', 'datetime': [0,120]}
data_personal = {'data_type': 'user_info'}
data_crawl = {'selected_date': '2020-04-24', 'data_type': 'list'}
header_example = {'Host': 'wx.lib.hunnu.edu.cn', 'Accept': 'application/json', 'Origin': 'http://wx.lib.hunnu.edu.cn', 'User-Agent': '7.0.5 WindowsWechat'}
urls = {'UserInfo': 'http://wx.lib.hunnu.edu.cn/mobile/ajax/user/UserHandler.ashx'}

crawl_list = []
file_output = open('seat_info.txt', 'w+')
completed = 1
iid = 1

def print_list():
    #print(crawl_list)
    for room in crawl_list:
        #print('===========================')
        for seat in room:
            if seat[1] == '-':
                file_output.write('\n')
                #print()
            file_output.write(seat + '\t')
            #print(seat + '\t'),
    print('Crawl complete. read seat_info.txt')

class CrawlThread (threading.Thread):   #继承父类threading.Thread
    mapid = '0-000'
    def __init__(self, threadID, name, counter, mapid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.mapid = mapid
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        global completed
        global iid
        #print('Thread of mapid ' + self.mapid + 'started')
        try:
            raw_data_2 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatInfoHandler.ashx', cookies=cookies,
                                       headers=header_example,
                                       data={'data_type': 'getMapPointInit', 'mapid': self.mapid}).json()
        except:
            print("Failed to request for room " + self.mapid + '\'s info')
        else:
            raw_data_2_2 = json.loads(raw_data_2['data'])
            i = 0
            for seat in raw_data_2_2:
                try:
                    raw_data_3 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', cookies=cookies, headers=header_example, data={'data_type': 'getSeatDate', 'seatno': seat['SeatNo'], 'seatdate': data_crawl['selected_date']}).json()
                except:
                    #print("Failed to request for seat " + seat['SeatNo'] + '\'s info')
                    crawl_list[self.threadID - 1].append(seat['SeatNo'])
                    crawl_list[self.threadID - 1].append('ERR CONNECTION FAILED')
                else:
                    crawl_list[self.threadID - 1].append(seat['SeatNo'])
                    if raw_data_3['count'] != 0:
                        raw_data_3_3 = json.loads(raw_data_3['data'])
                        crawl_list[self.threadID - 1].append('Occupied')
                        for book in raw_data_3_3:
                            print(book)
                            crawl_list[self.threadID - 1].append('\t' + book['Id'] + ' ' + book['reader_no'] + ' ' + book['real_name'] + ' ' + book['StartTime'] + '--->' + book['EndTime'])
                        print()
                        file_output.write('\n')
                    else:
                        crawl_list[self.threadID - 1].append('spare')
                    i += 1
        completed += 1
        print(iid - completed)
        if completed >= iid:
            print_list()

#cookies['ASP.NET_SessionId'] = input('ASP.NET_SessionId:')
#cookies['txw_cookie_txw_unit_Id'] = input('txw_cookie_txw_unit_Id:')
#cookies['dt_cookie_user_name_remember'] = input('dt_cookie_user_name_remember:')





print('Checking...')
try:
    cus_info = requests.post(urls['UserInfo'], data=data_personal, cookies=cookies)
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
        slice_mark = 0;
        for i in range(0, len(comm)):
            if comm[i] == ' ':
                comm_slice.append(comm[slice_mark:i])
                slice_mark = i + 1
        comm_slice.append(comm[slice_mark:len(comm)])
        while comm_slice[0] != 'quit':
            if comm_slice[0] == 'help' or comm_slice[0] == '?':
                print('HELP\t\t\t\t\t\t\t\tshow help info')
                print('QUIT\t\t\t\t\t\t\t\texit the program')
                print('BOOK [SEAT NO] [DATE] [START TIME] [END TIME]\t\t\t\t\t\t\t\tattempt to book chosen seat of chosen time')
                print('CRAWL [DATE]\t\t\t\t\t\t\t\tcrawl all seats\' status of chosen date')
            elif comm_slice[0] == 'book':
                if len(comm_slice) >= 5:
                    data_book['seatno'] = comm_slice[1]
                    data_book['seatdate'] = comm_slice[2]
                    data_book['datetime'] = [comm_slice[3], comm_slice[4]]
                    try:
                        test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx',
                                             data=data_book, cookies=cookies)
                    except:
                        print("Error:Connection Failed")
                    else:
                        test = test.json()
                        print(test['msg'])
                else:
                    print('Invalid input')
                    print('BOOK [SEAT NO] [DATE] [START TIME] [END TIME]\t\t\t\t\t\t\t\tattempt to book chosen seat of chosen time')
            elif comm_slice[0] == 'crawl':
                if len(comm_slice) >= 2:
                    data_crawl['selected_date'] = comm_slice[1]
                    try:
                        mpr = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatAddressHandler.ashx',
                                        headers=header_example, cookies=cookies, data=data_crawl)
                    except:
                        print('Error: Connection failed')
                    else:
                        raw_data_1 = mpr.json()
                        raw_data_1_1 = json.loads(raw_data_1['data'])
                        completed = 1;
                        iid = 1;
                        for room in raw_data_1_1:
                            crawl_list.append([room['Map_Id'] + '\t' + room['Name'] + '\t\t\t' + room['Quantity'] + '/' +
                                             room['status1'] + '/' + room['status2']])
                            CrawlThread(iid, 'thread', iid, room['Map_Id']).start()
                            iid += 1
                else:
                    print('Invalid input.')
                    print('CRAWL [DATE]\t\t\t\tcrawl all seats\' status of chosen date')
            comm = raw_input('>')
            comm_slice = []
            slice_mark = 0;
            for i in range(0, len(comm)):
                if comm[i] == ' ':
                    comm_slice.append(comm[slice_mark:i])
                    slice_mark = i + 1
            comm_slice.append(comm[slice_mark:len(comm)])
            print(comm_slice)



    else:
        print('Failed to sign up. msg: ' + cus_info['msg'])

'''
try:
    test = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', data=data_book, cookies=cookies)
except:
    print("Error:Connection Failed")
else:
    try:
        test2 = test.json()
    except:
        print('Error: ')
r = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', data=data_book, cookies=cookies)
print(r.json())
'''