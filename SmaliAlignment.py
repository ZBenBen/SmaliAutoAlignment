# -*- coding: utf-8 -*-
#author:wenzhaoyan
#discribe:批量扫描指定的安卓原版smali目录和color修改版本的smali目录
#         对安卓smali的每个文件找出color中相同的并调用smali错位修改函数进行
#         method错误的修改，并写入修改log

import os,sys,fnmatch,io,shutil,filecmp,difflib,getopt,time

# ---------------------function()-------------------
def all_files(root,patterns='*',single_level=False,yield_folders=False):
    patterns=patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name,pattern):
                    yield os.path.join(path,name)
                    break
        if single_level:
            break

def filecompre(oppofilepath,androidfilepath,output,fileuri):
        try:
            oppofile=open(oppofilepath+fileuri,'r')
            androidfile=open(androidfilepath+fileuri,'r')
        except Exception as err:
            print(err)
            return "Can't Open the File"+oppofilepath+fileuri
        #定义opposmali和Androidsmali的method索引
        opponame=[]
        oppostart=[]
        oppoend=[]

        androidname=[]

        tmpoppo=[]
        i=0
        j=0
        #建立method名称 开始行和结束行的索引
        for line in oppofile:
            i=i+1
            tmpoppo.append(line)
            tt=[]
            if '.method ' in line:
                #识别method的名称，去掉权限修饰标志
                tt=line.strip('\n').split(' ')
                opponame.append(tt[-1])
                oppostart.append(i)
            if '.end method' in line:
                oppoend.append(i)
                j+=1
        opponum=j

        i=0
        j=0
        for line in androidfile:
            i+=1
            tt=[]
            if '.method ' in line:
                tt=line.strip('\n').split(' ')
                androidname.append(tt[-1])
        androidnum=j
        #创建临时文件用于错位修改输出
        #smali索引已经建立完毕,文件可以关闭了
        oppofile.close()
        androidfile.close()

        diff = difflib.Differ().compare(opponame,androidname)
        outlist=list(diff)
        count=0
        global ans  #判断method是否有错位 需要移动
        for line in outlist:
            #print(line)
            count+=1
            tmp=[]
            try:
                #先处理 - 号的
                if line[0] == '-':
                    for w in range(oppostart[count-1]-2,oppoend[count-1],1):
                        #
                        ww=tmpoppo[w]
                        tmpoppo[w]=''
                        tmp.append(ww)
                    tmpoppo.extend(tmp)
                    ans=1
                else:
                    if line[0] == '+':
                        ans=1
                        count-=1
                    else:
                        if line[0]=='?':
                            ans=1
                            count-=1
            except Exception as err:
                print(err)

        tmpname=[]
        tmpstart=[]
        tmpend=[]
        i=0
        for line in tmpoppo:
            i+=1
            tt=[]
            if '.method ' in line:
                tt=line.strip('\n').split(' ')
                tmpname.append(tt[-1])
                if ' virtual ' in tmpoppo[i-2]:
                    #found a double empty
                    if len(tmpoppo[i-3]) > 1:
                        tmpstart.append(i)
                    else:
                        if len(tmpoppo[i-4]) > 1:
                            tmpstart.append(i-1)
                        else:
                            tmpstart.append(i-2)
                else:
                    tmpstart.append(i)
            if '.end method' in line:
                tmpend.append(i)

        diff = difflib.Differ().compare(tmpname,androidname)
        outlist=list(diff)

        #接下来处理 + 号的
        i=0
        cout=0

        #建立最终输出
        try:
            outoppo=[]
            outoppo.extend(tmpoppo[0:tmpstart[0]-2])
        except Exception as err:
            #Method list is empty)
            outoppo.extend(tmpoppo)

        check=[]
        for line in outlist:
            if line[0]=='+':
                j=0
                ans=1
                count=0
                for t in outlist:
                    count+=1
                    if t[0] != '+':
                        j+=1
                    if t[0] == '-':
                        if t[1:] == line[1:]:
                            outoppo.extend(tmpoppo[tmpstart[j-1]-2:tmpend[j-1]])
                            check.append(count)

            else:
                if line[0] == ' ':
                    i+=1
                    try:
                        outoppo.extend(tmpoppo[tmpstart[i-1]-2:tmpend[i-1]])
                    except Exception as err:
                            print('最后输出错误：'+output+fileuri)
                            print(err)

        if ans ==0:
            return ('need no change')

        i=0
        j=0
        for line in outlist:
            j+=1
            #print(line)
            if line[0]!='+' and line[0] != '?':
                i+=1
            if line[0]=='-':
                if j not in check:
                    #print('not in'+str(j))
                    try:
                        outoppo.extend(tmpoppo[tmpstart[i-1]-2:tmpend[i-1]])
                    except:
                        print('List num error')
                        print('file:'+output+fileuri)
                        print(line)

        #最后输出outoppo
        print('output file: '+output+fileuri)
        outfile=open(output+fileuri,'w')
        outfile.writelines(outoppo)
        outfile.close()

