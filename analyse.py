import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#calcule la vitesse de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de la vitesse
def calcVitesse(df):
    return df.insert(2,'Vitesse', np.sign(df.get('[00].VehicleUpdate-speed.001'))*np.sqrt(df.get('[00].VehicleUpdate-speed.001')**2 + df.get('[00].VehicleUpdate-speed.002')**2 + df.get('[00].VehicleUpdate-speed.003')**2))