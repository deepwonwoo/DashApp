
import pandas as pd
import numpy as np
import argparse
import pickle
import shutil
import json
import time
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--username")
parser.add_argument("--id")
args = parser.parse_args()

sys.path.append(os.getcwd())
id = args.id
username = args.username

with open(f"./workspace/{username}/{id}/meas.pickle", "rb") as f:
    meas = pickle.load(f)
    from utils.env import Spice_Env
    env = Spice_Env(id, username, meas)

para_log = "error,episode,step"
for i in range(len(env.df_para)):
    para_log += f",{env.df_para['Parameters'][i]}"


f = open(f"./workspace/{username}/{id}/trained_para.log", "w")
f.write(para_log)
f.close()

os.mkdir(f"./workspace/{username}/{id}/top1")
os.mkdir(f"./workspace/{username}/{id}/top2")
os.mkdir(f"./workspace/{username}/{id}/top3")
