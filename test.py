#coding:utf8

"""
描述 此文件用于提取装维人员属性数据，并将其输出
版本 0.1
作者 Shangdong
"""


import datetime

class People:
    def __init__(self):
        self.file = open('/home/ysd/data/装维互联网数据20171019/人员明细.csv')
        self.people = []
        for line in self.file.readlines():
            self.people.append(line.split('","'))
        self.file.close()

    def getStaffId(self):
        staff_id = {}
        for i in range(len(self.people)):
            if i > 0:
                key = self.people[i][0].split('"')[1]
                staff_id[key] = [self.people[i][11],self.people[i][12]]
        return staff_id

class BonusPoint:
    def __init__(self, zhuang_ji, xiu_zhang, ying_xiao, yan_shen):
        self.file = open('/home/ysd/data/装维互联网数据20171019/积分明细宽表.csv')
        self.bonus_point = {}
        for line in self.file.readlines()[1:]:
            list = []
            key = line.split(',')[0]
            list.append(line.split(',')[4])
            a = line.split(',')[-3]
            b = unicode(a,'gbk')
            #print type(b.encode('utf8'))
            b = b.encode('utf8')
            if b == '装机评价' or b == '抢单' or b == '装机调度':
                b = '装机'
            if b == '故障' or b == '故障调度' or b == '障碍评价':
                b = '修障'
            if b == '装积分漏单补算' or ('干预' in b):
                b = '干预'
            if b == '积分商城' or b == '活动':
                b = '活动'
            if b =='考试' or b == '使用频次' or b == '投诉':
                b = '其他'
            #print b
            list.append(b)
            if line.split(',')[-2] != '':
                if b == '装机' and line.split(',')[-2] in zhuang_ji:
                    list.append(zhuang_ji[line.split(',')[-2]])
                elif b == '修障' and line.split(',')[-2] in xiu_zhang:
                    list.append(xiu_zhang[line.split(',')[-2]])
                elif b == '营销' and line.split(',')[-2] in ying_xiao:
                    list.append(ying_xiao[line.split(',')[-2]])
                elif b == '延伸服务' and line.split(',')[-2] in yan_shen:
                    list.append(yan_shen[line.split(',')[-2]])
                else:
                    list.append('Null')
            if key in self.bonus_point:
                self.bonus_point[key].append(list)
            else:
                value = []
                self.bonus_point[key] = value
        self.file.close()

    def getBonusPolit(self):
        for key in self.bonus_point:
            #       装机,修障,营销,延伸服务,活动,人工干预,其他
            list = [0, 0, 0, 0, 0, 0, 0]
            dict_zhuangji = {'shijian':[],'jine':[]}
            dict_xiuzhang = {'shijian':[],'leixing':[1,1]}
            dict_yingxiao = {'jifen':[],'leixing':[0,0,0]}
            dict_yanshen  = {'feiyong':[]}
            for i in range(len(self.bonus_point[key])):
                if self.bonus_point[key][i][1] == '装机':
                    list[0] += 1
                    if len(self.bonus_point[key][i][2]) > 8 and '/' in self.bonus_point[key][i][2][5]:
                        d1 = datetime.datetime.strptime(self.bonus_point[key][i][2][3], '%Y/%m/%d')
                        d2 = datetime.datetime.strptime(self.bonus_point[key][i][2][5], '%Y/%m/%d')
                        #print d1,d2,(d2-d1).days
                        dict_zhuangji['shijian'].append(int((d2-d1).days))
                        if self.bonus_point[key][i][2][6] != '':
                            dict_zhuangji['jine'].append(float(self.bonus_point[key][i][2][6]))
                if self.bonus_point[key][i][1] == '修障':
                    list[1] += 1
                    if len(self.bonus_point[key][i])==3 and len(self.bonus_point[key][i][2]) > 4:
                        d1 = datetime.datetime.strptime(self.bonus_point[key][i][2][0], '%Y/%m/%d %H:%M:%S')
                        d2 = datetime.datetime.strptime(self.bonus_point[key][i][2][1], '%Y/%m/%d %H:%M:%S')
                        dict_xiuzhang['shijian'].append(float((d2-d1).total_seconds()/3600.0))
                        if self.bonus_point[key][i][2][-2]=='1415':
                            dict_xiuzhang['leixing'][0] += 1
                        if self.bonus_point[key][i][2][-2]=='1416':
                            dict_xiuzhang['leixing'][1] += 1
                if self.bonus_point[key][i][1] == '营销':
                    list[2] += 1
                    if len(self.bonus_point[key][i][2]) == 3:
                        dict_yingxiao['jifen'].append(float(self.bonus_point[key][i][2][1]))
                        if self.bonus_point[key][i][2][2] == '天翼':
                            dict_yingxiao['leixing'][0] += 1
                        if self.bonus_point[key][i][2][2] == '宽带':
                            dict_yingxiao['leixing'][1] += 1
                        if self.bonus_point[key][i][2][2] == 'ITV':
                            dict_yingxiao['leixing'][2] += 1
                if self.bonus_point[key][i][1] == '延伸服务':
                    list[3] += 1
                    if self.bonus_point[key][i][2][0] != '' and self.bonus_point[key][i][2][0] != 'N':
                        dict_yanshen['feiyong'].append(float(self.bonus_point[key][i][2][0]))
                if self.bonus_point[key][i][1] == '活动':
                    list[4] += 1
                if self.bonus_point[key][i][1] == '人工干预':
                    list[5] += 1
                if self.bonus_point[key][i][1] == '其他':
                    list[6] += 1
            self.bonus_point[key].append(list)
            if len(dict_zhuangji['shijian'])!=0 and len(dict_zhuangji['jine'])!=0:
                self.bonus_point[key].append([round(float(sum(dict_zhuangji['shijian']))/len(dict_zhuangji['shijian']),3),round(float(sum(dict_zhuangji['jine']))/len(dict_zhuangji['jine']),3)])
            else:
                self.bonus_point[key].append([0.0,0.0])
            if len(dict_xiuzhang['shijian'])!=0 and dict_xiuzhang['leixing'][0]+dict_xiuzhang['leixing'][1] > 0:
                self.bonus_point[key].append([round(float(sum(dict_xiuzhang['shijian']))/len(dict_xiuzhang['shijian']),3),round(float(dict_xiuzhang['leixing'][0])/(dict_xiuzhang['leixing'][0]+dict_xiuzhang['leixing'][1]),3)])
            else:
                self.bonus_point[key].append([0.0, 0.0])
            if len(dict_yingxiao['jifen']) != 0 and dict_yingxiao['leixing'][0]+dict_yingxiao['leixing'][1]+dict_yingxiao['leixing'][2] > 0:
                self.bonus_point[key].append([round(float(sum(dict_yingxiao['jifen']))/len(dict_yingxiao['jifen']),3),round(float(dict_yingxiao['leixing'][0])/(dict_yingxiao['leixing'][0]+dict_yingxiao['leixing'][1]+dict_yingxiao['leixing'][2]),3),round(float(dict_yingxiao['leixing'][1])/(dict_yingxiao['leixing'][0]+dict_yingxiao['leixing'][1]+dict_yingxiao['leixing'][2]),3),round(float(dict_yingxiao['leixing'][2])/(dict_yingxiao['leixing'][0]+dict_yingxiao['leixing'][1]+dict_yingxiao['leixing'][2]),3)])
            else:
                self.bonus_point[key].append([0.0, 0.0, 0.0, 0.0])
            if len(dict_yanshen['feiyong'])!=0:
                self.bonus_point[key].append([round(float(sum(dict_yanshen['feiyong']))/len(dict_yanshen['feiyong']),3)])
            else:
                self.bonus_point[key].append([0.0])
        return self.bonus_point

