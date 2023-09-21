#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime


# 传入一个时间字符串，如果该字符串的分和秒对应位置大于等于60，则向上进位；如果小于0，则向下进位，时分秒如果均小于0，则强制取0，最后返回符合要求的时间字符串
def solvedCarry(timeStr):
    tmpList = timeStr.split(":")
    hourStr = tmpList[0]
    minStr = tmpList[1]
    seconedStr = tmpList[2]
    hourInt = int(hourStr)
    minInt = int(minStr)
    seconedFloat = float(seconedStr)

    # 处理秒数
    if seconedFloat < 0:
        carryNum = int(abs(int(seconedFloat)) / 60) + 1
        seconedFloat = seconedFloat + (60.0 * carryNum)
        minInt = minInt - carryNum
    elif seconedFloat >= 60:
        carryNum = int(int(seconedFloat) / 60)
        seconedFloat = seconedFloat - (60.0 * carryNum)
        minInt = minInt + carryNum
    else:
        pass

    # 处理分钟数
    if minInt < 0:
        carryNum = int(abs(minInt) / 60) + 1
        minInt = minInt + (60 * carryNum)
        hourInt = hourInt - carryNum
    elif minInt >= 60:
        carryNum = int(minInt / 60)
        minInt = minInt - (60 * carryNum)
        hourInt = hourInt + carryNum
    else:
        pass

    if hourInt < 0:
        # 当最终计算导致小时为负数时，强制将时间轴归零
        hourInt = 0
        minInt = 0
        seconedFloat = 0.00
    else:
        pass

    # 构建时间字符串
    seconedStr = "{:0>.2f}".format(seconedFloat)
    seconedStr = "{:0>5}".format(seconedStr)
    minStr = "{:0>2}".format(minInt)
    hourStr = "{0}".format(hourStr)
    tmpList = [hourStr, minStr, seconedStr]
    reTimeStr = ":".join(tmpList)
    return reTimeStr


# 调整秒速
def addS(timeStr, addS):
    tmpList = timeStr.split(":")
    minStr = tmpList[1]
    minInt = int(minStr)
    secondStr = tmpList[2]
    addFloat = float(tmpList[2]) + addS

    addStr = "{:0>.2f}".format(addFloat)
    addStr = "{:0>5}".format(addStr)
    tmpList[2] = addStr
    solvedTimeStr = ":".join(tmpList)
    finalTimeStr = solvedCarry(solvedTimeStr)
    return finalTimeStr


# 使用前需要修改的变量
inputFolder = r"E:\pycharm project\new\ass"  # 要输入的字幕文件的保存文件夹
addSInt = -120  # 要整体移动的秒速，正数为加，负数为减
supportedSuffixList = [".ass"]  # 支持的字幕后缀名
assContentStartStr = "Dialogue:"  # 表示要处理的时间轴部分的前缀
outputParentFolder = "结果"  # 保存生成ass文件的文件夹名

nowSaveFolerName = datetime.datetime.now().strftime("%Y%m%d-%X").replace(":", "")
saveFolderPath = os.path.join(os.getcwd(), outputParentFolder, nowSaveFolerName)
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

        with open(filePath, "r", encoding="utf-8") as fr:
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
