import json
import pymongo
from bson.objectid import ObjectId
from uuid import uuid4
from os import makedirs
from os.path import join

mongodbPath = 'mongodb://127.0.0.1/dirDB'
siteDataPath = '/Volumes/DATA/SiteData/'

'''
novel = {
    'title':'string',
    'parentdirId':'ObjectId',
    'filename':'string'
}

chapter = {
    'title':'string',
    'parentnovelId':'ObjectId',
    'filename':'string',
    'ordinal':'string'
}
'''

def getdirDB():
    client = pymongo.MongoClient(mongodbPath)
    return client['dirDB']

def getRoot():
    client = pymongo.MongoClient(mongodbPath)
    db = client['dirDB']
    dirCollection = db['dirmodels']
    root = dirCollection.find_one({'parentdirId':None})
    return root

class thisdirNovel():
    def __init__(self,dirID,novelFilePath=None):
        self.client = pymongo.MongoClient(mongodbPath)
        db = self.client['dirDB']
        self.dirCollection = db['dirmodels']
        self.novelCollection = db['novelmodels']
        self.chapterCollection = db['chaptermodels']
        
        if(novelFilePath is not None):
            self.novelFilePath = novelFilePath
        else:
            self.novelFilePath = str(uuid4())
        self.parentDir = self.dirCollection.find_one({'_id':ObjectId(dirID)})
        self.novelid = None
        self.chapterNum = 0

        self.infojson = {}
        self.infojson['chapter'] = []
        
    def insertANovel(self,novelName):
        novelid = self.novelCollection.insert_one({'title':novelName,'parentdirId':self.parentDir['_id'],'filename':self.novelFilePath})
        self.novelid = novelid.inserted_id
        self.infojson['novel'] = {'novelTitle':novelName, 'dirName':self.novelFilePath}
        makedirs(join(siteDataPath,self.novelFilePath))

    def insertAChapter(self,chapterName,content,filepath=None):
        self.chapterNum += 1
        if(filepath is None):
            filepath = str(uuid4())
        if(self.novelid is None):
            raise 'novel id is not given'
        
        self.chapterCollection.insert_one({'title':chapterName,'parentnovelId':ObjectId(self.novelid),'filename':filepath,'ordinal':self.chapterNum})
        
        self.infojson['chapter'].append({'chapterTitle':chapterName, 'fileName':filepath, 'oridnal':self.chapterNum})
        with open(join(siteDataPath,self.novelFilePath,filepath),'w') as f:
            f.write(content)
        
    def close(self):
        self.client.close()
        self.infojson['totalchapter'] = self.chapterNum
        with open(join(siteDataPath,self.novelFilePath,'info.json'),'w', encoding='utf-8') as f:
            json.dump(self.infojson, f, ensure_ascii=False)
