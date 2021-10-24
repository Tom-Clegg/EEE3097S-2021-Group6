import zlib, base64, time, sys, os

def compress(file, level):
    file1 = open(file,"r")
    text = file1.read()
    file1.close()

    start = time.time()
    compressed =base64.b64encode(zlib.compress(text.encode("utf-8"),level))
    stop =time.time()
    print(level, "compressed size took ", stop-start,"compression ratio ", os.path.getsize(file)/sys.getsizeof(compressed))
    
    compressed = compressed.decode("utf-8")

    file1 = open("compressed.txt","w")
    file1.write(compressed)
    file1.close()
    
def decompress(file):
    decompressed =zlib.decompress(base64.b64decode(text.encode("utf-8")))
    file2 = open(file,"r")
    text = file2.read()
    file2.close()

    start =time.time()
    decompressed = zlib.decompress(base64.b64decode(text.encode("utf-8")))
    stop =time.time()
    print("decompression took ", stop-start)
    
    file2 = open("decompressed.txt","w")
    file2.write(decompressed.decode("utf-8"))
    file2.close()
    
compress("data_2000.txt",7)
decompress("compressed.txt")