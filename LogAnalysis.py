'''
Created on 2018年1月30日

@author: withmaple
'''
#!/usr/bin/python
# coding:utf-8

import logging
import time
import os.path
import xlrd
import xlwt
import codecs  
from xlutils.copy import copy

#  --- 测试路径 ---
phonepath = 'sdcard/Android/data/'
#phonepath = 'storage/emulated/0/Android/data/'
#apk及log路径
filePath    = 'C:/Users/Desktop/phoneLogAnalysis/'
#预置资源路径
keywordfile = 'C:/Users/Desktop/phoneLogAnalysis/profile/keywordexcel/GMPKeywords.xls'
sfgpath = 'C:/Users/Desktop/phoneLogAnalysis/profile/sfg'
#输出路径
outputpath  = 'C:/Users/Desktop/phoneLogAnalysis/out/'
#临时文件路径
pkgnamepath = 'C:/Users/Desktop/phoneLogAnalysis/temp/pkgname.txt'
outxlstemp  = 'C:/Users/Desktop/phoneLogAnalysis/temp/outtemp.xls'

#  --- 获取指定目录下的所有指定后缀的文件名---
def getFileName(filePath):
    f_list = os.listdir(filePath)
    logname = []
    logfile = []
    outputfile = []
    flag=0
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.log':
            logfile.append(filePath+i)
            outputfile.append(filePath+'out/'+i)
            #logname.append(os.path.splitext(i)[0])
            logname.append(i)
            flag=flag+1
    return logfile,outputfile,logname,flag

#  --- 获取keywordfile数据 ---
def open_excel(keywordfile):
    try:
        data = xlrd.open_workbook(keywordfile)
        return data
    except Exception as e:
        print(e)

#  --- 根据索引获取Excel表格中的数据   参数:keywordfile：Excel文件路径    rownameindex：表头行名所在行的索引  ，by_index：表的索引 ---
def excel_table_byindex(keywordfile,rownameindex=0,by_index=0):
    data = open_excel(keywordfile)
    table = data.sheets()[by_index]
    rows = table.nrows #获取行数
    list =[]
    for rownum in range(0,rows):
        row = table.row_values(rownum)
        list.append(row)
    return list

#  --- 通过keyword1，keyword2搜索log，输出结果到文本 参数：item：测试项目名---
def search_keyword(logname,item,keyword1,keyword2=''):
    logfile=filePath+logname
    cpoylogfile=outputpath+logname
    nowt = time.strftime("%Y%m%d", time.localtime()) 
    outputfile=filePath+'out/'+nowt+'/'+'filter_'+logname
    with codecs.open(logfile, 'r', 'utf8') as f_in, codecs.open(outputfile, 'a','utf8') as f_out:
        f_out.write('\n' + item + '\n')
        list=[]        
        for line in f_in:  
            line = line.strip()
            if (keyword1 in line) and (keyword2 in line) :
                f_out.write(line + '\n')
                list.append(line)
    return list

#  --- jsonkeyword搜索结果输入表格---   
def jsonkeyword_out(filename,item,keyword1,json_keyword,keyword2=''):
    #outputfile=filePath+'out/'+filename
    outputfile=filePath+filename
    getWord=''
    getWord1=''
    # 开始标识
    startSign='"'+ json_keyword+ '":'
    # 结束标识
    endSign1=','   
    endSign2='}' 
    endSign3=']'
    with codecs.open(outputfile, 'r', 'utf8') as file02:
        list=[]
        for line in file02.readlines():    
            #line = line.encode("utf8")    
            line = line.strip()
            if (keyword1 in line) and (keyword2 in line) :
                #  --- 判断开始标识是否存在于当前行中 ---
                if startSign in line:
                    #  --- 进行字符串的切割 ---
                    startIndex = line.index(startSign)
                    if startIndex >= 0:
                        startIndex += len(startSign)
                    getWord1=line[startIndex:].strip()
                    if getWord1[0]=='[':
                        endIndex=getWord1.find(endSign3) 
                    elif endSign1 in getWord1:
                        endIndex=getWord1.find(endSign1)
                    elif endSign2 in getWord1:
                        endIndex=getWord1.find(endSign2)
                    getWord=getWord1[0:endIndex]
                    #去掉空格,'',[,等符号
                    getWord=getWord.strip()
                    getWord=getWord.strip('[')  
                    getWord=getWord.strip('"')                    
    return getWord
   
