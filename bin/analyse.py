import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import erreur
"""
    Ce script comporte les fonctions de calculs de ressemblance des courbes
    Il contient aussi les formatages de csv pour l'interpolation du temporel vers le spatial
"""
gdfa = None #dataframe utilisateur  
gdf1 = None #dataframe style1
gdf2 = None #dataframe style2

#calcule la vitesse de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de la vitesse
def calcVitesse(df):
    """
    Calcul la vitesse en faisant la norme des vecteurs vitesse et en prenant le signe du vecteur vitesse x, soit la direction dans l'axe du chassis du véhicule 0.
    Args:
        df:   dataframe panda indexé sur 'time' et comportant '[00].VehicleUpdate-speed.001', '[00].VehicleUpdate-speed.002', '[00].VehicleUpdate-speed.003'
    Returns:
        tdf : une copie du dataframe panda auquel on a ajouté la colonne 'Vitesse' en première position
    """
    tdf = df.fillna(value=0)
    tdf.insert(0, 'Vitesse', np.sign(tdf.get('[00].VehicleUpdate-speed.001'))*np.sqrt(tdf.get('[00].VehicleUpdate-speed.001')**2 + tdf.get('[00].VehicleUpdate-speed.002')**2 + tdf.get('[00].VehicleUpdate-speed.003')**2))
    return tdf

#calcule l'acceleration de la voiture 
#in: dframe
#out: nouveau dataframe avec insertion de l'acceleration
def calcAccel(df):
    """
    Calcul l'acceleration en faisant la norme des vecteurs acceleration et en prenant le signe du vecteur acceleration x, soit la direction dans l'axe du chassis du véhicule 0.
    Args:
        df:   dataframe panda indexé sur 'time' et comportant '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002', '[00].VehicleUpdate-accel.003'
    Returns:
        tdf : une copie du dataframe panda auquel on a ajouté la colonne 'Acceleration' en première position
    """
    tdf = df.fillna(value=0)
    tdf.insert(0, 'Acceleration', np.sign(tdf.get('[00].VehicleUpdate-accel.001'))*np.sqrt(tdf.get('[00].VehicleUpdate-accel.001')**2 + tdf.get('[00].VehicleUpdate-accel.002')**2 + tdf.get('[00].VehicleUpdate-accel.003')**2))
    return tdf

#calcule la distance parcourue de la voiture du début du dataframe à la fin
#Colonne panda 'Vitesse' doit être présente
#in: dframe
#out: nouveau dataframe avec insertion de la distance
def calcDistance(df):
    """
    Calcul la distance à l'instant t depuis le début du tableau. La fréquence d'échantillonage doit être constante.
    Args:
        df:   dataframe panda indexé sur 'time' et comportant 'Vitesse'.
    Returns:
        tdf: une copie du dataframe panda auquel on a ajouté la colonne 'distance' en première position
    """
    tdf = df.fillna(value=0)
    tdf.insert(0, 'distance', (tdf.get('Vitesse')*(tdf.index[1]-tdf.index[0])).cumsum())
    return tdf

#calcule le schema de la courbe de vitesse
def plotVitesse(dfAn, df1, df2, glabel, label0 = 'User', label1 = 'style1', label2 = 'style2'):
    """
    Calcul la pyplot.fig qui représente les courbes de vitesse des trois dataframes.
    Args:
        dfAn:   dataframe panda (a analyser) indexé sur 'time' et comportant 'distance' et 'Vitesse'.
        df1 :   dataframe panda (du style 1) indexé sur 'time' et comportant 'distance' et 'Vitesse'.
        df2 :   dataframe panda (du style 2) indexé sur 'time' et comportant 'distance' et 'Vitesse'.
    Kwargs:
        label0: string, nom de la courbe à analyser.
        label1: string, nom de la courbe du style 1.
        label2: string, nom de la courbe du style 2.
    Returns:
        fig : pyplot.fig contenant les courbes de vitesses
    """
    fig = plt.figure(glabel, figsize=(5,3.7))
    plt.plot(dfAn['distance'], dfAn['Vitesse'], label = label0, color = 'blue')
    plt.plot(df1['distance'], df1['Vitesse'], label = label1, color = 'red')
    plt.plot(df2['distance'], df2['Vitesse'], label = label2, color = 'green')
    plt.legend()
    plt.xlabel('Distance m')
    plt.ylabel('Vitesse m/s')
    plt.close(fig)
    return fig

