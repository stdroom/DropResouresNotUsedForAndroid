#!/usr/bin/env python
#coding=utf-8
#leixun33@163.com
#qq: 378640336

"""
    删除Android项目中无用的png文件
"""

import os,sys,re

findstr='';
findDrawable=[];
findFilePath=[];

# Java class文件中使用的drawable资源
java_drawableMatch='(?<=R.drawable.)[a-z|_|0-9|A-Z]*';
# 布局文件、选择器、主题等xml文件中使用的drawable资源
layout_drawableMatch='(?<=drawable\/)[a-z|_|A-Z|0-9|-]*(?=[\s]*\")';
# 路径中的png文件匹配
png_name_in_filepath='[a-z|_|A-Z]{1}[a-z|_|A-Z|0-9|-]*(?=[.9]*.png)';
# 布局文件
java_layout='';
include_layout='';

def scan_res_files(directory,prefix=None,postfix=None):
  files_list=[]
    
  for root, sub_dirs, files in os.walk(directory):
    for special_file in files:
      if postfix:
        if special_file.endswith(postfix):
          files_list.append(os.path.join(root,special_file))
      elif prefix:
        if special_file.startswith(prefix):
          files_list.append(os.path.join(root,special_file))
      else:
        files_list.append(os.path.join(root,special_file))
               
  return files_list

def scan_files(directory,prefix=None,postfix=None):
  files_list=[]
    
  for root, sub_dirs, files in os.walk(directory):
    for special_file in files:
      if postfix:
        if special_file.endswith(postfix):
            special_file = os.path.join(root,special_file)
            func_findstr(special_file)
      elif prefix:
        if special_file.startswith(prefix):
            special_file = os.path.join(root,special_file)
            func_findstr(special_file)
      else:
        special_file = os.path.join(root,special_file)
        func_findstr(special_file)
               
  return files_list

def func_findstr(filepath):
    thefile=open(filepath, 'rb')
    while True:
        buffer = thefile.read(104857600)
        if not buffer:
            break
        for match in re.findall(findstr,buffer): 
            # print "Found in "+filepath+" %s" % match
            findDrawable.append(match)
    thefile.close()

def filterstr(str):
    str = str.replace('$','\$')
    return str.replace('{','\{').replace('}','\}')

def getSizeInNiceString(sizeInBytes):
    """
    Convert the given byteCount into a string like: 9.9bytes/KB/MB/GB
    """
    for (cutoff, label) in [(1024*1024*1024, "GB"),
                            (1024*1024, "MB"),
                            (1024, "KB"),
                            ]:
        if sizeInBytes >= cutoff:
            return "%.1f %s" % (sizeInBytes * 1.0 / cutoff, label)

    if sizeInBytes == 1:
        return "1 byte"
    else:
        bytes = "%.1f" % (sizeInBytes or 0,)
        return (bytes[:-2] if bytes.endswith('.0') else bytes) + ' bytes'

def delteFile(filename):
    file = filename
    if os.path.exists(file):
        os.remove(file)
    else:
        print 'no such file:%s' % file

def deltefile(list):
    while True:
        a = raw_input('逐个核对删除(Y/N): ')
        if a == 'y' or a=='Y':
             for i in range(0,len(list)):
                while True:
                    b = raw_input(list[i]+' 是否删除（Y/N）：')
                    if b == 'y' or b=='Y':
                        delteFile(list[i])
                        print list[i]+'已删除'
                    break
        else:
            for i in range(0,len(list)):
                delteFile(list[i])
        break

if __name__ == '__main__':
    if len(sys.argv)>=3 and (sys.argv[1]=='-f' or sys.argv[1]=='-d'):
        if sys.argv[1]=='-f' and os.path.isfile(sys.argv[2]):
            findstr = filterstr(sys.argv[3])
            func_findstr(sys.argv[2])
        elif sys.argv[1]=='-d' and os.path.exists(sys.argv[2]):
            # findstr = filterstr(sys.argv[3])
            # scan_files(sys.argv[2],postfix=sys.argv[5])
            deletefiles = []
            findstr = filterstr(layout_drawableMatch)
            scan_files(sys.argv[2],postfix='xml')
            findstr = filterstr(java_drawableMatch)
            scan_files(sys.argv[2],postfix='java')
            listFile = scan_res_files(sys.argv[2],postfix='png')
            sumFile=0
            size = 0
            for i in range(0,len(listFile)):
                findFlag = False
                for pngName in re.findall(png_name_in_filepath,listFile[i]):
                    for j in range(0,len(findDrawable)):
                        if findDrawable[j]==pngName :
                            findFlag = True
                            break
                if findFlag == False:
                    sumFile=sumFile+1
                    size = size+os.path.getsize(listFile[i])
                    deletefiles.append(listFile[i])
                    print listFile[i]
            print '目录中总共引用了：%d 次数资源对象' % len(findDrawable)
            print '目录中总共有：%d 个png文件' % len(listFile)
            print '目录中总共有：%d 个未用到的png文件 共%s 可以删除' %(sumFile,getSizeInNiceString(size))
            while True:
                a = raw_input('是否删除(Y/N): ')
                if a == 'y' or a=='Y':
                    deltefile(deletefiles)
                else:
                    print 'n'
                break
                
                    
           
        else:
            print '-- 参数错误'
    elif len(sys.argv)==2:
        findstr = filterstr(sys.argv[1])
        print func_walks(os.getcwd())
    else:
        print '-- 参数说明 ：'
        print '    1. '+sys.argv[0]+ ' -d' +' directory "string" \t在指定目录(包括子目录)下的所有文件查找字符串'
        # print '    2. '+sys.argv[0]+ ' -l' +' 列出查找到的文件名'



