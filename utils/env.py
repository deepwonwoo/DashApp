import os
import sys
import time
import numpy as np
import pandas as pd
from threading import Thread
from scipy.interpolate import griddata


class Spice_Env:
    def __init__(self, id, username, meas):
        print(f"Env id = {id} initialized!")
        self.id = id
        self.username = username
        self.df_transfer = meas.df_transfer
        self.df_output = meas.df_output
        self.transfer_vds_list = np.array(
            meas.transfer_vds_list, dtype=np.object)
        self.output_vgs_list = meas.output_vgs_list
        self.x_Vgs = meas.x_Vgs
        self.x_Vds = meas.x_Vds
        self.df_para = meas.df_para
        self.spice_dir = f"./workspace/{id}/"
        Xs = np.array(meas.x_Vds, dtype=np.int)
        Ys = np.array(meas.x_Vgs, dtype=np.int)

        #self.xi = np.linspace(Xs[0], Xs[-1], img_w)
        #self.yi = np.linspace(Ys[0], Ys[-1], img_h)

        self.max_im = max(
            self.df_transfer.iloc[:, 1:].max().max(),
            self.df_output.iloc[:, 1:].max().max(),
        )
        self.min_im = min(
            self.df_transfer.iloc[:, 1:].min().min(),
            self.df_output.iloc[:, 1:].min().min(),
        )

        self.max_steps = 4
        self.current_step = 0
        self.action_range = 1
        self.action_dim = 5