#calcule le schema de la courbe d'acceleration
def plotAcceleration(df0, df1, df2, glabel, label0 = 'User', label1 = 'style1', label2 = 'style2'):
    """
    Calcul la pyplot.fig qui représente les courbes d'acceleration des trois dataframes.
    Args:
        dfAn:   dataframe panda (a analyser) indexé sur 'time' et comportant 'distance' et 'Acceleration'.
        df1 :   dataframe panda (du style 1) indexé sur 'time' et comportant 'distance' et 'Acceleration'.
        df2 :   dataframe panda (du style 2) indexé sur 'time' et comportant 'distance' et 'Acceleration'.
    Kwargs:
        label0: string, nom de la courbe à analyser.
        label1: string, nom de la courbe du style 1.
        label2: string, nom de la courbe du style 2.
    Returns:
        fig : pyplot.fig contenant les courbes d'acceleration
    """
    fig = plt.figure(glabel, figsize=(5,3))
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
def filter(string, parseString = "Parser"):
    """
    Reconnait une chaine de caractère comme un nom de délimiteur de tronçon.
    La chaine doit commencer par parseString et se terminer par un nombre.
    Args:
        string: Chaine de caractère
    Kwargs:
        parseString: le nom des triggers délimitants un tronçon sans le chiffre à la fin.
    Returns:
        bolean
    """
    if re.match(parseString + "\d*", string) != None:
        return True
    else:
        return False

#traduit la colonne des trigger en int et leur etat
def trigToInt(df):
    """
    Transforme les noms des triggers délimitants les tronçons en integers ainsi que leurs états.
    Args:
        df: dataframe panda contenant 'TriggeredState-name' et 'TriggeredState-state'.
    Returns:
        dataf: copie de df contenant des int dans les colonnes d'états et de noms
    """
    dataf = df.copy()
    
    name_loc = df.columns.get_loc('TriggeredState-name') # recupération des emplacements des colonnes
    state_loc = df.columns.get_loc('TriggeredState-state')
    
    for i in range(int(df.shape[0])):
        dataf.iloc[i, name_loc] = int(dataf.iloc[i, name_loc][6:]) #traduction en int des nom de parser
        
    dataf.iloc[:, state_loc] = dataf.iloc[:, state_loc].astype(int) #traduction en int des états de parser
    
    return dataf


#retourne l'index de la première et dernière valeur du tronçon
def getIndex(data, i):
    """
    Calcul et retourne les indexes de départ du tronçon i dans le dataframe data
    Args:
        data: dataframe panda contenant 'TriggeredState-name', colonne contenant des integers
        i: numéro du tronçon
    Returns:
        (iBegin,iEnd) : tuple des index de départ et d'arrivé
    """
    return (data[data['TriggeredState-name'] == i].head(1).index, data[data['TriggeredState-name'] == i+1].head(1).index)

#à partir d'un dataframe, découpe en tableaux de dataframes en fonctions des triggers
#TODO exeption de nb impair de triggers
def parse(dataf, parseString = "Parser"):
    """
    Sépare dataf en un tableau selon les tronçons.
    Args:
        dataf: dataframe panda contenant 'TriggeredState-name', 'TriggeredState-state'
    Kwargs:
        parseString: le nom des triggers délimitants un tronçon sans le chiffre à la fin.
    Returns:
        tableD: le tableau contenant des dataframes panda, les differents tronçons.
    """
    df = dataf[[filter(str(x), parseString) for x in dataf['TriggeredState-name'].fillna(value="0")]]#filtration des bon formats de parsers
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
    """
    donne la ligne de df la plus proche de la distance d. Utilisé pour l'interpolation.
    Args:
        df: dataframe panda contenant 'distance'
        d: integers représentant la distance désiré
    Returns:
        dataframe de 1 ligne de df
    """
    return df.iloc[(df['distance']-d).abs().argmin()]

