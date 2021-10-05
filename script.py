#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import zlib, base64


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
                if (fname != 'script.py'): # what files to not include
                    dirs.append(dirName + "\\" + fname)
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
    
    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'script.py'): # what files to not include
                    dirs.append(dirName + "\\" + fname)
        return dirs
    
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



class Comparator:
    def __init__(self):
        pass
    
    def get_preprocess(self, file_name):
        file_to_compress = open(file_name, 'r')
        self.pretext = file_to_compress.read()
        file_to_compress.close()
    
    def get_postprocess(self, file_name):
        file_to_compress = open(file_name, 'r')
        self.posttext = file_to_compress.read()
        file_to_compress.close()
    
    def compare(self):
        if self.pretext == self.posttext:
            print('File is the same after decryption and decompression')
        else:
            print('There was loss after decryption and decompression')






key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
com = Compressor()
cmp = Comparator()
clear = lambda: os.system('cls')

cmp.get_preprocess('2018-09-19-03_57_11_VN100.csv')

while True:
        #clear()
        choice = int(input(
            "1. Press '1' to compress all files in the directory.\n"+
            "2. Press '2' to encrypt all files in the directory.\n"+
            "3. Press '3' to decrypt all files in the directory.\n"+
            "4. Press '4' to decompress all files in the directory.\n"+
            "5. Press '5' to compare pre-compression/encryption to post-decryption/decompression.\n"+
            "6. Press '6' to exit.\n"))
        clear()
        if choice == 1:
            com.compress_all_files()
        elif choice == 2:
            enc.encrypt_all_files()
        elif choice == 3:
            enc.decrypt_all_files()
        elif choice == 4:
            com.decompress_all_files()
        elif choice == 5:
            cmp.get_postprocess('2018-09-19-03_57_11_VN100.csv')
            cmp.compare()
        elif choice == 6:
            exit()
        else:
            print("Please select a valid option!")