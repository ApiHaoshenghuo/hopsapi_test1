# @Time    : 6/18/2020 9:16 AM
# @Author  : Yang Xiaobai
# @Email   : yangzhiyongtest@163.com
import json
import re

import requests

from utils.logger import Log

logger = Log(logger='para_analysis').get_log()

class ApiCommon:
    def __init__(self):
        pass
    # 将值替换字符串中的内容

class Common:
    def __init__(self):
        pass
    # 判断是否为list，list有几级
    def estimateList(self,estimatelistValue):
        listNum=0
        while isinstance(estimatelistValue, list):
                for item_list in estimatelistValue:
                    if isinstance(item_list,list):
                        listNum+=1
                        estimatelistValue=item_list
                        break
                    else:
                        estimatelistValue = item_list
                        break
        return listNum

    # 替换字符串中指定的字符
    def replaceStr(self,strRes,strKey,strValue):
        strRes = json.dumps(strRes,ensure_ascii=False)
        logger.info(strValue)
        if not isinstance(strValue,str):
            strValue = str(strValue)
            strKey1 = "'{" + strKey + "}'"
            strKey2 = '"{' + strKey + '}"'
            strRes1 = strRes.replace(strKey1, strValue)
            strRes2 = strRes1.replace(strKey2, strValue)
        else:
            strKey = "{" + strKey + "}"
            strRes2 = strRes.replace(strKey,strValue)
        strRes3 = json.loads(strRes2,encoding='utf-8')
        return strRes3

    def getJsonValue(self,mydict, key, assitValue=None,assitKey=None):
        # mydict = json.loads(mydict,encoding="utf-8")
        if isinstance(mydict, dict):  # 使用isinstance检测数据类型，如果是字典
            if key in mydict.keys():  # 替换字典第一层中所有key与传参一致的key
                if assitValue == None:
                    needValue=mydict[key]
                    return needValue
                elif  assitValue == mydict[assitKey]:
                    needValue = mydict[key]
                    return needValue
            for k in mydict.keys():  # 遍历字典的所有子层级，将子层级赋值为变量chdict，分别替换子层级第一层中所有key对应的value，最后在把替换后的子层级赋值给当前处理的key
                chdict = mydict[k]
                if self.getJsonValue(chdict, key, assitValue=assitValue,assitKey=assitKey):
                    return self.getJsonValue(chdict, key, assitValue=assitValue,assitKey=assitKey)
        elif isinstance(mydict, list):  # 如是list
            for element in mydict:  # 遍历list元素，以下重复上面的操作
                if isinstance(element, dict):
                    if key in element.keys():
                        if assitValue == None:
                            needValue = element[key]
                            return needValue
                        elif assitValue == element[assitKey]:
                            needValue = element[key]
                            return needValue
                    for k in element.keys():
                        chdict = element[k]
                        if self.getJsonValue(chdict, key, assitValue=assitValue,assitKey=assitKey):
                            return self.getJsonValue(chdict, key, assitValue=assitValue, assitKey=assitKey)
                else:
                    for elementItem in element:
                        chdict = elementItem
                        if self.getJsonValue(chdict, key, assitValue=assitValue,assitKey=assitKey):
                            return self.getJsonValue(chdict, key, assitValue=assitValue, assitKey=assitKey)

        else:
            return False

    # 对列表中的数据进行计数
    def itemListCount(self,lst):
        itemDic = {}
        lstSet = set(lst)
        lstSet = list(lstSet)
        countEnd = 1
        for item in lstSet:
            countGap = 0
            for compareItem in lst:
                if item == compareItem:
                    countGap += 1
            countEnd = countEnd + countGap
            itemDic[item] = [item, countGap, countEnd]
        itemDic['list']=lstSet
        return itemDic
    #itemKey, itemValue, needKey
    def getValueFalse(self,lst, itemKey, itemValue, needKey):
        for i in lst:
            try:
                if i[itemKey] == itemValue:
                    return i[needKey]
                elif itemValue.isdigit():
                    if i[itemKey] == int(itemValue):
                        return i[needKey]
                else:
                    return False
            except:
                return False

    def getUrlReg(self,urla):
        urla = "https://tbroker.lifeat.cn:45788/easylife/{rest}/{broker}/login"
        regex = re.compile("{(.*?)}", re.I)
        resultlist = regex.findall(urla)
        return resultlist

    # 正则内容对比返回true
    def getConpareResult(self,strData,regular,value):
        prog = re.compile(regular)
        result = prog.findall(strData)
        logger.info(result)
        if result == value:
            return True
        else:
            return False

    # pass
    def test_upload(self,url,filepath,):
        """
        test case
        :return:
        """
        header={}
        header["content-type"] = "multipart/form-data; boundary=werghnvt54wef654rjuhgb56trtg34tweuyrgf"
        header["user-agent"]="QiniuObject-C/7.2.5 (iPhone; iOS 12.2; D5525AE8-3362-4E8C-9BE2-A604B651C1BF; m1qdTqGcH54NLtQrE2j0MRnvKf8LaJBu1A7omyfe)"
        header[":authority"]="upload-z1.qiniup.com"
        url = 'https://upload-z1.qiniup.com/'
        jsonrpc = "{\"title\": \"标题yzc0116\", \"tag\":\"标签yzc0116\",\"desc\":\"描述yzc0116\"}"
        filepath = 'C:\\Users\\yangzc\\Desktop\\FlickAnimation.avi'
        # 打开文件
        # fo = open(filepath, 'rb')
        # # video表示实际的文件参数
        # video = {'Filedata': fo}
        # params表示实际的参数列表，包括：writetoken和JSONRPC这两个参数
        params = {'writetoken': '7043f898-8322-4e39-8bb5-7956bf0eb641', 'JSONRPC': jsonrpc}
        files = {
            'token': (None, tokenValue),
            'crc32': (None, crc32Value),
            'files': ('test.txt', open(file_path, 'rb'), 'text/plain'),
        }
        r = requests.post(url=url, files=files, header=header)
        # response = requests.post(url, data=params, files=video)
        # 关闭文件
        # fo.close()
        return response


if __name__ == "__main__":
    valuea = {"isApp":"N","isTransmit":{"tokenName":[["token","token"],["Authorization","token"]],"transmitName":[["token",{"valueKey":"token","getValuePath":"$.data.token"}],["applicationToken",{"valueKey":"applicationToken","getValuePath":"$.data.applicationToken"}],["cityId",{"valueKey":"cityId","getValuePath":{"threeListAll":"$.data.cityList","threeList":"city-北京市-cityId"}}]]}}
    assitValue={"threeListAll": "$.data.cityList", "threeList": "city-北京市-cityId"}
    assitKey="getValuePath"
    valueab=Common().getJsonValue(mydict=valuea, key="valueKey1", assitValue=assitValue,assitKey=assitKey)
    print(valueab)