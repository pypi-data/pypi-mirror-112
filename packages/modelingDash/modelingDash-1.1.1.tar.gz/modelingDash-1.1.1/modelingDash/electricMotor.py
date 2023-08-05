# from utils import*
# plt.close('all')

def modelingRonan(Kb=1,E=48):
    C = np.linspace(0,500,100) #Nm
    Cmax =  500#Nm

    Cv = 50
    I = Kb*(C+Cv)

    omega0 = 4000
    omega = omega0*(1 - C/Cmax)

    Pabs = E*I
    Pmeca = C*omega*2*np.pi/60 #W

    eta=Pmeca/Pabs
    etaN =eta/eta.max()
    PmecaN=Pmeca/Pmeca.max()
    omegaN=omega/omega.max()
    IN=I/I.max()
    PabsN=Pabs/Pabs.max()
    CN=C/C.max()
    return

def plotRonan():
    plts = [[omega,etaN  ,'g-' ,r'$\eta$'],
            [omega,PmecaN,'b--',r'$P_{meca}(W)$'],
            [omega,CN    ,'m',r'$C(Nm)$'],
            [omega,IN ,'r',r'$I(A)$']
            ]
    pathFig='moteurCurveSimulated.png'
    fig,ax = dsp.stddisp(plts,xylims=['y',-0.05,1.05],texts=[[3090,1.02,'$\eta_{max}$','g']],
        labs=[r'$N(tr/min)$','normalized unit'],lw=2,fonts={'lab':25},axPos=[0.2, 0.1,0.7,0.8],
        name=pathFig,opt='sc')
    dsp.addyAxis(fig,ax,[[omega,IN ,'r','']],'I(A)','r')

# Km=tau/sqrt(P)
import pandas as pd,numpy as np

def caraDC_Motor_SS(Kt,Ke,Ra,ei=24,torqueMax=50,N=1000):
    '''
    Kt : electromotric force (lorentz)
    Ke : induction (lenz) or couterelectromotric force
    Ra : resistance in Ohm
    ei : voltage in Volt
    '''
    df=pd.DataFrame()
    df['torque (Nm)'] = np.linspace(0,torqueMax,N)
    df['I (A)']=df['torque (Nm)']/Kt
    df['speed (rad/s)']=(ei-df['I (A)']*Ra)/Ke
    df['speed (tours/min)']=df['speed (rad/s)']/np.pi*60
    df['Mecanical power (W)']=df['torque (Nm)']*df['speed (rad/s)']
    df['Electrical power (W)']=df['I (A)']*ei
    df['yield (%)']=df['Mecanical power (W)']/df['Electrical power (W)']
    df = df.set_index('torque (Nm)')
    return df


def plotElectricMotor(Kt,Ke,Ra,**kwargs):
    df = caraDC_Motor_SS(Kt=Kt,Ke=Ke,Ra=Ra,**kwargs)
    from dorianUtils.utilsD import Utils
    utils=Utils()
    fig=utils.multiYAxis(df.iloc[:,[0,2,3,4,5]])
    fig=utils.updateStyleGraph(fig)
    params = {'Kt':Kt,'Ke':Ke,'Ra':Ra,}
    fig=utils.quickLayout(fig,title='electric motor characteristic ' + utils.figureName(params),xlab='torque(Nm)',style='std')
    return fig
plotElectricMotor(3,1,1,ei=24,torqueMax=80).show()
# df = caraDC_Motor_SS(30,1,5,48,40)
