#/bin/env/python
#coding:utf-8

"""
12306 网站余票查询模块，使用python3环境
2018-5-22
"""
import json
import re
import conf
import requests


class TickQurey:
    def __init__(self):
        #站点信息
        self.station_name=dict()
        self.ticks=list(list())
        #余票信息
    def get_station_name(self):
        '''
        获取车站对应的名称
        :return:
        '''
        pattern=re.compile('\@(.*?)(\d{1,3})')
        staion_info=list()
        conf_station=self.deal_station_conf()
        station_info=re.findall(pattern,conf_station)
        for staion_item in station_info:
            tmp="".join(staion_item)
            station_list=tmp.split('|')
            self.station_name[station_list[1]]=station_list[2]


    def read_station_conf(self):
        """
        读取车站配置文件
        :return:
        """
        try:
            with open("station_name.conf","r",encoding="utf-8") as fr:
                buff=fr.read()
        except Exception as e:
                print("FILE is failuer",(str(e)))
                buff=None
        return buff


    def deal_station_conf(self):
        return self.read_station_conf()


    def get_tick_data(self,date,from_station,to_staion):
        """
        获取车次信息
        :param date:时间
        :param from_station:出发站
        :param to_staion: 到达站
        :return: 车次信息
        """
        try:
            from_station=self.station_name[from_station]
            to_staion=self.station_name[to_staion]
        except Exception as e:
            print(str(e))
            return False
        tick_url = "".join([conf.URL, conf.T_DATE, date, conf.F_STATION, from_station, conf.T_STATION, to_staion,conf.AUTH])
        tick_info=self.get_raw_data(tick_url)
        if not tick_info:
            return None
        for tick_item in tick_info['data']['result']:
            tmp="".join(tick_item)
            tick_raw=tmp.split('|')
            tick_list=list()
            tick_list.append(tick_raw[8])
            tick_list.append(tick_raw[9])
            tick_list.append(tick_raw[10])
            tick_list.append(tick_raw[3])
            tick_list.append(tick_raw[32])#特等座
            tick_list.append(tick_raw[31])#一等座
            tick_list.append(tick_raw[30])#二等座
            tick_list.append(tick_raw[23]) #软卧
            tick_list.append(tick_raw[28]) #硬卧
            tick_list.append(tick_raw[29]) #硬座
            tick_list.append(tick_raw[26])#无座
            self.ticks.append(tick_list)
            self.ticks.append(tick_list)

    def get_raw_data(self,url):
        """
        提交get信息进行查询
        :param url:
        :return:
        """
        try:
            response=requests.get(url)
        except Exception as e:
            print(str(e))
        if response.status_code!=200:
            return None
        return response.json()

    def show_info(self):
        for seat_item in conf.seat_info:
            print ('%15s'%(seat_item),end='\t')
        print('\n')
        for tick_item in self.ticks:
            for tick in tick_item:
                print('%15s'%(tick),end='\t\t')
            print('\n')

if __name__ == "__main__":
    tickqurey=TickQurey()
    tickqurey.get_station_name()
    date,from_staion,to_staion=input().split(' ')
    tickqurey.get_tick_data(date,from_staion,to_staion)
    tickqurey.show_info()
    input('按任意键关闭')



