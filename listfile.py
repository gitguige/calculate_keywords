import glob,os
from sys import argv

#for file in glob.glob("*.py"):
#  print file

#for file in os.listdir("/mydir"):
#    if file.endswith(".txt"):
#        print(os.path.join("/mydir", file))



def calculate_keywords(pathwork,savefile):
        # if not pathwork:
        #         print "path is illeagel, exit."
        #         return

        fpkw = open("keywordlist.txt",'r')
        line = fpkw.readline()
        line = line.replace('\n','')
        line = line.split(',')
        fpkw.close()
        print line
        leng = len(line)

        wordlist = line
        for i in range(leng, 10):
                wordlist.append('null')

        # summFile = open("summary.csv",'w')
        savefile = savefile.replace('\n','')+'.csv'
        summFile = open(savefile,'w')
        summLine = 'Directory#,Filename#,Filetype#,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,Total#\n' %(wordlist[0],wordlist[1],wordlist[2],wordlist[3],wordlist[4],wordlist[5],wordlist[6],wordlist[7],wordlist[8],wordlist[9])
        summFile.write(summLine)
        
        # pathwork = '/home/gui/Documents/openpilot/1_openpilot/1_openpilot_LVSpConst_WOdocker/selfdrive/'#os.getcwd()
        for root, dirs, files in os.walk(pathwork):
                for file in files:
                        if file.endswith(".py") or file.endswith(".c") or file.endswith(".cpp"):
                                filetype = file.replace('\n','')
                                filetype = filetype.split('.')
                                filetype = filetype[len(filetype)-1]  

                                fileresult = os.path.join(root, file)
                                total_consist = 0
                                consist = [0,0,0,0,0,0,0,0,0,0]
                                fpcode = open(fileresult,"r")
                                for fline in fpcode:
                                        for index in range(leng):
                                                keyword = line[index]
                                                if consist[index] == 0 and keyword in fline:
                                                        if "while" in keyword or "for" in keyword: #while or for structure
                                                                if ('(' not in fline or ')' not in fline) and (':' not in fline): # not while() /while: /for() /for:
                                                                        continue
                                                        consist[index] = 1
                                                        total_consist += 1
                                                        # print fileresult + keyword
                                summLine = '%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' %(root,file,filetype,consist[0],consist[1],consist[2],consist[3],consist[4],consist[5],consist[6],consist[7],consist[8],consist[9],total_consist)
                                summFile.write(summLine)
        summFile.close()
                        #             os.system('cp '+ fileresult+ ' result1/')
                        # print(fileresult)

if __name__ == "__main__":
        calculate_keywords(argv[1],argv[2])