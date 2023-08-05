import librosa
import numpy as np
import os
from os import path
import pandas as pd
import pickle

class Covid:
    def __init__(self):
        file = 'filename.pkl'
        self.model = pickle.load(open(file,'rb'))
    def detect_covid(self,sample):
        
        test = self.extract_info(sample).reshape(1,-1)
        result = round(np.max(self.model.predict_proba(test)[0]),2)
        label = self.model.predict(test)[0]
        
        return result , label
    def extract_info(self,file_name):
    
        data, sampling_rate = librosa.load(file_name)
        mfccs = librosa.feature.mfcc(data,sampling_rate)
        mfccs = np.mean(mfccs.T,axis=0)
        label = file_name[1]
        return mfccs