class ZhuangJi():
    def __init__(self):
        self.file = open('/home/ysd/data/装维互联网数据20171019/out2.csv')
        self.zhuang_ji = {}
        for line in self.file.readlines()[1:]:
            key = line.split(',')[0]#主键id
            value = []
            for i in range(len(line.split(','))-1):
                value.append(line.split(',')[i+1])#综调id,区属id,区属名称,创建时间,平台记录时间,完成时间,原价格,实际价格
            self.zhuang_ji[key] = value
        self.file.close()

    def getZhuangJi(self):
        return self.zhuang_ji

class XiuZhang():
    def __init__(self):
        self.xiu_zhang = {}
        file = open('/home/ysd/data/装维互联网数据20171019/修障场景工单表.csv')
        for line in file.readlines():
            list = []
            line = line.split(',')
            key = line[27] #主键-时间id
            list.append(line[5])#报障时间
            list.append(line[8])#修复时间
            qx = unicode(line[43], 'gbk')#区县名称
            qx = qx.encode('utf8')
            list.append(qx)
            list.append(line[47])#障碍专业类型ID
            type = unicode(line[48], 'gbk')#障碍专业类型
            type = type.encode('utf8')
            list.append(type)
            self.xiu_zhang[key]=list
        file.close()

    def getXiuZhang(self):
        return self.xiu_zhang

