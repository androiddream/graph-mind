# -*- coding: UTF-8 -*-

'''
Created on 2016年1月9日

@author: hylovedd
'''
import xml
from xml.etree import ElementTree

from bs4 import BeautifulSoup

from org_ailab_seg.extraSegOpt import extraSegOpt
from org_ailab_seg.wordSeg import wordSeg


class segSentiWbTest:
    # analysis nlpcc2014 dateset
    def __init__(self, filePath):
        self.filePath = filePath
    
    def fetchParaText(self):
        fileObj = open(self.filePath)
        paraTextList = []
        try:
            fileAllText = fileObj.read()
            
            soup = BeautifulSoup(fileAllText)
            soupEles = soup.find_all('review')
            for ele in soupEles:
                paraTextList.append(ele.get_text().encode('utf-8'))
        finally:
            fileObj.close()
            
        print('textNum:' + str(len(paraTextList)))
        
        return paraTextList
    
    def fetchXMLText(self):
        root = ElementTree.parse(self.filePath)
        sentences = root.getiterator('sentence')
        
        posSentences = []
        negSentences = []
        other = []
        allTextNum = 0
        for sentence in sentences:
            allTextNum += 1
            if sentence.get('opinionated') == 'Y':
                if sentence.get('emotion-1-type') == 'happiness' or sentence.get('emotion-1-type') == 'like':
                    posSentences.append(sentence.text)
                elif sentence.get('emotion-1-type') == 'anger' or sentence.get('emotion-1-type') == 'disgust' or sentence.get('emotion-1-type') == 'sadness':
                    negSentences.append(sentence.text)
                else:
                    other.append(sentence.text)
            else:
                other.append(sentence.text)
        
        print('allTextNum:' + str(allTextNum))            
        print('posTextNum:' + str(len(posSentences)))
        print('negTextNum:' + str(len(negSentences)))
        print('other:' + str(len(other)))
        
        
        return posSentences, negSentences
    
    def segParaText(self, segMode):
        paraTextList = self.fetchParaText()
        testSeger = wordSeg(segMode, paraTextList)
        
        segParaList = testSeger.serialSeger()
        
        return segParaList

if __name__ == '__main__':
    filePath = u"NLPCC2014.xml"
    segObj = segSentiWbTest(filePath)
    
    posSentences, negSentences = segObj.fetchXMLText()
    allSentences = posSentences
    allSentences.extend(negSentences)
    wordSegObj = wordSeg('a', allSentences)
    segParaList = wordSegObj.serialSeger(True)
    extraSegOptObj = extraSegOpt()
    avgWordsNum = extraSegOptObj.conutAvgWordsNum(segParaList)
    
    print(avgWordsNum)
    
    writePath = u'segNLPCC2014.txt'
    extraSegOptObj.writeIntoFile(writePath, segParaList)
