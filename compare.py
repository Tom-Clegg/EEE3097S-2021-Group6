import zlib, base64, time, sys, os


def compress(file, level):
    file1 = open(file,"r")
    text = file1.read()
    file1.close()

    start = time.time()
    compressed =base64.b64encode(zlib.compress(text.encode("utf-8"),level))   
    compressed = compressed.decode("utf-8")
    file1 = open("compressed.csv","w")
    file1.write(compressed)
    stop =time.time() 
    file1.close()
    print(level , "has compression speed of", os.path.getsize(file)/((stop-start)*1024), " it took ", stop-start , "compression ratio ", os.path.getsize(file)/os.path.getsize("compressed.csv"), " size of uncompressed file is ", os.path.getsize(file)/1024, "size of compressed is ", os.path.getsize("compressed.csv")/1024)
def decompress(file):
    file2 = open(file,"r")
    text = file2.read()
    file2.close()

    start =time.time()
    decompressed = zlib.decompress(base64.b64decode(text.encode("utf-8")))
    stop =time.time()
    print("decompression took ", stop-start)
    
    file2 = open("decompressed.csv","w")
    file2.write(decompressed.decode("utf-8"))
    file2.close()
    
def comparison(original, decompressed): 
    file1 = open(original, 'r')
    file2 = open(decompressed, 'r')
    og = file1.readlines() 
    dc = file2.readlines() 
    file1.close() 
    file2.close() 

    diff=0 #registers differences
    line=0 #current line
    
    for i in og: 
        if i != dc[line]: 
            diff=diff+1 
            line=line+1 
            
    print("registered differences are ", diff)
    
compress("2018-09-19-09_49_31_VN100.csv",3)
df1=pd.read_excel('2018-09-19-09_49_31_VN100.csv')
df2=pd.read_excel('compressed.csv')
print(df1.equals(df2))