class YingXiao():
    def __init__(self):
        self.ying_xiao = {}
        file = open('/home/ysd/data/装维互联网数据20171019/营销积分.csv')
        for line in file.readlines():
            list = []
            line = line.split('","')
            key = line[6]#主键ID
            qx = unicode(line[1], 'gbk')#区县名称
            qx = qx.encode('utf8')
            list.append(qx)
            list.append(line[14])#积分
            type = unicode(line[-2], 'gbk')#营销产品类型
            type = type.encode('utf8')
            list.append(type)
            self.ying_xiao[key] = list
        file.close()

    def getYingXiao(self):
        return self.ying_xiao

class YanShen():
    def __init__(self):
        self.yan_shen = {}
        file = open('/home/ysd/data/装维互联网数据20171019/延伸服务.csv')
        for line in file.readlines():
            list = []
            line = line.split('","')
            key = line[0].split('"')[1]#主键id
            list.append(line[8])#总计费用
            self.yan_shen[key] = list
        file.close()

    def getYanShen(self):
        return self.yan_shen

if __name__ == "__main__":
    people = People()
    staff_id_dict = people.getStaffId()
    print staff_id_dict

    zhuang_ji = ZhuangJi()
    zhuang_ji_dict = zhuang_ji.getZhuangJi()

    xiu_zhang = XiuZhang()
    xiu_zhang_dict = xiu_zhang.getXiuZhang()

    ying_xiao = YingXiao()
    ying_xiao_dict = ying_xiao.getYingXiao()

    yan_shen = YanShen()
    yan_shen_dict = yan_shen.getYanShen()

    bonus_point = BonusPoint(zhuang_ji_dict, xiu_zhang_dict, ying_xiao_dict, yan_shen_dict)
    bonus_point_dict = bonus_point.getBonusPolit()

    fl = open('/home/ysd/data/装维互联网数据20171019/out3.csv','w')
    fl.write('员工ID,' + '员工等级,' + '员工积分,' + '装机次数,' + '装机耗时/天,' + '装机均价,' + '修障次数,' + '修障耗时/时,' + '修障宽带占比,' + '营销次数,' + '营销均价,' + '营销天翼占比,' + '营销宽带占比,' + '营销ITV占比,' + '延伸服务次数,' + '延伸服务均价,' + '活动次数,' + '人工干预次数,' + '其他次数,' + '\n')
    for key in bonus_point_dict:
        if key in staff_id_dict:
            print key, bonus_point_dict[key][-5], bonus_point_dict[key][-4], bonus_point_dict[key][-3], bonus_point_dict[key][-2], bonus_point_dict[key][-1]
            fl.write(key+','+staff_id_dict[key][0]+','+staff_id_dict[key][1]+',')

            fl.write(str(bonus_point_dict[key][-5][0])+',')
            fl.write(str(bonus_point_dict[key][-4][0])+',')
            fl.write(str(bonus_point_dict[key][-4][1])+',')

            fl.write(str(bonus_point_dict[key][-5][1])+',')
            fl.write(str(bonus_point_dict[key][-3][0])+',')
            fl.write(str(bonus_point_dict[key][-3][1])+',')

            fl.write(str(bonus_point_dict[key][-5][2])+',')
            fl.write(str(bonus_point_dict[key][-2][0])+',')
            fl.write(str(bonus_point_dict[key][-2][1])+',')
            fl.write(str(bonus_point_dict[key][-2][2])+',')
            fl.write(str(bonus_point_dict[key][-2][3])+',')

            fl.write(str(bonus_point_dict[key][-5][3])+',')
            fl.write(str(bonus_point_dict[key][-1][0])+',')

            fl.write(str(bonus_point_dict[key][-5][4])+',')

            fl.write(str(bonus_point_dict[key][-5][5])+',')

            fl.write(str(bonus_point_dict[key][-5][6]))

            fl.write('\n')
    fl.close()