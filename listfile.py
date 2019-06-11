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
        item = []
        weight = []
        fpkw = open("keywordlist.txt",'r')
        for line in fpkw:
                # line = fpkw.readline()
                line = line.replace('\n','')
                line = line.split(',')
                item.append(line[0])
                weight.append(int(line[1]))
        fpkw.close()
        print item
        leng = len(item)
        print weight
        wordlist = item
        # for i in range(leng, 20):
        #         wordlist.append('null')

        # summFile = open("summary.csv",'w')
        savefile = savefile.replace('\n','')+'.csv'
        summFile = open(savefile,'w')
        # summLine = 'Directory#,Filename#,Filetype#,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,Total#\n' %(wordlist[0],wordlist[1],wordlist[2],wordlist[3],wordlist[4],wordlist[5],wordlist[6],wordlist[7],wordlist[8],wordlist[9])
        # summFile.write(summLine)

        summLine = 'Directory#,Filename#,Filetype#,Total#,'
        summFile.write(summLine)
        for i in range(leng):
                summLine ='%s,' %wordlist[i]
                summFile.write(summLine)
        summLine = '\n'
        summFile.write(summLine)
        
        # pathwork = '/home/gui/Documents/openpilot/1_openpilot/1_openpilot_LVSpConst_WOdocker/selfdrive/'#os.getcwd()
        for root, dirs, files in os.walk(pathwork):
                for file in files:
                        if file.endswith(".py") or file.endswith(".c") or file.endswith(".cpp"):
                                filetype = file.replace('\n','')
                                filetype = filetype.split('.')
                                filetype = filetype[len(filetype)-1]  

                                fileresult = os.path.join(root, file)
                                total_consist = 0 #recored the number of cases where the code matches the keywords
                                consist = [0]
                                for i in range(leng):
                                        consist.append(0)
                                fpcode = open(fileresult,"r")
                                linenum = 0 # recorded the number of each line
                                for fline in fpcode:
                                        linenum += 1
                                        fline = fline.lower()
                                        for index in range(leng):
                                                keyword = wordlist[index]
                                                if consist[index] == 0 and keyword in fline:
                                                # if keyword in fline:
                                                        if "while" in keyword or "for" in keyword: #while or for structure
                                                                if ('(' not in fline or ')' not in fline) and (':' not in fline): # not while() /while: /for() /for:
                                                                        continue
                                                        consist[index] = linenum#weight[index]
                                                        total_consist += weight[index]
                                                        # print fileresult + keyword
                                # summLine = '%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' %(root,file,filetype,consist[0],consist[1],consist[2],consist[3],consist[4],consist[5],consist[6],consist[7],consist[8],consist[9],total_consist)
                                # summFile.write(summLine)
                                summLine = '%s,%s,%s,%d,' %(root,file,filetype,total_consist)
                                summFile.write(summLine)
                                for i in range(leng):
                                        summLine ='%d,' %consist[i]
                                        summFile.write(summLine)
                                summLine = '\n' 
                                summFile.write(summLine)

        summFile.close()
                        #             os.system('cp '+ fileresult+ ' result1/')
                        # print(fileresult)

if __name__ == "__main__":
        calculate_keywords(argv[1],argv[2])