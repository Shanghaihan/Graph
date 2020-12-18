import json
import  numpy as np
from graph2vec import main
from param_parser import parameter_parser
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
def processData(data,year):
    final = []
    datas=dict()                    #datas字典是为了能够根据人名直接找数据
    for i in data:
        datas[i['name']] = i
    def findCircle(author):
        position = 0  # 记录作者在每篇论文所处的位置
        author_circle = []
        author_name = []
        # 遍历论文，将相关作者都加到circle里面，用以形成图的数据
        i = author
        for j in i['paper']:
            for author in j['author']:
                if author != i['name']:
                    author_name.append(author)
                    temp = [i['name'], author]
                    author_circle.append(temp)
                else:
                    position+=(j['author'].index(author) + 1)
        position = position/len(i['paper'])
        author_name = list(set(author_name))
        return author_circle,position,author_name
    for i in data:
        author_circle,position,author_name= findCircle(i)          #作者本人向外扩一圈
        connect = len(author_circle)/len(np.array(list(set([tuple(t) for t in author_circle]))))
        #向外扩一圈
        for j in i['paper']:
            for author in j['author']:
                if author != i['name']:
                    #寻找相关作者的圈子，这里伏笔的不考虑重复论文
                    other_circle,other_position,other_author = findCircle(datas[author])
                    author_circle +=other_circle
                    author_name += other_author
        author_name = list(set(author_name))        #人名去重
        totalCount = 0
        totalCite = 0
        totalPosition = 0
        totalPaper = []
        for j in author_name:
            for x  in datas[j]['paper']:
                if  x not  in totalPaper:
                    totalPaper.append(x)
        for j in totalPaper:
            totalCite +=  j['cite']
            totalPosition += len(j['author'])
        totalCount = len(totalPaper)/len(author_name)
        totalCite = totalCite / len(totalPaper)
        totalPosition = totalPosition /len(totalPaper)
        temp = { 'name':i['name'],'graph':author_circle,'position': position,'count':i['count'],'cite':i['cite'],'connect':connect,'year':year,'paper':i['paper'],
                 'totalCount':totalCount,'totalCite':totalCite,'totalPosition':totalPosition
                 }
        final.append(temp)
    return final
def mergeData(totalData,begin,end):
    merge=[]
    while begin<=end:
        merge += processData(totalData[str(begin)],begin)                             #直接添加
        begin+=1
    return merge
def addId(data):
    for i in range(0,len(data)):
        son_sum = 0
        son_author_id = dict()
        son_author_id_reverse = dict()     #由于在可视化时，需要通过下标来访问作者名，所以需要反向编号
        for j in data[i]['graph']:         #给作者圈子内部编号
            if j[0] not in son_author_id.keys():
                son_author_id[j[0]] = son_sum
                son_author_id_reverse[son_sum] = j[0]
                son_sum+=1
            if j[1] not in son_author_id.keys():
                son_author_id[j[1]] =son_sum
                son_author_id_reverse[son_sum] = j[1]
                son_sum+=1
        for j in data[i]['graph']:
            j[0] = son_author_id[j[0]]
            j[1] = son_author_id[j[1]]
        data[i]['authorId'] = son_author_id_reverse
    return data
def preMain(stratYear,endYear):
    data = []
    with open('data_weight.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    merge = mergeData(data, stratYear, endYear)                 #直接对每一年的进行数据操作，然后相加
    final= addId(merge)                                         #给作者内部编号
    # 需要分别导出所有作者的图结构，以便于生成graph2vec的数据格式
    Alltemp=[]
    for i in range(0,len(final)):
        tt = dict()
        #一下两个用于生成结构图的数据格式
        nodes = []
        edgess = []
        temp_edges = []          #用于去重的保存数组
        for j in final[i]['graph']:
            if str(j[0]) not in tt.keys():
                tt[str(j[0])] = str(j[0])
                nodes.append({'id':str(j[0])})
            if str(j[1]) not in tt.keys():
                tt[str(j[1])] = str(j[1])
                nodes.append({'id':str(j[1])})
            flag = 1
            for t  in temp_edges:
                if (t[0]==j[0] and t[1]==j[1]) or (t[0]==j[1] and t[1]==j[0]):
                    flag = 0
            if flag ==1:
                temp_edges.append(j)
                edgess.append(  {'source':str(j[0]),'target':str(j[1])})
        totalConnect = len(final[i]['graph'])/(len(temp_edges))           #团队的合作紧密度
        temp = {"edges": temp_edges,"features": tt,'count':final[i]['count'],'cite':final[i]['cite'],'position':final[i]['position'],'connect':final[i]['connect'],
                'totalConnect':totalConnect,'totalCount':final[i]['totalCount'],'totalCite':final[i]['totalCite'],'totalPosition':final[i]['totalPosition'],
                'paper':final[i]['paper'],
                'name':final[i]['name'],'nodes':nodes,'edgess':edgess,'year':final[i]['year'],
                'authorId':final[i]['authorId']}
        Alltemp.append(temp)
        with open('./structure/' + str(i) + '.json', "w") as f:
            json.dump(temp, f, cls=MyEncoder)
    with open('AllInfo.json', "w") as f:
        json.dump(Alltemp, f, cls=MyEncoder)
    print("preData finished")
if __name__ == "__main__":
    preMain(2019,2019)      #对于原数据，一般只需要修改年限
    args = parameter_parser()
    main(args)



