# -*- coding: utf-8 -*-
# Author  : Mr.Lee Ji
# Email   : 470390366@qq.com
# Time    : 2019/8/13 1:01
import json
import re
import smtplib
import urllib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import requests
from PIL import Image
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import time
from CityCode import station_dic

disable_warnings(InsecureRequestWarning)

class OneTwoThreeZeroSix():
    def __init__(self,username,password,my_sender,my_user):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/68.0'}
        self.session = requests.Session()
        self.session.verify = False
        self.username = username
        self.password = password
        self.my_sender = my_sender  # 发件人邮箱账号
        self.my_user = my_user  # 收件人邮箱账号
        self.set_code = {
            '9': '商务座',
            'M': '一等座',
            'O': '二等座',
            'I': '一等卧',
            'J': '二等卧',

        }
        self.train_set = ['9', 'M', 'O', 'I', 'J']



    def captcha(self):
        #获取验证码
        captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9250735987164926'
        captcha_url_img = self.session.get(captcha_url,headers= self.headers).content
        with open('captcha.png','wb') as ca:
            ca.write(captcha_url_img)
        captacha_img = Image.open('captcha.png')
        captacha_img.show()
        captacha_img.close()
        #验证码验证
        choice_capt = {'1':'40,40',
                       '2':'110,40',
                       '3':'180,40',
                       '4':'250,40',
                       '5':'40,110',
                       '6':'110,110',
                       '7':'180,110',
                       '8':'250,110'}

        print(""" 
                -----------------
                | 1 | 2 | 3 | 4 |
                -----------------
                | 5 | 6 | 7 | 8 |
                ----------------- """)
        number_inpt = input("输入验证码索引(见上图，以','分割）：")
        number_sp=number_inpt.split(',')
        number_len = len(number_sp)
        codes=''
        for i in range(number_len):
            codes=codes+choice_capt[number_sp[i]]+','
        answer =codes.rstrip(',')
        captcha_cheak = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        data = {'answer': answer,
                'login_site': 'E',
                'rand': 'sjrand',
                }
        captacha_req = self.session.post(captcha_cheak,headers=self.headers,data=data).text
        result_str = re.search(r'\{(.*?)\}',captacha_req)
        captacha_result_json = json.loads(result_str.group())
        capt_result = captacha_result_json['result_code']
        if str(capt_result) == '4':
            print(captacha_result_json['result_message'])
            time.sleep(1)
            print('正在登陆.....')
        else:
            print(captacha_result_json['result_message'])
            self.captcha()


    def login(self):
        login_url = 'https://kyfw.12306.cn/passport/web/login'
        login_url2 = 'https://kyfw.12306.cn/otn/login/userLogin'
        login_url3 = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        login_url4 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        login_url5 = 'https://kyfw.12306.cn/otn/uamauthclient'
        data_url1 = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
        }
        self.session.cookies['RAIL_DEVICEID'] = 'XQ0xiH-VnSGYwebVyByxBEU1yJqsStE6f1Khg9ZD6tMgYBV-vaqYc4QDHqaHtiv0-WjiiD2VmmElfDOLIzrAXSTpmx_ggRwmtCDd3az9erjsnV2k2Y73l63q_zyVoIPBbQG_4gTnAoK8fQVKgkExML_wg04ayGxQ'
        self.session.cookies['RAIL_EXPIRATION'] = '1565922992430'
        self.session.cookies['route'] = 'c5c62a339e7744272a54643b3be5bf64'
        login_req = self.session.post(login_url, headers=self.headers, data=data_url1).text
        login_req_result = json.loads(login_req)
        print(login_req_result['result_message'])
        data_url2 = {
            '_json_att': ''
        }
        req_url = self.session.post(login_url2, headers=self.headers, data=data_url2).text
        req_url1 = self.session.get(login_url3, headers=self.headers).text
        data_url4 = {'appid': 'otn'}
        req_url2 = self.session.post(login_url4, headers=self.headers, data=data_url4).text
        result_url2 = json.loads(req_url2)
        # print(result_url2['result_message'])
        # print(result_url2)
        tk = result_url2['newapptk']
        data_url5 = {'tk': tk}
        req_url3 = self.session.post(login_url5, headers=self.headers, data=data_url5).text
        result_url3 = json.loads(req_url3)
        # print(result_url3['result_message'] + ',' + result_url3['username'])
        print(result_url3['result_message'])


    #查票
    def cheak_ticket(self,userinfo):
        global train
        self.train_data = user_info['train_data']
        self.from_station = user_info['from_station']
        self.to_station = user_info['to_station']
        self.fromstation = user_info['fromstation']
        self.tostation = user_info['tostation']
        self.train_num = user_info['train_num']
        self.ticketer_name = user_info['ticketer_name']
        self.ticketer_num = user_info['ticketer_num']
        self.ticketer_phone = user_info['ticketer_phone']
        self.train_set = user_info['train_set']



        cheak_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+self.train_data+'&leftTicketDTO.from_station='+self.from_station+'&leftTicketDTO.to_station='+self.to_station+'&purpose_codes=ADULT'
        cheak_req = self.session.get(cheak_ticket_url,headers=self.headers).text
        cheak_req_json = json.loads(cheak_req)
        for i in cheak_req_json['data']['result']:
            tmplist = i.split('|')
            if train_num == tmplist[3]:
                print(tmplist[3]+'  '+self.train_data)
                print('出发地：'+self.fromstation+'  目的地：'+self.tostation)
                self.__statistics_tickets(tmplist)

    def __statistics_tickets(self,train_info):
        print('开始查询 '+train_info[3]+' 票数')
        url1 = 'https://kyfw.12306.cn/otn/login/checkUser'
        url2 = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        url3 = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        url4 = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        url5 = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        url6 = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'  #下单
        url7 = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'  #计数
        data_url1 = {'_json_att':''}
        data_url2 = {'secretStr': urllib.parse.unquote(train_info[0]),
                 'train_date': self.train_data,
                 'back_train_date': self.train_data,
                 'tour_flag': 'dc',
                 'purpose_codes': 'ADULT',
                 'query_from_station_name': self.fromstation,
                 'query_to_station_name': self.tostation,
                 'undefined':''}
        req1 = self.session.post(url1,headers=self.headers,data=data_url1).text
        req2 = self.session.post(url2, headers=self.headers, data=data_url2).text
        req3 = self.session.post(url3, headers=self.headers, data=data_url1).text
        self.token_req = re.findall(r"globalRepeatSubmitToken = '(.*?)'",req3)[0]
        self.key_check_isChange =re.findall(r"'key_check_isChange':'(.*?)'",req3)[0]
        self.train_location = re.findall(r"'tour_flag':'dc','train_location':'(.*?)'}",req3)[0]
        data_url4 = {'_json_att': '',
                 'REPEAT_SUBMIT_TOKEN': self.token_req}
        req4 = self.session.post(url4, headers=self.headers, data=data_url4).text#定单界面
        req4_json = json.loads(req4)
        encStr = req4_json['data']['normal_passengers']
        allEncStr=''
        for i in list(encStr):
            passengers_name = i['passenger_name']
            if passengers_name == self.ticketer_name:
                allEncStr = i['allEncStr']
                break
        #下单
        self.passengerTicketStr = self.train_set + ',0,1,' + self.ticketer_name + ',1,' + self.ticketer_num + ',' + self.ticketer_phone + ',N,'+allEncStr
        self.oldPassengerStr = self.ticketer_name + ',1,' + self.ticketer_num + ',1_'
        data_url5 = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'tour_flag': 'dc',
            'randCode':'',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN':self.token_req
        }
        req5 = self.session.post(url5, headers=self.headers, data=data_url5).text
        timeArray = time.strptime(self.train_data, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        time_local = time.localtime(timeStamp)
        train_date_temp = time.strftime("%a %b %d %Y %H:%M:%S", time_local)
        train_date2 = train_date_temp + ' GMT+0800 (中国标准时间)'
        data_url7 = {
            'train_date':train_date2,
            'train_no':train_info[2],
            'stationTrainCode':train_info[3],
            'seatType':self.train_set,
            'fromStationTelecode':train_info[6],
            'toStationTelecode':train_info[7],
            'leftTicket':train_info[12],
            'purpose_codes':'00',
            'train_location':train_info[15],
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN':self.token_req
        }
        req7 = self.session.post(url7, headers= self.headers, data=data_url7).text
        try:
            result_url7 = json.loads(req7)
            result = result_url7['data']['ticket']
            if train_info[3][0] == 'D' and train =='O':
                set_num = result.split(',')
                set=self.set_code[self.train_set]
                print(set+':'+set_num[0])
                print('无座:'+set_num[1])
                print('是否购买本次车票 输入 1 购买 ，输入 2 取消 。')
                is_buy = input('请输入：')
                if is_buy == '1':
                    self.buy_ticket(train_info)
                else:
                    quit()
            else:
                set = self.set_code[self.train_set]
                print(set + ':' + result)
                print('是否购买本次车票 输入 1 购买 ，输入 2 取消 。')
                is_buy = input('请输入：')
                if is_buy == '1':
                    self.buy_ticket(train_info)
                else:
                    quit()
        except Exception as e:
            print(self.set_code[train]+':无票')

     #购票
    def buy_ticket(self,train_info):
        buy_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            'passengerTicketStr': self.passengerTicketStr,
            'oldPassengerStr': self.oldPassengerStr,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': train_info[12],
            'train_location': train_info[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token_req
        }
        req = self.session.post(buy_url, headers=self.headers, data=data).text
        req_json = json.loads(req)
        if req_json['status']:
            # print(req_json)
            print('购票成功')
            self.sendMail(train_info)
        else:
            print(req_json)
            print('购票失败')

    def sendMail(self,train_info):
        try:
            '''发送邮件'''
            message = self.train_data+' '+self.train_num+' 次列车购票成功，请前去付款'
            msg = MIMEText(message, "plain", 'utf-8')  # 发送邮件内容
            msg["Subject"] = Header('购票成功', 'utf-8')  # 发送邮件主题/标题
            msg["From"] = formataddr(['Mr.Lee Ji', self.my_sender])  # 邮件发送方名称
            msg["To"] = formataddr(['xixixi', self.my_user])  # 邮件接收方名称

            s = smtplib.SMTP("smtp.qq.com", 25)  # 邮箱的传输协议，端口默认25
            s.login(self.my_sender, 'fyebwvkwlqbybiif')  # 登录邮箱，这里的第二个参数为qq邮箱授权码，不要填你的登录密码
            s.sendmail(self.my_sender, [self.my_user, ], msg.as_string())  # 发送方，接收方，发送消息
            s.quit()  # 退出邮箱
            print("抢票通知邮件发送成功！")
        except Exception:
            print("邮件发送失败~~")


if __name__ == "__main__":

    username = input(' 请输入12306用户名：')
    password = input(' 请输入12306密码：')
    train_data = input(' 购票日期（格式：2019-08-20）：')
    ticketer_name = input(' 购票用户姓名：')
    ticketer_phone= input(' 购票用户手机：')
    ticketer_num1 = input(' 购票用户身份证：')
    ticketer_num = ticketer_num1[0:4] + '***********' + ticketer_num1[-3:]
    forstation = input(' 请输入出发地：')
    tostation = input(' 请输入目的地：')
    train_num = input(' 请输入车次：')
    print('座位类型：商务座(9),一等座(M),二等座(O[英文大写字母O]),一等卧(I),二等卧(J)')
    train_set=input(' 请输入座次：')
    my_sender = input(' 请输入发件人邮箱账号：')  # 发件人邮箱账号
    my_user = input(' 请输入收件人邮箱账号：')  # 收件人邮箱账号
    onetwothreezoresix = OneTwoThreeZeroSix(username,password,my_sender,my_user)
    onetwothreezoresix.captcha()
    onetwothreezoresix.login()
    user_info = {
        'train_data': train_data,
        'fromstation': forstation,
        'tostation': tostation,
        'from_station' : station_dic[forstation],
        'to_station' :station_dic[tostation],
        'train_num': train_num,
        'ticketer_name': ticketer_name,
        'ticketer_num': ticketer_num,
        'ticketer_phone': ticketer_phone,
        'train_set':train_set
    }
    onetwothreezoresix.cheak_ticket(user_info)


