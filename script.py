#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import zlib, base64
from ICM20948 import *


class Encryptor:
    def __init__(self, key):
        self.key = key
    
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname == 'script.py' or fname == 'ICM20948.py' or fname == 'compare.py'):
                    continue
                else:
                    dirs.append(dirName + "/" + fname)
        return dirs
    
    #Used to test individually
    def getUnencyptedFiles(self):
        dirs = []
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt')
        return dirs

    #used to test individually 
    def getEncyptedFiles(self):
        dirs = []
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt.enc')
        return dirs

    def encrypt_all_files(self):
        start = time.time()
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)
        stop =time.time()
        print('Encryption time: '+ str(stop-start))

    def decrypt_all_files(self):
        start = time.time()
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)
        stop =time.time()
        print('Decryption time: '+ str(stop-start))




class Compressor:
    def __init__(self):
        pass
    
    def compress_file(self, file_name):
        file_to_compress = open(file_name, 'r')
        text = file_to_compress.read()
        file_to_compress.close()
        compressed = base64.b64encode(zlib.compress(text.encode("utf-8"),7))
        compressed = compressed.decode("utf-8")
        compressed_file = open(file_name,"w")
        compressed_file.write(compressed)
        compressed_file.close()

    def decompress_file(self, file_name):
        file_to_decompress = open(file_name, 'r')
        text = file_to_decompress.read()
        file_to_decompress.close()
        decompressed =zlib.decompress(base64.b64decode(text.encode("utf-8")))
        decompressed_file = open(file_name,"w")
        decompressed_file.write(decompressed.decode("utf-8"))
        decompressed_file.close()
    
    
    def compress_all_files(self):
        start = time.time()
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.compress_file(file_name)
        stop =time.time()
        print('Compression time: '+ str(stop-start))

    def decompress_all_files(self):
        start = time.time()
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decompress_file(file_name)
        stop =time.time()
        print('Decompression time: '+ str(stop-start))
    
    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_50.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt')
        #for dirName, subdirList, fileList in os.walk(dir_path):
        #    for fname in fileList:
        #        if (fname == 'script.py' or fname == 'ICM20948.py' or fname == 'compare.py'):
        #            continue
        #        else:
        #            dirs.append(dirName + "/" + fname)
        return dirs
    
    def getUnencyptedFiles(self):
        dirs = []
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt')
        return dirs
    
    def getEncyptedFiles(self):
        dirs = []
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt.enc')
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt.enc')
        return dirs



class Comparator:
    def __init__(self):
        pass

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        #dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_50.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_500.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1000.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_1500.txt')
        dirs.append('/home/pi/Documents/3097/EEE3097S-2021-Group6/data_2000.txt')
        return dirs

    def get_preprocess(self):
        self.pretext = ""
        dirs = self.getAllFiles()
        for file_name in dirs:
            with open (file_name, 'r') as myFile:
                content1 = myFile.read()
            self.pretext += content1
            myFile.close()
    
    def get_postprocess(self):
        self.posttext = ""
        dirs = self.getAllFiles()
        for file_name in dirs:
            with open (file_name, 'r') as myFile:
                content2 = myFile.read()
            self.posttext += content2
            myFile.close()
             
    
    def compare(self):
        if self.pretext == self.posttext:
            print('File is the same after decryption and decompression')
        else:
            print('There was loss after decryption and decompression')






key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
com = Compressor()
cmp = Comparator()
clear = lambda: os.system('clear')

cmp.get_preprocess()
clear()

while True:
        #clear()
        choice = int(input(
            "1. Press '1' to record samples.\n"+
            "2. Press '2' to compress all files in the directory.\n"+
            "3. Press '3' to encrypt all files in the directory.\n"+
            "4. Press '4' to decrypt all files in the directory.\n"+
            "5. Press '5' to decompress all files in the directory.\n"+
            "6. Press '6' to compare pre-compression/encryption to post-decryption/decompression.\n"+
            "7. Press '7' to exit.\n"))
        clear()
        if choice == 1:
            num_samples = int(input(
                "Enter number of samples to record in batch: "))
            print("Recording...")
            data = sample_data(num_samples)
            with open("data_"+str(num_samples)+".txt", "w") as text_file:
                text_file.write(str(data))
            text_file.close()
            print("Done")
            time.sleep(1)
        if choice == 2:
            com.compress_all_files()
        elif choice == 3:
            enc.encrypt_all_files()
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            com.decompress_all_files()
        elif choice == 6:
            cmp.get_postprocess()
            cmp.compare()
        elif choice == 7:
            exit()
        else:
            print("Please select a valid option!")