import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#calcule la vitesse de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de la vitesse
def calcVitesse(df):
    return df.assign('Vitesse', np.sign(df.get('[00].VehicleUpdate-speed.001'))*np.sqrt(df.get('[00].VehicleUpdate-speed.001')**2 + df.get('[00].VehicleUpdate-speed.002')**2 + df.get('[00].VehicleUpdate-speed.003')**2))

#calcule la distance parcourue de la voiture du début du dataframe à la fin
#Colonne panda 'Vitesse' doit être présente
#in: dframe
#out: nouveau dataframe avec insertion de la distance
def calcDistance(df):
    tdf = df.fillna(value=0)
    return df.assign(0, 'distance', (df.get('Vitesse')*df.index[1]).cumsum())

#calcule le schema de la courbe de vitesse
def plotVitesse(dfAn, dfAgg, dfDef):
    fig = plt.figure(0)
    plt.plot(dfAn['distance'], dfAn['Vitesse'], label='User', color='blue')
    plt.plot(dfAgg['distance'], dfAgg['Vitesse'], label='Aggresiv', color='red')
    plt.plot(dfDef['distance'], dfDef['Vitesse'], label = 'Cautious', color = 'green')
    plt.legend()
    plt.xlabel('Distance m')
    plt.ylabel('Vitesse m/s')
    return fig