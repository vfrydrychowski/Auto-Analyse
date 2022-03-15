import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

#calcule la vitesse de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de la vitesse
def calcVitesse(df):
    tdf = df.copy()
    tdf.insert(0, 'Vitesse', np.sign(df.get('[00].VehicleUpdate-speed.001'))*np.sqrt(df.get('[00].VehicleUpdate-speed.001')**2 + df.get('[00].VehicleUpdate-speed.002')**2 + df.get('[00].VehicleUpdate-speed.003')**2))
    return tdf

#calcule la distance parcourue de la voiture du début du dataframe à la fin
#Colonne panda 'Vitesse' doit être présente
#in: dframe
#out: nouveau dataframe avec insertion de la distance
def calcDistance(df):
    tdf = df.fillna(value=0)
    tdf.insert(0, 'distance', (df.get('Vitesse')*df.index[1]).cumsum())
    tdf = df.fillna(value=0)
    return tdf

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

#reconnait une string comme le nom d'un délimiteur de tronçons
#in: une string
#out: un bool
def filter(string):
    if re.match("Parser\d*", string) != None:
        return True
    else:
        return False

#traduit la colonne des trigger en int et leur etat
def trigToInt(df):
    dataf = df.copy()
    
    name_loc = df.columns.get_loc('TriggeredState-name') # recupération des emplacements des colonnes
    state_loc = df.columns.get_loc('TriggeredState-state')
    
    for i in range(int(df.shape[0])):
        dataf.iloc[i, name_loc] = int(dataf.iloc[i, name_loc][6:]) #traduction en int des nom de parser
        
    dataf.iloc[:, state_loc] = dataf.iloc[:, state_loc].astype(int) #traduction en int des états de parser
    
    return dataf

#fonction boolean de masque du troncon i
def isTroncon(df,i):
    return df['TriggeredState-name'] == i or (df['TriggeredState-name'] == i+1 and df['TriggeredState-state'] == 1)

#à partir d'un dataframe, découpe en tableaux de dataframes en fonctions des triggers
#TODO exeption de nb impair de triggers
def parse(dataf):
    df = dataf[[filter(x) for x in dataf['TriggeredState-name'].fillna(value="0")]]
    df = trigToInt(df)
    dim = len(df['TriggeredState-name'].unique()) #calcul du nombre de triggers
    tableD = [df[isTroncon(df,i)] for i in range(dim/2)]
    return tableD

#calcul le tableau de grtaphiques features*tronçons
#TODO multi paramêtres et multi tronçons
def plot_graph(dfAn, dfAgg, dfDef):
    dfAn, dfAgg, dfDef = calcDistance(calcVitesse(dfAn)), calcDistance(calcVitesse(dfAgg)), calcDistance(calcVitesse(dfDef))
    return [[plotVitesse(dfAn, dfAgg, dfDef)]]