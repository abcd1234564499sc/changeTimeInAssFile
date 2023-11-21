#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime


def addS(timeStr, addS):
    tmpList = timeStr.split(":")
    minStr = tmpList[1]
    minInt = int(minStr)
    secondStr = tmpList[2]
    addFloat = float(tmpList[2]) + addS
    # 判断是否需要进位
    if addFloat >59:
        # 分位进一位
        minInt = minInt+1
        addFloat = addFloat-60
    elif addFloat<0:
        # 分位退一位
        minInt = minInt -1
        addFloat = addFloat+60
        if minInt<0:
            minInt=0
    
    addStr = "{:0>.2f}".format(addFloat)
    addStr = "{:0>5}".format(addStr)
    tmpList[2] = addStr
    minStr = "{:0>2}".format(minInt)
    tmpList[1] = minStr
    return ":".join(tmpList)

# 使用前需要修改的变量
inputFolder = r"H:\ceshi"    # 要输入的字幕文件的保存文件夹
addSInt = 1    # 要整体移动的秒速，正数为加，负数为减
supportedSuffixList = [".ass"]    # 支持的字幕后缀名
assContentStartStr = "Dialogue:"    # 表示要处理的时间轴部分的前缀
outputParentFolder = "结果"       # 保存生成ass文件的文件夹名 
fileEncodeStrList = ["utf-8","utf-16"]           # 读取和保存文件的编码，一般尝试utf-8 和 utf-16
solvedType = 1                    # 处理文件的方式，0为保存到新的文件夹中，1为直接修改原始文件

nowSaveFolerName = datetime.datetime.now().strftime("%Y%m%d-%X").replace(":","")
saveFolderPath = os.path.join(os.getcwd(),outputParentFolder, nowSaveFolerName)
if not os.path.exists(saveFolderPath) and solvedType==0:
    os.makedirs(saveFolderPath)

fileNameList = os.listdir(inputFolder)

for fileIndex, fileName in enumerate(fileNameList):
    print("正在处理文件：{0}（{1}/{2}）".format(fileName, fileIndex + 1, len(fileNameList)))
    filePath = os.path.join(inputFolder, fileName)
    nowFileSuffix = os.path.splitext(fileName)[-1]
    if nowFileSuffix not in supportedSuffixList:
        print("非字幕后缀名,不进行处理\n")
        continue
    else:
        fileLines = []
        for fileEncodeIndex,fileEncodeStr in enumerate(fileEncodeStrList):
            try:
                with open(filePath, "r", encoding=fileEncodeStr) as fr:
                    fileLines = fr.readlines()
                break
            except:
                if fileEncodeIndex != len(fileEncodeStrList)-1:
                    continue
                else:
                    print("编码错误")
                    exit(0)
        print("读取到{}行输入".format(len(fileLines)))
        solvedLines = []
        
        if solvedType == 0:
            outputName = os.path.join(saveFolderPath, fileName)
            writeType = "w+"
        elif solvedType == 1:
            outputName = os.path.join(inputFolder, fileName)
            writeType = "w"
        
        with open(outputName, writeType, encoding=fileEncodeStr) as fr:
            for index, line in enumerate(fileLines):
                print("\r正在处理{0}/{1}行数据".format(index + 1, len(fileLines)), end="")
                solvedLine = ""
                if line[:len(assContentStartStr)] != assContentStartStr:
                    solvedLine = line
                else:
                    tmpList = line.split(",")
                    first = tmpList[1]
                    seconed = tmpList[2]
                    tmpList[1] = addS(first, addSInt)
                    tmpList[2] = addS(seconed, addSInt)
                    solvedLine = ",".join(tmpList)
                fr.write(solvedLine)
        print("处理完毕，结果输出为:{}\n".format(outputName))
