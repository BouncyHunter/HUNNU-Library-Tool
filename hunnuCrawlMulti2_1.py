import requests
import json
import threading

cookies = {'ASP.NET_SessionId': ' ', 'txw_cookie_txw_unit_Id': ' ', 'dt_cookie_user_name_remember': ' '}
header_example = {'Host': 'wx.lib.hunnu.edu.cn', 'Accept': 'application/json', 'Origin': 'http://wx.lib.hunnu.edu.cn', 'User-Agent': '7.0.5 WindowsWechat'}
data = {'selected_date': '2020-04-24', 'data_type': 'list'}
mpr = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatAddressHandler.ashx', headers=header_example, cookies=cookies, data=data)
print(mpr)
select_date = '2020-04-24'
file_output = open('index.out', 'w+')
tot_list = []
completed = 1;

def print_list():
    print(tot_list)
    for room in tot_list:
        print('===========================')
        for seat in room:
            if seat[1] == '-':
                file_output.write('\n')
                print()
            file_output.write(seat + '\t')
            print(seat + '\t'),

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
                    raw_data_3 = requests.post('http://wx.lib.hunnu.edu.cn/mobile/ajax/seat/SeatDateHandler.ashx', cookies=cookies, headers=header_example, data={'data_type': 'getSeatDate', 'seatno': seat['SeatNo'], 'seatdate': select_date}).json()
                except:
                    #print("Failed to request for seat " + seat['SeatNo'] + '\'s info')
                    tot_list[self.threadID - 1].append(seat['SeatNo'])
                    tot_list[self.threadID - 1].append('ERR CONNECTION FAILED')
                else:
                    tot_list[self.threadID - 1].append(seat['SeatNo'])
                    if raw_data_3['count'] != 0:
                        raw_data_3_3 = json.loads(raw_data_3['data'])
                        tot_list[self.threadID - 1].append('Occupied')
                        for book in raw_data_3_3:
                            print(book)
                            tot_list[self.threadID - 1].append('\t' + book['Id'] + ' ' + book['reader_no'] + ' ' + book['real_name'] + ' ' + book['StartTime'] + '--->' + book['EndTime'])
                        print()
                        file_output.write('\n')
                    else:
                        tot_list[self.threadID - 1].append('spare')
                    i += 1
        completed += 1
        print(iid - completed)
        if completed >= iid:
            print_list()







raw_data_1 = mpr.json()
raw_data_1_1 = json.loads(raw_data_1['data'])
iid = 1;
for room in raw_data_1_1:
    tot_list.append([room['Map_Id'] + '\t' + room['Name'] + '\t\t\t' + room['Quantity'] + '/' + room['status1'] + '/' + room['status2']])
    CrawlThread(iid, 'thread', iid, room['Map_Id']).start()
    iid += 1