#création du sataframe avec les valeurs de d2 indexé sur la distance de d1
def createClosestD(df1,df2):
    """
    Interpolation de df2.
    Création du dataframe avec les valeurs de df2 indexé sur df1.
    On prend la ligne de df2 la plus proche de la distance de df1 pour chauque valeurs de df1.
    Args:
        df1: dataframe panda contenant 'distance'
        df2: dataframe panda contenant 'distance'
    Returns:
        ndf2: copie de df2 indexé sur df1
    """ 
    l = []
    for x in df1['distance']:
        l.append([y for y in getClosestD(df2,x)])
    ndf2 = pd.DataFrame(l,columns = df1.columns) #recupération des lignes de df2 ayant la distance la plus proche de df1
    ndf2 = ndf2.set_index(pd.Series(df1.index, name = 'time')) #alignement de ndf2 sur l'index de df1
    return ndf2

#normalisation de x entre -1 et 1
def norm(x):
    """
    Fonction de normalisation de x entre -1 et 1.
    Fonction dérivé de la softmax de 1 élément.
    Args:
        x: integer
    Returns:
        float entre -1 et 1
    """ 
    return((1/(1+np.exp(-x/10))-0.5)*2)

#fonction de calcul de proximité basique des courbes de vitesses
#in deux dataframes indexés sur 'distance'. Doivent contenir le champs 'Vitesse'
def vitesseMSE(df1,df2):
    """
    Calcul de l'erreur quadratique de la vitesse de df2 par rapport à df1
    Args:
        df1: dataframe panda contenant 'Vitesse'
        df2: dataframe panda contenant 'Vitesse'
    Returns:
        float
    """ 
    return norm(((df1['Vitesse'].to_numpy() - df2['Vitesse'].to_numpy())**2).mean())

#fonction de calcul de proximité basique des courbes d'accceleration
#in deux dataframes indexés sur 'distance'. Doivent contenir le champs 'Acceleration'
def accelerationMSE(df1,df2):
    """
    Calcul de l'erreur quadratique de l'acceleration de df2 par rapport à df1
    Args:
        df1: dataframe panda contenant 'Acceleration'
        df2: dataframe panda contenant 'Acceleration'
    Returns:
        float
    """ 
    return norm(((df1['Acceleration'].to_numpy() - df2['Acceleration'].to_numpy())**2).mean())

#fonction de correlation de Pierson point à point pour l'acceleration et la vitesse
# 1 : ressemblance parfaite
# 0 : aucune ressemblance
def correlation(df1, df2):
    """
    Calcul de la correlation de la vitesse et de l'acceleration entre df1 et df2
    Args:
        df1: dataframe panda contenant 'Vitesse', 'Acceleration'
        df2: dataframe panda contenant 'Vitesse', 'Acceleration'
    Returns:
        float
    """ 
    coef = np.corrcoef(df1[['Vitesse','Acceleration']].to_numpy(), df2[['Vitesse','Acceleration']].to_numpy(), rowvar=False)
    coef[coef<0] = 0 # on ne veut que la ressemblance, pas la symétrie/opposition
    return norm(coef.sum())

#renvoi le score de proximité de df avec df1 et df2
#out : si < 0 , le style df1 est le plus ressemblant, si > 0 c'est le stle df2
def score(df,df1,df2, coeffAcc = 1, coefVit = 1):
    """
    Calcul du score de ressemblance de df avec df1 et df2.
    Si score() < 0, le style df1 est le plus ressemblant
    Si score() > 0, le style df2 est le plus ressemblant
    
    On utilise la mse de la vitesse, la mse de l'acceleration et la correlation des vitesses et des accelerations
    
    Args:
        df: dataframe panda contenant 'Vitesse', 'Acceleration'
        df1: dataframe panda contenant 'Vitesse', 'Acceleration'
        df2: dataframe panda contenant 'Vitesse', 'Acceleration'
    Kwargs:
        coeffAcc: float entre 0 et 1. Coefficient du paramètre d'acceleration.
        coeffVit: float entre 0 et 1. Coefficient du paramètre de vitesse
    Returns:
        float
    """ 
    ndf1 = createClosestD(df, df1)
    ndf2 = createClosestD(df, df2)
    return coefVit*(vitesseMSE(df,ndf1) - vitesseMSE(df,ndf2)) + coeffAcc*(accelerationMSE(df,ndf1) - accelerationMSE(df,ndf2)) + correlation(df,ndf2) - correlation(df,ndf1)

