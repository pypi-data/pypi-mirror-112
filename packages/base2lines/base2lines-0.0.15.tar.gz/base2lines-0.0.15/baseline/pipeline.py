from sklearn.pipeline import *
from sklearn.naive_bayes import *
from sklearn.preprocessing import *
from sklearn.svm import *
from sklearn.decomposition import *
from sklearn.model_selection import *
from sklearn.linear_model import *
from sklearn.compose import *
from sklearn.feature_extraction.text import *
from sklearn.impute import *
from sklearn.ensemble import *
from sklearn.metrics import *
from sklearn.neural_network import *
from xgboost import *
import numpy as np
import pandas as pd
import graphviz


class Pipeline:
    dataset = None
    def __init__(self,dataset):
        self.dataset = pd.DataFrame(dataset)
    def show_graph(self,pipeline_show):
        listOfItems =[]
        def pipetolist(pipel,listOfParameters = None):
            if 'steps' in pipel:
                pipel=pipel['steps']
            for element in pipel:
                se = [x for x in element]
                if str(type(se[1])) == "<class 'sklearn.compose._column_transformer.ColumnTransformer'>":
                    transformers = se[1].get_params()['transformers']
                    for transformer in transformers:
                        bs = [x for x in transformer]
                        if str(type(bs[1])) == "<class 'sklearn.pipeline.Pipeline'>":
                            pipetolist(bs[1].get_params()['steps'],bs[2])
                        else:
                            listOfItems.append(bs)
                elif str(type(se[1])) == "<class 'sklearn.pipeline.Pipeline'>":
                    pipetolist(se[1].get_params()['steps'])
                else:
                    if listOfParameters != None:
                        se.append(listOfParameters)
                    listOfItems.append(se)
        pipetolist(pipeline_show)
        
        dot = graphviz.Digraph(comment='Graph',strict=True)  
        dot.node('start','pandas dataframe')
        for listOfParameters in listOfItems:
            dot.node(str(listOfParameters[1]),str(listOfParameters[1]))
        columns = []
        dicOfEdges = {}
        for column in self.dataset.columns:
            columns.append(str(column))
        for element in columns:
            a = ['start']
            for l in listOfItems:
                if len(l) == 3:
                    if element in l[2]:
                        a.append(str(l[1]))
                else:
                    a.append(str(l[1]))
            print(a)
            for i in range(0,len(a)-1):
                
                st = a[i]+"-"+a[i+1]
                if st in dicOfEdges:
                    dicOfEdges[st].append(element)
                else:
                    #dot.edge(a[i],a[i+1])
                    dicOfEdges[st] = [element]
        for st in dicOfEdges:
            #print(st)
            st1,st2 = st.split('-')
            print(st,st1,st2)
            dot.edge(st1,st2,label= str(dicOfEdges[st]))
        dot.format='jpeg'
        dot.render('FileName', view=True)

        