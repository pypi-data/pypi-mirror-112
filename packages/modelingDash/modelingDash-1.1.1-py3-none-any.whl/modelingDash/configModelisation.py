import re, pandas as pd,datetime as dt,pickle
from dateutil import parser
from dorianUtils.configFilesD import ConfigMaster

class ConfigModelisation(ConfigMaster):
    def __init__(self,folderCSV,folderPkl=None):
        super().__init__(folderCSV)
        self.folderCSV = folderCSV
        self.folderPkl = folderPkl
        if not self.folderPkl:self.folderPkl = self.folderCSV+'pkl/'
        self.filesCsv  = self.utils.get_listFilesPklV2(self.folderCSV,'*.csv')
        self.filesPkl  = self.utils.get_listFilesPklV2(self.folderPkl)
        self.infoFiles = self.__getInfosEssais__()

    def getColumnsDF(self):
        return list(self.loadFile(self.filesPkl[0]).columns)

    def getValidFiles(self,type,ext='.pkl'):
        filenames = list(self.infoFiles[self.infoFiles.typeTrial==type].filename)
        if ext=='.pkl':filenames = [f.split('/')[-1][:-4]+ext for f in filenames]
        return filenames

    def __getInfosEssais__(self):
        dates,nameEssais,namePump,GasUsed,typePump,detailTrial,typeTrial=[],[],[],[],[],[],[]
        for filename in self.filesCsv:
            infile      = open(filename, 'r',encoding='latin-1')
            dates.append(infile.readline().split(';')[1])
            bd = filename.split('_')
            namePump.append(bd[0].split('/')[-1])
            GasUsed.append(bd[1])
            typePump.append(bd[2])
            nameEssais.append(infile.readline().split(';')[1])
            detailTrial.append('_'.join(filename.split('_')[9:])[:-4])
            if re.findall('\d{1,5}hz',filename):
                typeTrial.append('wobulationFreq')
            elif 'triangle' in filename.lower():
                typeTrial.append('triangle')
            else :
                typeTrial.append('echelon')
            infile.close()
        df = pd.DataFrame([namePump,GasUsed,typePump,typeTrial,detailTrial,dates,nameEssais,self.filesCsv],
                            index= ['namePump','gasUsed','typePump','typeTrial','detailTrial','date','nameEssai','filename'])
        return df.transpose()

    def getPossibleGasUsed(self,namePump):
        return list(self.utils.combineFilter(self.infoFiles,['namePump'],[namePump]).gasUsed.unique())

    def getPossibleTypePump(self,namePump,gasUsed):
        return list(self.utils.combineFilter(self.infoFiles,['namePump','gasUsed'],[namePump,gasUsed]).typePump.unique())

    def getPossibleTrial(self,namePump,gasUsed,typePump):
        return list(self.utils.combineFilter(self.infoFiles,['namePump','gasUsed','typePump'],[namePump,gasUsed,typePump ]).detailTrial.unique())

    def findFilename(self,namePump,gasUsed,typePump,detailTrial,ext='.pkl'):
        # print(namePump,gasUsed,typePump,detailTrial)
        dfi=self.infoFiles
        dfp = dfi[dfi.namePump==namePump]

        dfg = dfp[dfp.gasUsed==gasUsed]
        if dfg.empty:
            print('trial : of '+ namePump,'has no trial with gas ' + gasUsed)
            print(dfp)
            return dfp

        dft = dfg[dfg.typePump==typePump]
        if dft.empty:
            print('trial : of '+ namePump + 'and gas ' + gasUsed +'has no trial with typePump ' + typePump)
            print(dfg)
            return dfg

        dfd = dft[dft.detailTrial==detailTrial]
        if dfd.empty:
            print('trial : of '+ namePump,'and gas ' + gasUsed + ' and typePump ' + typePump + 'has no trial with detailTrial ' + detailTrial)
            print(dft)
            return dft
        filename = dfd.filename.iloc[0]
        if ext == '.pkl' : filename = self.folderPkl+filename.split('/')[-1][:-4]+'.pkl'
        return filename

    def read_csv(self,filename,encode="latin-1",**kwargs):
        df = pd.read_csv(filename,sep=';',decimal=',',encoding=encode,low_memory=False,**kwargs)
        df = df.iloc[:,~df.columns.str.contains('Unnamed')]
        dateTrial=parser.parse(df.columns[1])
        df.index=[dateTrial+dt.timedelta(milliseconds=k) for k in df['Temps (ms)']]
        df = df.drop(df.columns[[0,1]],axis=1)
        return df

    def convert_csv2pkl(self):
        import os
        if not os.path.exists(self.folderPkl) : os.mkdir(self.folderPkl)
        for f in self.filesCsv:
            print(f)
            df = self.read_csv(f)
            df = self.computePhysics(df)
            filePkl = self.folderPkl + f.split('/')[-1][:-4] + '.pkl'
            print('saving pkl : ',filePkl)
            with open(filePkl , 'wb') as handle:
                pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def getUnits(self,listCols,pattern='unitsInParenthesis'):
        if pattern == 'unitsInParenthesis':
            return [re.findall('\([\w\W]+\)',x)[0][1:-1] for x in listCols]

    def computePhysics(self,df):
        df['Temps (s)']  = df.filter(regex='\(ms\)', axis=1)/1000
        df['pression rel.(Pa)'] = df.filter(regex='PR33X', axis=1)*100
        try : df['pression abs.(Pa)'] = df.filter(regex='PAA33X', axis=1)*100
        except: print('column containing PAA33X is absent in dataframe')
        try: df['massflow (m3/s)'] = df.filter(regex='\(l/h\)', axis=1)/3600/1000#m3/s
        except: print('column containing (l/h) is absent in dataframe')
        try : df['electric power (W)']  = 24*df.filter(regex='\(A\)', axis=1)
        except: print('column containing (A) is absent in dataframe')
        df['hydraulic power (W)'] = df['pression rel.(Pa)']*df['massflow (m3/s)']
        df['yield (%)'] = df['hydraulic power (W)']/df['electric power (W)']*100
        return df

    def getSteadyStates(self,df,trfinims=90100,lastPtsForMean = 100):
        dfSS = df[df['Temps (ms)']>trfinims] ## select only the data after a certain time to surpress the ramp
        if 'Consigne' in dfSS.columns : dfSS = dfSS[dfSS['Consigne'].diff()<-dfSS.Consigne.max()/20]
        elif 'Consigne (pts ou mbars)' in dfSS.columns : dfSS = dfSS[dfSS['Consigne (pts ou mbars)'].diff()<-dfSS['Consigne (pts ou mbars)'].max()/20]
        elif 'Sortie ana. (pts)' in dfSS.columns : dfSS = dfSS[dfSS['Sortie ana. (pts)'].diff()<-dfSS['Sortie ana. (pts)'].max()/20]
        else :
            print('Consigne ',',Consigne (pts ou mbars) ','et Sortie ana. (pts) ne sont pas des colonnes du df')
            return pd.DataFrame()
        if not dfSS.empty:
            dfSS=pd.concat([df.loc[k-dt.timedelta(seconds=6)] for k in dfSS.index],axis=1).transpose()
        return dfSS

    def decomposeFrequences(self,df):
        allFreq = np.unique(fr)
        freqk   = allFreq[k]
        listIdx = (fr[fr==freqk]).index.values.tolist()# get all the indexes
        s = slice(listIdx[0],listIdx[round(len(listIdx)/dw)],1)
        dfU     = columns_in_SI(df,s)
        return listDfFreq

    def get_AllsteadyStates(self,filenames):
        dfs = []
        for filename in filenames:
            print(filename)
            df = self.loadFile(filename)
            df = self.getSteadyStates(df)
            df['filename'] = filename.split('/')[-1]
            dfs.append(df)
            # print(df)
        dfT = pd.concat(dfs,axis=0)
        return dfT

    def plotCheckdfS(self,filePkl):
        import plotly.graph_objects as go

        df   = self.loadFile(filePkl)
        dfSS = self.getSteadyStates(df)
        trace1 = go.Scatter(x=dfSS.index,y=dfSS['Consigne'],name='sample',mode='markers',
                            marker=dict(symbol='circle',size=10))
        trace2 = go.Scatter(x=df.index,y=df['Consigne'],name='Consigne')
        fig = go.Figure([trace1,trace2])
        return fig

    '''to do '''
    # def computeBodeDiagramm(self,df):