#renvoie les scores des vitesses poour chaques tronçons 
def get_score(dfa, df1, df2, coeffAcc = 1, coefVit = 1, parseString = "Parser"):
    """
    Calcul du score de ressemblance de df avec df1 et df2 pour chaques tronçons
    
    Args:
        df: dataframe panda
        df1: dataframe panda 
        df2: dataframe panda 
    Kwargs:
        coeffAcc: float entre 0 et 1. Coefficient du paramètre d'acceleration.
        coeffVit: float entre 0 et 1. Coefficient du paramètre de vitesse
        parseString: le nom des triggers délimitants un tronçon sans le chiffre à la fin.
    Returns:
        tab[tronçons]: tableau des scores par tronçon
    """

    csvs = [dfa, df1, df2]
    DV = [calcDistance(calcVitesse(calcAccel(x))) for x in csvs]
    tronc = np.transpose([parse(x, parseString) for x in DV])

    #mise à jour des tableau pour le téléchargement des données
    global gdfa
    gdfa = dfa
    global gdf1
    gdf1 = df1
    global gdf2 
    gdf2 = df2
    
    return [[score(x[0], x[1], x[2], coeffAcc, coefVit)] for x in tronc]

#renvoie le score global de tout les tronçons
#tabScore : le tableau de score renvoyé par get_score
#tabPoid : le tableau des poids associés aux troncons
def get_score_global(tabScore, tabPoids):
    """
    Calcul du score global.
    
    Args:
        tabScore: tableau de score des troçons
        tabPoids: tableau des poids des tronçons
    Returns:
        float
    """
    return (np.array(tabScore)*np.array(tabPoids)).sum()

#retourne les tableau de données utilisées
def get_data():
    """
    Permet de récuperer les dataframes utilisé pour l'analyse, donc avec l'interpolation.
    Returns:
        (gdfa, gdf1, gdf2): dataframes panda
    """
    global gdfa
    global gdf1
    global gdf2
    return gdfa, gdf1, gdf2

#calcul le tableau de grtaphiques tronçons*features
#TODO multi paramêtres et multi tronçons
def plot_graph(dfAn, df1, df2, label0 = 'User', label1 = 'style1', label2 = 'style2', parseString = "Parser"):
    """
    Contructions des graph de vitesses et d'accelerations.
    
    Args:
        dfAn: dataframe panda indexé sur 'time' ayant '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002', '[00].VehicleUpdate-accel.003', 'TriggeredState-name' et 'TriggeredState-state'
        df1: dataframe panda indexé sur 'time' ayant '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002', '[00].VehicleUpdate-accel.003', 'TriggeredState-name' et 'TriggeredState-state'
        df2: dataframe panda indexé sur 'time' ayant '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002', '[00].VehicleUpdate-accel.003', 'TriggeredState-name' et 'TriggeredState-state'
    Kwargs:
        label0: string, nom de la courbe à analyser.
        label1: string, nom de la courbe du style 1.
        label2: string, nom de la courbe du style 2.
    Returns:
        tab[tronçons*parametre]: tableau des pyplot.fig
    """
    csvs = [dfAn, df1, df2]
    DV = [calcDistance(calcVitesse(calcAccel(x))) for x in csvs]
    #tronc = np.transpose([parse(x, parseString) for x in DV])
    tronc = [parse(x, parseString) for x in DV]
    
    #verification de la coherence du nombre de tronçons entre les dataframes
    taille = np.array([len(x) for x in tronc])
    if not all((taille == taille[0])): 
        print("#####################\nErreur du nombre de triggers. Vérifiez les fichiers d'entrées\n#####################")
        erreur.callback("Erreur du nombre de triggers. Vérifiez les fichiers d'entrées.")
        return []
    
    tronc = np.transpose(tronc)
    ids = [x for x in range(len(tronc))]
    return [[plotVitesse(x[0], x[1], x[2], id, label0, label1, label2),plotAcceleration(x[0], x[1], x[2], id+100, label0, label1, label2)] for (x,id) in zip(tronc,ids)]