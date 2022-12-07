#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime


def addS(timeStr, addS):
    tmpList = timeStr.split(":")
    secondStr = tmpList[2]
    addFloat = float(tmpList[2]) + addS
    addStr = "{:0>.2f}".format(addFloat)
    addStr = "{:0>5}".format(addStr)
    tmpList[2] = addStr
    return ":".join(tmpList)

# 使用前需要修改的变量
inputFolder = r"C:\Users\Desktop\ori\5"    # 要输入的字幕文件的保存文件夹
addSInt = -1    # 要整体移动的秒速，正数为加，负数为减
supportedSuffixList = [".ass"]    # 支持的字幕后缀名
assContentStartStr = "Dialogue:"    # 表示要处理的时间轴部分的前缀
outputParentFolder = "结果"       # 保存生成ass文件的文件夹名

nowSaveFolerName = datetime.datetime.now().strftime("%Y%m%d-%X").replace(":","")
saveFolderPath = os.path.join(os.getcwd(),outputParentFolder, nowSaveFolerName)
if not os.path.exists(saveFolderPath):
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

        with open(filePath, "r", encoding="utf-16") as fr:
            fileLines = fr.readlines()
        print("读取到{}行输入".format(len(fileLines)))
        solvedLines = []
        outputName = os.path.join(saveFolderPath, fileName)
        with open(outputName, "w+", encoding="utf-8") as fr:
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