# -------------------main()-------------------------
try:
    opionns,args=getopt.getopt(sys.argv[1:],"ha:c:o:")
    andrdidURI="android"
    colorURI="smali_framework"
    output="out"
    for op,value in opionns:
        if op == "-a":
            andrdidURI=value
        if op == "-c":
            colorURI=value
        if op == "-o":
            output=value
        if op == "-h":
            print('*** Help Info:')
            print('*** The script need three parameters. They are:')
            print('*** -a the AndroidSmali filepath ')
            print('*** -c the ColorSmali filepath ')
            print('*** -o the OutputSmali filepath (this path must be non-existent)')
            print('*** commond example: ')
            print('*** python SmaliAlignment.py -a Android_Smali -c Color_Smali -o Out_Samli')
            print('*** The filepath can input two types: F:\Smali\Android_Smali or Android_Smali')
            print('*** If yor use the second one. you must put this script in the same path with the smali folder')
            sys.exit()
except Exception as err:
    print('*** Help Info:')
    print('*** The script need three parameters. They are:')
    print('*** -a the AndroidSmali filepath ')
    print('*** -c the ColorSmali filepath ')
    print('*** -o the OutputSmali filepath (this path must be non-existent)')
    print('*** commond example: ')
    print('*** python SmaliAlignment.py -a Android_Smali -c Color_Smali -o Out_Samli')
    print('*** The filepath can input two types: F:\Smali\Android_Smali or Android_Smali')
    print('*** If yor use the second one. you must put this script in the same path with the smali folder')
    sys.exit()
##############################
if os.path.exists(output):
    print('*** Sorry, the output folder is existent')
    print('*** Please change the output folder or delete the exitent one')
else:
    if os.path.exists(colorURI) and os.path.exists(andrdidURI):
        #复制输出文件
        print('Prepare to alignment smali files.')
        shutil.copytree(colorURI,output)
        print('Begin to output.')
        i=0
        j=0
        android=[]
        for path in all_files(andrdidURI,'*.smali'):
            android.append(str(path[len(andrdidURI)::]))
        print("finish file search")
        logfile=open("Smali_Alignment_Log.txt",'a')
        logfile.write("\n")
        logfile.write("\n")
        logfile.write("\n")
        logfile.write("\n")
        logfile.write(time.strftime('%m-%d %H:%M:%S'))
        logfile.write("\n***************************************************\n")
        logfile.write("***************************************************\n")
        logfile.write("File Change Log:\n")
        global ans
        for line in android:
            ans=0
            filecompre(colorURI,andrdidURI,output,line.strip('\n'))
            if ans == 1:
                logfile.write(colorURI+line.strip('\n')+'\n')
        logfile.close()
        print('*******************')
        print('Alignment fisished!')
        print('*******************')
    else:
        print('\n*** Sorry, Wrong Smali Path, Please Recheck the filepath or your commond.')
        print('*** commond example: ')
        print('*** python SmaliAlignment.py -a Android_Smali -c Color_Smali -o Out_Samli')
        print('***  Color_Smali  path: '+colorURI)
        print('*** Android_Smali path: '+andrdidURI)
        print('*** If you need help, please run script like this:')
        print('*** python SmaliAlignment.py -h')