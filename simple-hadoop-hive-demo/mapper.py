#!/usr/bin/python
import sys  
  
# 调用标准输入流  
for line in sys.stdin:  
    # 读取文本内容   
    line = line.strip()  
    # 对文本内容分词，形成一个列表 
    words = line.split()  
    # 读取列表中每一个元素的值  
    for word in words:  
        # map函数输出，key为word，下一步将进行shuffle过程，将按照key排序，输出，这两步为map阶段工作为，在本地节点进行  
        print('%s\t%s' % (word, 1))
