import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.special as spef
import re

#calcule la vitesse de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de la vitesse
def calcVitesse(df):
    tdf = df.fillna(value=0)
    tdf.insert(0, 'Vitesse', np.sign(tdf.get('[00].VehicleUpdate-speed.001'))*np.sqrt(tdf.get('[00].VehicleUpdate-speed.001')**2 + tdf.get('[00].VehicleUpdate-speed.002')**2 + tdf.get('[00].VehicleUpdate-speed.003')**2))
    return tdf

#calcule l'acceleration de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de l'acceleration
def calcAccel(df):
    tdf = df.fillna(value=0)
    tdf.insert(0, 'Acceleration', np.sign(tdf.get('[00].VehicleUpdate-accel.001'))*np.sqrt(tdf.get('[00].VehicleUpdate-accel.001')**2 + tdf.get('[00].VehicleUpdate-accel.002')**2 + tdf.get('[00].VehicleUpdate-accel.003')**2))
    return tdf

#calcule la distance parcourue de la voiture du début du dataframe à la fin
#Colonne panda 'Vitesse' doit être présente
#in: dframe
#out: nouveau dataframe avec insertion de la distance
def calcDistance(df):
    tdf = df.fillna(value=0)
    tdf.insert(0, 'distance', (tdf.get('Vitesse')*(tdf.index[1]-tdf.index[0])).cumsum())
    return tdf

#calcule le schema de la courbe de vitesse
def plotVitesse(dfAn, dfAgg, dfDef, glabel, label0 = 'User', label1 = 'style1', label2 = 'style2'):
    fig = plt.figure(glabel)
    plt.plot(dfAn['distance'], dfAn['Vitesse'], label = label0, color = 'blue')
    plt.plot(dfAgg['distance'], dfAgg['Vitesse'], label = label1, color = 'red')
    plt.plot(dfDef['distance'], dfDef['Vitesse'], label = label2, color = 'green')
    plt.legend()
    plt.xlabel('Distance m')
    plt.ylabel('Vitesse m/s')
    plt.close(fig)
    return fig

#calcule le schema de la courbe d'acceleration
def plotAcceleration(df0, df1, df2, glabel, label0 = 'User', label1 = 'style1', label2 = 'style2'):
    fig = plt.figure(glabel)
    plt.plot(df0['distance'], df0['Acceleration'], label = label0, color = 'blue')
    plt.plot(df1['distance'], df1['Acceleration'], label = label1, color = 'red')
    plt.plot(df2['distance'], df2['Acceleration'], label = label2, color = 'green')
    plt.legend()
    plt.xlabel('Distance m')
    plt.ylabel('Acceleration m/s²')
    plt.close(fig)
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

#retourne l'index de la première et dernière valeur du tronçon
def getIndex(data, i):
    return (data[data['TriggeredState-name'] == i].head(1).index, data[data['TriggeredState-name'] == i+1].head(1).index)

#à partir d'un dataframe, découpe en tableaux de dataframes en fonctions des triggers
#TODO exeption de nb impair de triggers
def parse(dataf):
    df = dataf[[filter(str(x)) for x in dataf['TriggeredState-name'].fillna(value="0")]]#filtration des bon formats de parsers
    df = trigToInt(df)
    dim = len(df['TriggeredState-name'].unique()) #calcul du nombre de triggers
    
    diml = df['TriggeredState-name'].unique() 
    diml = diml[diml%2 == 0] #liste des identifiants de triggers de début de troncons
    
    tableD = [0] * (dim//2)
    for i in range(dim//2):
        f,l = getIndex(df, diml[i])
        tableD[i] = df.loc[f[0]:l[0]]
    return tableD

#donne la ligne du dataframe la plus proche de la distance d
def getClosestD(df,d):
    return df.iloc[(df['distance']-d).abs().argmin()]

#création du sataframe avec les valeurs de d2 indexé sur la distance de d1
def createClosestD(df1,df2): 
    l = []
    for x in df1['distance']:
        l.append([y for y in getClosestD(df2,x)])
    ndf2 = pd.DataFrame(l,columns = df1.columns)
    dist2 = pd.Series(df1['distance'].values, name = 'distance', index = df1.index) #alignement de la distance sur celle du premier tableau
    df2.update(dist2)
    df2.set_index('distance')
    return ndf2

#fonction de calcul de proximité basique des courbes de vitesses
#in deux dataframes indexés sur 'distance'. Doivent contenir le champs 'Vitesse'
def vitesseMSE(df1,df2):
    return spef.softmax(((df1['Vitesse'].to_numpy() - df2['Vitesse'].to_numpy())**2).mean())

#fonction de calcul de proximité basique des courbes d'accceleration
#in deux dataframes indexés sur 'distance'. Doivent contenir le champs 'Acceleration'
def accelerationMSE(df1,df2):
    return spef.softmax(((df1['Acceleration'].to_numpy() - df2['Acceleration'].to_numpy())**2).mean())

#renvoi le score de proximité de df avec df1 et df2
#out : si < 0 , le style df1 est le plus ressemblant, si > 0 c'est le stle df2
def score(df,df1,df2, coeffAcc = 1, coefVit = 1):
    ndf1 = createClosestD(df,df1)
    ndf2 = createClosestD(df, df2)
    return coefVit*(vitesseMSE(df,ndf1) - vitesseMSE(df,ndf2)) + coeffAcc*(accelerationMSE(df,ndf1) - accelerationMSE(df,ndf2))

#renvoie les scores des vitesses poour chaques tronçons 
def get_score(dfa, df1, df2, coeffAcc = 1, coefVit = 1):
    csvs = [dfa, df1, df2]
    DV = [calcDistance(calcVitesse(calcAccel(x))) for x in csvs]
    tronc = np.transpose([parse(x) for x in DV])
    return [[score(x[0], x[1], x[2], coeffAcc, coefVit)] for x in tronc]

#calcul le tableau de grtaphiques tronçons*features
#TODO multi paramêtres et multi tronçons
def plot_graph(dfAn, dfAgg, dfDef):
    csvs = [dfAn, dfAgg, dfDef]
    DV = [calcDistance(calcVitesse(calcAccel(x))) for x in csvs]
    tronc = np.transpose([parse(x) for x in DV])
    ids = [x for x in range(len(tronc))]
    return [[plotVitesse(x[0], x[1], x[2], id),plotAcceleration(x[0], x[1], x[2], id+100)] for (x,id) in zip(tronc,ids)]