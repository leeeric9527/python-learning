 #-*- encoding:UTF-8 -*-

# from sklearn.feature_extraction.text import CountVectorizer as CV
# from sklearn.feature_extraction import text as txt
# vectorizer = CV()#生成向量化容器
# corpus = [#设定料库
#     'This is the first document.',#导入语料库
#     'This is the second second document.',
#     'And the third one.',
#     'Is this the first document?',
# ]
# X = vectorizer.fit_transform(corpus)
# X.toarray()#出现次数表示为矩阵形式          
# vectorizer.get_feature_names()#获取每一列对应的单词
# transformer = txt.TfidfTransformer()#TF_IDF的转换容器
# tfidf = transformer.fit_transform(X)#根据词频矩阵生成权重矩阵
# tfidf.toarray()#权重矩阵输出                        
import os
import jieba
import jieba.posseg as pseg
import sys
import string
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def getFilelist(argv) :
#输入参数：路径
#输出：文件路径和文件列表
    path = argv[1]
    filelist = []
    files = os.listdir(path)
    for f in files :
        if(f[0] == '.') :
            pass
        else :
            filelist.append(f)
    return filelist,path

#对文档进行分词处理
def fenci(argv,path) :
#输入参数：argv为文件列表，path为文件路径
#输出结果：所有文件的分词结果，其分词结果存入路径path+./segfile中
    
    sFilePath = './segfile'
    if not os.path.exists(sFilePath) : #生成保存分词结果的目录
        os.mkdir(sFilePath)
    #读取文档
    filename = argv
    f = open(path+filename,'r+')
    file_list = f.read()
    f.close()
    #对文档进行分词处理，采用默认模式
    seg_list = jieba.cut(file_list,cut_all=True)
    #对空格，换行符进行处理
    result = []
    for seg in seg_list :
　　　　 seg = ''.join(seg.split())
        if (seg != '' and seg != "\n" and seg != "\n\n") :
            result.append(seg)
    #将分词后的结果用空格隔开，保存至本地。比如"我来到北京清华大学"，分词结果写入为："我 来到 北京 清华大学"
    f = open(sFilePath+"/"+filename+"-seg.txt","w+")
    f.write(' '.join(result))
    f.close()


#读取100份已分词好的文档，进行TF-IDF计算
def Tfidf(filelist) :
　　path = './segfile/'
    corpus = []  #存取100份文档的分词结果
    for ff in filelist :
        fname = path + ff
        f = open(fname,'r+')
        content = f.read()
        f.close()
        corpus.append(content)    
    vectorizer = CountVectorizer()    
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    
    word = vectorizer.get_feature_names() #所有文本的关键字
    weight = tfidf.toarray()              #对应的tfidf矩阵
    
    sFilePath = './tfidffile'
    if not os.path.exists(sFilePath) : 
        os.mkdir(sFilePath)

    # 这里将每份文档词语的TF-IDF写入tfidffile文件夹中保存
    for i in range(len(weight)) :
　　　　 print u"--------Writing all the tf-idf in the",i,u" file into ",sFilePath+'/'+string.zfill(i,5)+'.txt',"--------"
        f = open(sFilePath+'/'+string.zfill(i,5)+'.txt','w+')
        for j in range(len(word)) :
            f.write(word[j]+"    "+str(weight[i][j])+"\n")
        f.close()
            
if __name__ == "__main__" : 
    (allfile,path) = getFilelist(sys.argv)
　　for ff in allfile :
        print "Using jieba on "+ff
        fenci(ff,path)

    Tfidf(allfile)