#  --- keyword搜索结果输入表格---      
def keyword_out(logname,list,table):
    data = open_excel(keywordfile)
    datacopy = copy(data)
    tableout = datacopy.get_sheet(0)
    rows = table.nrows #获取行数       
    itemnum = 1 #excel表格 keyword定位，item所在的列，1表示第2列
    for rownum in range(1,rows):       
        item=list[rownum][itemnum]
        keyword1=list[rownum][itemnum+1]
        keyword2=list[rownum][itemnum+2]
        json_keyword=list[rownum][itemnum+3]
        #json_keyword为空则out为keyword1,keyword2的搜索结果
        if json_keyword=='' :
            colnum=itemnum+6
            outline=search_keyword(logname,item,keyword1,keyword2)
            try:
                for num in range(0,len(outline)):
                    #tableout.write(rownum,colnum+num,outline[num])
                    tableout.write(rownum,colnum,'见filter_pkgname.log文件')              
            except Exception as e:
                print(e)   
        #json_keyword不为空则out为json_keyword的搜索结果               
        else :
            colnum=itemnum+7
            outline=jsonkeyword_out(logname,item,keyword1,json_keyword,keyword2)
            getlen=len(outline)
            if getlen>3:
               getlen=3 
            try:
                for num in range(0,getlen):
                    tableout.write(rownum,colnum+num,outline)
            except Exception as e:
                print(e)        
    datacopy.save(outxlstemp)

#  --- 设置单元格字体颜色---      
def style_red():
    font0 = xlwt.Font()
    font0.colour_index = 2
  
    style0 = xlwt.XFStyle()
    style0.font = font0    
    
    return style0

#  --- jsonout compare结果输入表格---        
def compareout(list,table,logname):        
    logname=logname.strip('.log')+'.xls'
    data = open_excel(outxlstemp)
    datacopy = copy(data)
    tableout = datacopy.get_sheet(0)
    rows = table.nrows #获取行数   
    colnum=6  
    compare_result=''  
    
    for rownum in range(1,rows):
        json_out=str(list[rownum][8])
        compare=str(list[rownum][5]).strip()
        if compare=='':  
            compare_result=''  
        else: 
            compare_result=''          
            if compare in json_out:
                compare_result='T'
                tableout.write(rownum,colnum,compare_result)
            else:
                compare_result='F'
                tableout.write(rownum,colnum,compare_result,style_red())
    nowt = time.strftime("%Y%m%d", time.localtime()) 
    datacopy.save(outputpath+nowt+'/'+logname)
  
#  --- jsonkeyword搜索结果输入表格---   
def out(keywordfile,logname):
    data = open_excel(keywordfile)
    table = data.sheets()[0]
    list1 = excel_table_byindex(keywordfile,0,0)
    keyword_out(logname,list1,table)
    print('---keyword1、2搜索已完成---')
    print('---json keyword搜索已完成---')
    list3 = excel_table_byindex(outxlstemp,0,0)
    compareout(list3,table,logname)    
    print('---json数据对比已完成---')
    
#  --- 删除文件---
def delete_file(path='C:/Users/mobif/Desktop/LogAnalysis/out/out.xls'):
    if os.path.exists(path):
        os.remove(path) 
        
#  --- 删除上一次测试数据---     
def delete_file_folder(src):
    if os.path.exists(src):        
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc=os.path.join(src,item)
                delete_file_folder(itemsrc) 
    else:
        os.makedirs(src)
        
def LogAnalysis():    
    nowt = time.strftime("%Y%m%d", time.localtime()) 
    delete_file_folder(outputpath+nowt) 
    print(outputpath+nowt+'中上次测试数据已删除')
    logfile,outputfile,logname,flag=getFileName(filePath)
    print(filePath+'文件夹中包含的log文件有%d个：' % flag)
    print(logname)
     
    for i in range(0,flag):
        name=str(logname[i])
        print('*****开始处理第%d个log：'% (i+1) +name+'*****' )
        try:    
            out(keywordfile,name)
        except Exception as e:
            print(e)
            logging.exception(e)
            print('分析'+name+'失败')   
        delete_file(outxlstemp)
        print(name+'处理完成')
        print('')

#  --- 获取apk包名 ---
def getPKGName(filePath):
    f_list = os.listdir(filePath)
    pkgname = ''
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.apk':
            pkgname = os.path.splitext(i)[0]
            print('当前处理的包名为：'+pkgname)
            break
    with open(pkgnamepath, 'w') as f_pkg:
        f_pkg.write(pkgname)
    return pkgname

    
if __name__=="__main__":
    #获取测试的apk包名
    pkgname=getPKGName(filePath)

    i=0
    for i in range(0,100):
        #从手机中获取指定应用的log      
        print('----从'+phonepath + pkgname+'/files/'+pkgname+'.log '+'获取log'+'----')
        os.system('adb pull '+phonepath + pkgname+'/files/'+pkgname+'.log ' + filePath)
        
        i=i+1
        #按规则分析log
        LogAnalysis()
        print('第%d轮处理完成' % i)
        print('----------------------------------------------------------------')
        input('按回车键再次从手机获取log')

    input('log刷新次数已达到最大，按回车键退出脚本')
