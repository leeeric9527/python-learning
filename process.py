#-*- coding:UTF-8 -*-
import numpy as np

data=np.loadtxt('find_parent.txt')#打开数据文件文件
slice=np.zeros((len(data),4),dtype='float')  
data=np.hstack((data, slice))#生成n*5规模矩阵存储相关数据
#数据结构
node_id=0; parent_id=1; parent_index=2; deepth=3; child_num=4; max_cdeepth=5
for i in range(0,len(data)):
	if data[i,parent_id]==-1:#初始化根节点
		data[i,parent_index]=-1#设定父节点索引为-1
		data[i,deepth]=1#设定深度为1
		data[i,child_num]=0#设定子节点个数为0
		data[i,max_cdeepth]=1#设定子节点最大深度为1
	else:#非根节点查找父节点
		for j in range(0,len(data)):
			if data[i,parent_id]==data[j,node_id]:
				#当前节点工作
				data[i,parent_index]=j#更新父节点下标索引
				data[i,deepth]=data[j,deepth]+1#更新节点深度
				data[i,child_num]=0
				data[i,max_cdeepth]=data[i,deepth]#设定最大层数为自己
				#父节点工作：增加子节点数目，记录子节点最大深度
				data[j,child_num]=data[j,child_num]+1
				ancestor_index=data[j,parent_index]
				if data[j,max_cdeepth]<data[i,deepth]:
					data[j,max_cdeepth]=data[i,deepth]
				while ancestor_index>=0:#给所有祖先节点增加子节点个数
					data[int(ancestor_index),child_num]=data[int(ancestor_index),child_num]+1
					#更新子节点最大层数
					if data[int(ancestor_index),max_cdeepth]<data[i,deepth]:
						data[int(ancestor_index),max_cdeepth]=data[i,deepth]
					ancestor_index=data[int(ancestor_index),parent_index]
				break
data[:,deepth]=data[:,max_cdeepth]-data[:,deepth]
out2txt=data[:,(node_id,deepth,child_num)]
np.savetxt('node_deepth_num.txt',out2txt,fmt='%7d',delimiter='\t')



