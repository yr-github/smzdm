import itchat
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from collections import Counter
import jieba.analyse


#制作饼图
def sexAnalyse(itemname_, itemnamelist_, itemnumlist_):
    totle = itemnumlist_[0] + itemnumlist_[1] + itemnumlist_[2]
    subtitle = "共有:%d个好友" % totle
    pie = Pie()#新建饼图对象
    pie.add("",[list(z) for z in zip(itemnamelist_,itemnumlist_)],center=["35%", "50%"])#饼图对象数据添加
    pie.set_global_opts(title_opts=opts.TitleOpts(title=subtitle),legend_opts=opts.LegendOpts(pos_left="15%"),)
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    outFileName = itemname_+ '.html'
    pie.render(outFileName)#保存饼图对象
#制作词云
def wordCloud(itemname_, itemnamelist_, itemnumlist_):
    wordcloud = WordCloud()#新建词云对象
    wordcloud.add("", [list(z) for z in zip(itemnamelist_,itemnumlist_)],word_size_range=[20, 100],shape='cardioid')#词云对象数据添加
    outFileName = itemname_ + '.html'
    wordcloud.render(outFileName)#保存词云对象
#提取签名关键词
def getTag(text_, cnt_):
    #text = re.sub(r"<span.*><span>", "", text_)
    text =  text_.replace("span","").replace("class","").replace("emoji","")
    tagList = jieba.analyse.extract_tags(text)
    for tag in tagList:
        cnt_[tag] += 1

def dict2list(dict_):
    namelist = []
    numlist = []
    for key, value in dict_.items():
        namelist.append(key)
        numlist.append(value)

    return namelist, numlist

def counter2list(counter_):
    namelist = []
    numlist = []

    for item in counter_:
        namelist.append(item[0])
        numlist.append(item[1])

    return namelist, numlist

if __name__ == '__main__':
    sexDict = {}
    sexDict['0'] = "其他"
    sexDict['1'] = "男"
    sexDict['2'] = "女"
    sexCounter = Counter()
    signatureCounter = Counter()
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)[0:]  # 获取好友信息
    friendslist = []
    for friend in friends:
        getTag(friend['Signature'], signatureCounter)
        sexCounter[sexDict[str(friend['Sex'])]] += 1

    #性别比例分析
    nameList, numList = dict2list(sexCounter)
    sexAnalyse("性别比例",nameList, numList)
    # 个性签名签名关键词
    nameList, numList = counter2list(signatureCounter.most_common(200))
    wordCloud('个性签名', nameList, numList)

