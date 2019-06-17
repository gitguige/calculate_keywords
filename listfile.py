import glob,os,math
from sys import argv
import pandas as pd

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
        # print (item)
        leng = len(item)
        # print (weight)
        wordlist = item
        # for i in range(leng, 20):
        #         wordlist.append('null')

        # summFile = open("summary.csv",'w')
        savefile = savefile.replace('\n','')#+'.csv'
        summFile = open(savefile,'w')
        # summLine = 'Directory#,Filename#,Filetype#,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,Total#\n' %(wordlist[0],wordlist[1],wordlist[2],wordlist[3],wordlist[4],wordlist[5],wordlist[6],wordlist[7],wordlist[8],wordlist[9])
        # summFile.write(summLine)

        summLine = 'Directory#,Filename#,Filetype#,Total_weight#,Total_count#'
        summFile.write(summLine)
        for i in range(leng):
                summLine =',%s' %wordlist[i]
                summFile.write(summLine)
        summLine = '\n'
        summFile.write(summLine)
        
        filewithcontrolloop = [0,'']
        # pathwork = '/home/gui/Documents/openpilot/1_openpilot/1_openpilot_LVSpConst_WOdocker/selfdrive/'#os.getcwd()
        # print(pathwork)
        for root, dirs, files in os.walk(pathwork):
                for file in files:
                        if file.endswith(".py") or file.endswith(".c") or file.endswith(".cpp"):
                                filetype = file.replace('\n','')
                                filetype = filetype.split('.')
                                filetype = filetype[len(filetype)-1]  

                                fileresult = os.path.join(root, file)

                                total_weight = 0 #recored the number of cases where the code matches the keywords
                                Total_count = 0 #recored the number of cases where the code matches the keywords
                                consist = ['']
                                for i in range(leng):
                                        consist.append('')
                                fpcode = open(fileresult,"r")
                                linenum = 0 # recorded the number of each line
                                for fline in fpcode:
                                        linenum += 1
                                        fline = fline.lower()
                                        for index in range(leng):
                                                keyword = wordlist[index]
                                                # if consist[index] == 0 and keyword in fline:
                                                if keyword in fline:
                                                        if "while" in keyword or "for" in keyword: #while or for structure
                                                                if ('(' not in fline or ')' not in fline) and (':' not in fline): # not while() /while: /for() /for:
                                                                        continue
                                                        Total_count += 1
                                                        if consist[index] == '':
                                                                total_weight += weight[index]
                                                                if total_weight > filewithcontrolloop[0]:
                                                                        filewithcontrolloop[0] =total_weight
                                                                        filewithcontrolloop[1] = root+'/ '+file
                                                                # print fileresult + keyword
                                                                consist[index] = 1
                                                        else:
                                                                consist[index] += 1#weight[index]#linenum#

                                # summLine = '%s,%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n' %(root,file,filetype,consist[0],consist[1],consist[2],consist[3],consist[4],consist[5],consist[6],consist[7],consist[8],consist[9],total_weight)
                                # summFile.write(summLine)
                                summLine = '%s,%s,%s,%d,%d' %(root,file,filetype,total_weight,Total_count)
                                summFile.write(summLine)
                                for i in range(leng):
                                        summLine =',%s' %consist[i]
                                        summFile.write(summLine)
                                summLine = '\n' 
                                summFile.write(summLine)
        print (filewithcontrolloop)

        summFile.close()

        data = pd.read_csv(savefile)
        data = data.set_index('Total_weight#')
        data = data.sort_index(ascending=False) #sort the table with index of Total#
        data.to_csv(savefile)
                        #             os.system('cp '+ fileresult+ ' result1/')
                        # print(fileresult)

def calculate_tfidf(cvsfile):
        cvsfile = cvsfile.replace('\n','')#+'.csv'
        fp = open(cvsfile,'r')
        title = fp.readline()
        # print (title)
        title = title.replace('\n','').split(',')
        del (title[0],title[0],title[0],title[0]) #delete the first 4 column
        # print (title)
        fp.close()

        data = pd.read_csv(cvsfile)
        data_bk =data
        keywordnum = len(title) 
        filenum = len(data[title[0]]) #how many row in the table file
        for i in range (1,keywordnum):
                keyword = title[i]
                count = data[keyword].count() #the number of files that a keywords is detected
                data_bk[keyword] = data[keyword]*1.0/data[title[0]]*math.log((filenum-1)/(1+count)) #tf*idf
                # for j in range(1,filenum):
                #         n = data[keyword][j]
                #         tf = n*1.0/data[title[0]][j]
                #         idf = 1.0*math.log((filenum-1)/(1+count))
                #         data_bk[keyword][j] = tf*idf
        data_bk = data_bk.set_index('Total_weight#')
        data_bk = data_bk.sort_index(ascending=False) #sort the table with index of Total#
        data_bk.to_csv('tfidf_'+cvsfile)


if __name__ == "__main__":
        calculate_keywords(argv[1],argv[2])
        calculate_tfidf(argv[2])