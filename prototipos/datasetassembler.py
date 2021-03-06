# -*- coding: utf-8 -*-
"""DatasetAssembler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jvkr7BZCCZ2J743vvmHVfaP8JJ-0g2fE
"""

import featureextractor
from os import listdir
from os.path import isdir
from pandas import read_json, DataFrame, concat

def audiosToDatapoints(path_datapoints, audios_dict):
  """
  Converte os áudios no dicionário audios_dict em datapoints salvos 
  no formato .json na pasta path_datapoints
  """

  assert(isdir(path_datapoints))

  assert(audios_dict)
  assert(isinstance(audios_dict, dict))

  for name, value in audios_dict.items():
    audio_name = name.split('.')[0]
    jsonName = audio_name+".json"
    data = value["data"]
    if len(data)%2==1 : data = data[:-1] 
    computeAndSaveAudioFeatures(audio_data=data,\
                                name=audio_name,\
                                file_path=path_datapoints+jsonName)
    
    #Transpõe o datapoint
    read_json(open(path_datapoints+jsonName)).T.to_json(path_datapoints+jsonName)

def concatDatapoints(path_datapoints, path_dataframe_json):
  """
  Concatena todos datapoints na pasta path_datapoints em um DataFrame e 
  salva no arquivo path_dataframe_json
  """

  total = DataFrame()

  for arq in listdir(path_datapoints):
    df = read_json(open(path_datapoints+arq))
    total = concat([total, df])

  total.to_json(path_dataframe_json)

def jsonToSklearn(data_frame_json_path):
  """
  Carrega o .json em data_frame_json_path e transforma-o em um dicionário no formato
  dos datasets de scikit-learn
  """

  data_frame = read_json(data_frame_json_path)
  data_frame.to_numpy()[0]
  data = np.array([ arr[:-1] for arr in data_frame.to_numpy() ])
  target = np.array([ arr[-1] for arr in data_frame.to_numpy() ])
  target_names = np.array(["polerar", "tapa"])
  feature_names = data_frame.keys().to_numpy()[:-1].tolist()
  return {
    "data":data,
    "feature_names":feature_names,
    "target":target,
    "target_names":target_names
  }