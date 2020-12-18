import json
import glob
import hashlib
import logging
import pandas as pd
import networkx as nx
from tqdm import tqdm
from joblib import Parallel, delayed
from param_parser import parameter_parser
import numpy.distutils.system_info as sysinfo
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import json
from sklearn.manifold import TSNE
import  numpy as np
from sklearn.cluster import DBSCAN
import itertools

# logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)
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
def modiData(data):
    x1 = []
    x2=[]
    for i in range(0,len(data+1)):
        x1.append(data[i][0])
        x2.append(data[i][1])
    x1=np.array(x1)
    x2=np.array(x2)
    #重塑数据
    X=np.array(list(zip(x1,x2))).reshape(len(x1),2)
    return X
class WeisfeilerLehmanMachine:
    """
    Weisfeiler Lehman feature extractor class.
    """
    def __init__(self, graph, features, iterations):
        """
        Initialization method which also executes feature extraction.
        :param graph: The Nx graph object.
        :param features: Feature hash table.
        :param iterations: Number of WL iterations.
        """
        self.iterations = iterations
        self.graph = graph
        self.features = features
        self.nodes = self.graph.nodes()
        self.extracted_features = [str(v) for k,v in features.items()]
        self.do_recursions()

    def do_a_recursion(self):
        """
        The method does a single WL recursion.
        :return new_features: The hash table with extracted WL features.
        """
        new_features = {}
        for node in self.nodes:
            nebs = self.graph.neighbors(node)
            degs = [self.features[neb] for neb in nebs]
            features = "_".join([str(self.features[node])]+sorted([str(deg) for deg in degs]))
            hash_object = hashlib.md5(features.encode())
            hashing = hash_object.hexdigest()
            new_features[node] = hashing
        self.extracted_features = self.extracted_features + list(new_features.values())
        return new_features

    def do_recursions(self):
        """
        The method does a series of WL recursions.
        """
        for iteration in range(self.iterations):
            self.features = self.do_a_recursion()

def dataset_reader(path):
    """
    Function to read the graph and features from a json file.
    :param path: The path to the graph json.
    :return graph: The graph object.
    :return features: Features hash table.
    :return name: Name of the graph.
    """
    name = path.strip(".json").split("\\")[-1]
    data = json.load(open(path))
    graph = nx.from_edgelist(data['edges'])
    if "features" in data.keys():
        features = data['features']
    else:
        features = nx.degree(graph)
    features = {int(k):v for k,v, in features.items()}
    return graph, features, name

def feature_extractor(path, rounds):
    """
    Function to extract WL features from a graph.
    :param path: The path to the graph json.
    :param rounds: Number of WL iterations.
    :return doc: Document collection object.
    """
    graph, features, name = dataset_reader(path)
    machine = WeisfeilerLehmanMachine(graph,features,rounds)
    doc = TaggedDocument(words = machine.extracted_features , tags = ["g_" + name])
    return doc

def save_embedding(output_path, model, files, dimensions):
    """
    Function to save the embedding.
    :param output_path: Path to the embedding csv.
    :param model: The embedding model object.
    :param files: The list of files.
    :param dimensions: The embedding dimension parameter.
    """
    out = []
    for f in files:
        identifier = f.split("\\")[-1].strip(".json")
        print(identifier)
        # out[identifier]=list(model.docvecs["g_"+identifier])
        out.append([int(identifier)] + list(model.docvecs["g_"+identifier]))

    out = pd.DataFrame(out,columns = ["type"] +["x_" +str(dimension) for dimension in range(dimensions)])
    out = out.sort_values(["type"])
    out.to_csv(output_path, index = None)

def main(args):
    """
    Main function to read the graph list, extract features, learn the embedding and save it.
    :param args: Object with the arguments.
    """
    AllGraph=[]
    with open('AllInfo.json','r') as f:
        AllGraph = json.load(f)
    graphs = glob.glob(args.input_path + "*.json")
    document_collections = Parallel(n_jobs=args.workers)(
        delayed(feature_extractor)(g, args.wl_iterations) for g in tqdm(graphs))
    model = Doc2Vec(document_collections,
                    vector_size=args.dimensions,
                    window=0,
                    min_count=args.min_count,
                    dm=0,
                    sample=args.down_sampling,
                    workers=args.workers,
                    epochs=args.epochs,
                    alpha=args.learning_rate)
    print("graph2vec Training finished")
    graphVec = model.docvecs.vectors_docs.tolist()
    #tsne降维
    X_tsne = TSNE(n_components=2,learning_rate=200).fit_transform(graphVec)
    print("Tsne Training finished")
    X_DBscan = modiData(X_tsne)
    #Dbscan聚类
    DBscanData = DBSCAN(eps=5, min_samples=5, metric='euclidean').fit(X_DBscan)
    print("DBscan Training finished")

    label = DBscanData.labels_.tolist()
    final = []
    for i in range(0, len(AllGraph)):
        temp = {'id': i, 'x': X_DBscan[i][0], 'y': X_DBscan[i][1], 'cluster': label[i],
                'name':AllGraph[i]['name'],'paper':AllGraph[i]['paper'],'count':AllGraph[i]['count'],
                'cite':AllGraph[i]['cite'],'position':AllGraph[i]['position'],'edges':AllGraph[i]['edges'],
                'nodes':AllGraph[i]['nodes'],'edgess':AllGraph[i]['edgess']}
        final.append(temp)
    with open('../public/struc.json', "w") as f:
        json.dump(final, f, cls=MyEncoder)
    print("All finished")
if __name__ == "__main__":
    args = parameter_parser()
    main(args)