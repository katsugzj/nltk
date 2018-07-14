# nltk_homework
---
# 第一次实验(预处理)
### 1.由DTD文件可知一个DOC标签下存在多个TEXT标签的情况
### 2.通过正则表达式读取标签的内容
### 3.首先词条化，并去除停用词和非字母和非数字，并对结果词性归并，对每个DOCNO输出一个文件保存结果
### 4.只保存了TEXT的内容，文件名为DOCNO
### 5.总运行时间为4.5小时
### 6.处理完成的文件共有741724个
---
# 第二次实验(倒排索引)
### 1.使用FreqDist方法直接统计词频，将结果以{词条：{DOCNO：词频}}的方式存储
### 2.总运行时间为40分钟
### 3.未使用归并，python的内存占用最高到达3.5G
### 4.处理后的文件有1.74G，文本编辑器中记事本，sublime和VScode都打不开，notepad++勉强可以(会有几秒卡顿)
---
# 第三次实验(检索模型)
### 1.构建索引时未统计总词数，所以使用文档大小来近似
### 2.没有构建布尔索引，仅使用了tfidf和bm25对文档打分
### 3.可以对topics的每个单词使用tfidf进行打分，然后对每个部分的title和两个描述总的单个单词的打分最高的几个单词作为检索关键字，但是处理量较大，只简单的使用title进行检索
### 4.第一实验处理后的文档较多，导致匹配文档来获取长度的时间过长，因此使用bm25处理时间比起简单使用tfidf的时长要多出许多
### 5.从实验结果来看，单纯使用tfidf得到的结果非常差，不论是准确率还是召回率都远远低于bm25所得到的结果
---
# 第四次实验(相关反馈和查询拓展)
### 1.对比使用bm25，使用tfidf计算权重的向量空间模型，tfidf，rocchio处理向量并使用bm25查询，只看df<10000的bm25处理的rocchio，rocchio处理向量并使用tfidf查询，使用bm25的wordnet
#### 其中只使用bm25的效果最好，使用rocchio处理后的用bm25查询反而效果变差了，只看df<10000次之，使用同义词的效果变化不大
#### part1部分结果如下：
#### tfidf：
        iprec_at_recall_0.00  	all	0.0580
        P_5                   	all	0.0200
#### bm25：
        iprec_at_recall_0.00  	all	0.8445
        P_5                   	all	0.6800
#### tfidf计算权重的vsm：
        iprec_at_recall_0.00  	all	0.0746
        P_5                   	all	0.0000
#### bm25计算权重的vsm:
        iprec_at_recall_0.00  	all	0.1993
        P_5                   	all	0.0200
#### bm25+rocchio(df<10000>):
        iprec_at_recall_0.00  	all	0.6193
        P_5                   	all	0.3500
#### bm25+rocchio:
        iprec_at_recall_0.00  	all	0.7149
        P_5                   	all	0.6000
#### tfidf+rocchio:
        iprec_at_recall_0.00  	all	0.0938
        P_5                   	all	0.0400
#### wordnet+bm25:
        iprec_at_recall_0.00  	all	0.7006
        P_5                   	all	0.5200
#### 从结果来看使用特殊方法对tfidf还是有一定提升的，但是对于bm25反而有反作用
### 2.本来使用过bm25计算权重的向量空间模型发现效果变差了很多
### 3.使用同义词时，不同单词的同义词个数不同，会导致单词权重变化。解决方式，查询同义词，但是得分加到查询的单词集合里的原单词上，设置权重时可以统一加到原单词。另一个方法是单独记录每一个同义词，但是该单词的得分要除以同义词个数。但是前提是所有的单词都被使用过，所以在这个数据集里是可以使用的，因为数据集比较大，基本涵盖了大多数的单词。最终实现的是第二个方法
### 4.rocchio速度太慢所以最终wordnet并没有建立在rocchio上
### 5.没有使用伪相关反馈
### 6.本来觉得出现在10000篇以上的文章的单词不会对结果有太大影响，结果差距还是有的
---
# 第五次实验（语言模型）
### 1.遍历index里的单词（即每一行），若是query中的关键字则遍历出现的文章里的词频，求和作为cft
### 2.对文章进行评分，每当index中匹配到关键字，就是使用平滑，参数a选择了0.95，但是因为没有记录文档集总长度取而代之的是文档大小，但是与词频单位不同，所以可以添加系数来近似
### 3.但是因为参数a较小所以单个文章的分数并没有太大影响（如果一个关键字在某一文档的tf/L远小于cf/T则会有很大影响，且是分数下降），但是事实上出现了这样的情况，直观上看分数给低一点是很合理的
### 4.事实上，直观上来看cf/T很大时，说明单词权重应该较小，但是取负相关是更不合理的，因为取负相关会导致完全无关的文档分数上升
### 5.文档匹配到的关键字的评分相乘
### 6.得到的结果非常差，不管是准确率还是召回率
        iprec_at_recall_0.00  	all	0.0049
        P_5                   	all	0.0000
---
# 第六次实验（LTR）
### 1.使用了三种特征，tfidf，bm25以及文档长度，代码在train2getfeature的T2F类中实现
### 2.使用的是用线性回归进行预测，使用的是predict_proba返回的每类的概率，取返回概率的第一部分，即不相关的概率，排名时按照分数低者排名高的原则
### 3.使用的是github上的项目的[测试文件](https://github.com/CLEF-TAR/tar)，不知道和助教给的是不是一样的，数据集是一样的，最终的结果如下
        ALL     topic_id        ALL
        ALL     num_docs        117562
        ALL     num_rels        1857
        ALL     num_shown       103273
        ALL     num_feedback    0
        ALL     rels_found      1651
        ALL     last_rel        2796.633
        ALL     wss_100 0.028
        ALL     wss_95  0.041
        ALL     NCG@10  0.363
        ALL     NCG@20  0.521
        ALL     NCG@30  0.613
        ALL     NCG@40  0.695
        ALL     NCG@50  0.742
        ALL     NCG@60  0.788
        ALL     NCG@70  0.826
        ALL     NCG@80  0.862
        ALL     NCG@90  0.88
        ALL     NCG@100 0.88
        ALL     total_cost      3442.433
        ALL     total_cost_uniform      3604.361
        ALL     total_cost_weighted     4233.438
        ALL     norm_area       0.666
        ALL     ap      0.126
        ALL     r       0.841
        ALL     loss_e  0.4
        ALL     loss_r  0.041
        ALL     loss_er 0.441
### 4.实现的评价指标是DCG，DCG目的是在保证准确率的同时，相关文件排名要高，公式如下
        ∑(((2^n)-1)/log(1+rank))
### n是相关性，可划分多个层次，本作业中只有两种，指定了不相关时n为0，相关为2，rank是该记录在搜索结果中的排名，所以排名越高，出错的惩罚越大。而NDCG一般还要除一个IDCG
### 5.线性回归使用的sklearn的线性回归模型
### 6.训练集提取的模型在trainfeature，测试集提取的模型在testfeature中