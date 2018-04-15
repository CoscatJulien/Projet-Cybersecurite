import string
import itertools
import sys
import os
fileName = 'PH.txt'
filePath = "/opt/projet-cyberscurite/documents_chiffres/%s" % (fileName)
reference = open('/opt/projet-cyberscurite/documents_chiffres/liste_francais.txt', 'r', errors='ignore').read().split('\n')


def readFile(filePath):
    message = []
    dataFile = open(filePath, 'rb').read()
    for char in dataFile:
        message.append(bin(int(char)))
    return message
# return a list of hex 

def hexTranslator(listMessage):
    binListMessage = []
    binListOutput = []
    for data in listMessage:
        binListMessage.append(bin(int(data, 0)))
    for binData in binListMessage:
        if len(binData[2:]) < 8:
            data = binData[2:]
            bitToAdd = 8 - len(binData[2:])
            for i in range (0, bitToAdd):
                data = '0%s' % (data)
            binListOutput.append(data)
        else : 
            binListOutput.append(binData[2:])
    return binListOutput
# return the message as a list of 8 bits string

def getDataInterval(message, interval):
    dataInterval = []
    x = interval
    for i in range(0, (int(len(message) / 6))):
        try:
            dataInterval.append(message[x])
            x = x + 6
        except:
            print('list index out of range : message[%s]' % (i))
    return dataInterval
# return a list of 8 bit string on a defined interval

def binAdder(bitString):
    data = ''
    if len(bitString) < 8:
        bitToAdd = 8 - len(bitString)
        for i in range (0, bitToAdd):
            data += '0'
        output = data + bitString
    else : 
        output = bitString
    return output

def getDataStats(message):
    occurence = []
    datas = set(message)
    i = 0
    for data in datas:
        occurence.append([message.count(str(data)), data])
        i = i + 1
    return sorted(occurence, reverse = True)
# return a list with [occurenceNb, 8 bit string]

def xorCryptor(data, key):
    result = []
    for i in range (0, 8):
        result.append(int(data[i]) ^ int(key[i]))
    return result
# return a list of 8 bit string

def fileXorDecryptor(dataFile, key):
    listKey = []
    decrypted = []
    x = 0
    y = 0
    for i in range(0, len(dataFile)):
        if x < 6:
            try:
                listKey.insert(i, key[x])
                x = x + 1
            except:
                print('index out of range')
        else :
            x = 0
            listKey.insert(i, key[x])
            x = x + 1
    for word in dataFile:
        decrypted.append(xorCryptor(word, listKey[y]))
        y = y + 1
    return decrypted
# return a list of 8 bit string


def checkDict(texte, reference):
    french = 0
    for word in reference:
        if word in texte:
            french = french + 1
    return french

            



if __name__ == "__main__":
    key = ''
    bitKey = []
    messageDechiffre = ''
    bitMessageList = []
    datas = readFile(filePath)
    espace = binAdder(''.join(format(ord(' '), 'b')))
    for i in range(0, 6):
        bitString = ''
        dataInterval = getDataInterval(hexTranslator(datas), i)
        dataStats = getDataStats(dataInterval)
        for char in xorCryptor(dataStats[0][1], espace):
            bitString += str(char)
        bitKey.append(bitString)
        key += chr(int(bitString, 2))
    for word in fileXorDecryptor(hexTranslator(datas), bitKey):
        bitMessageList.append(''.join(str(x) for x in word))
    for finalWord in bitMessageList:
        try:
            sys.stdout = open(os.devnull, 'w')
            print(chr(int(finalWord.encode('ascii', 'ignore'), 2)))
            sys.stdout = sys.__stdout__
            messageDechiffre += chr(int(finalWord.encode('utf-8'), 2))
        except:
            continue
    langue = checkDict(messageDechiffre.split(' '), reference)
    if langue > 100:
        messageDechiffreFile = open("decrypted-%s" % (fileName), "w")
        messageDechiffreFile.write(messageDechiffre)
        messageDechiffreFile.close()
        print('message %s dechiffre dans decrypted-%s' % (fileName, fileName))
    else : 
        print('could not find the key')
