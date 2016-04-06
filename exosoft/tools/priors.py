#@Author: Kyle Mede, kylemede@astron.s.u-tokyo.ac.jp
import numpy as np
import constants
import settings as sett

########################################
#Define the priors as python functions #
########################################
#NOTE: only change the code and not the name of the functions or their inputs.
def ePriorRatio(eProposed,eLast):
    if (sett.settings['lowEcc'][0]==False)and(sett.settings['eMAX']!=0):
        if eProposed!=eLast!=0:
            if (sett.settings['PMIN']*constants.daysPerYear)>1000.0:
                return eProposed/eLast
            else:
                return 1.0
        else:
            return 1.0
    else:
        return 1.0
    
def pPriorRatio(Pproposed,Plast):
    if sett.settings['PMAX']!=0:
        if Pproposed!=0:
            return Plast/Pproposed
        else:
            return 1.0
    else:
        return 1.0
    
def incPriorRatio(incProposed,incLast):
    if sett.settings['incMAX']!=0:
        if (incLast%90.0)!=0:
            return np.sin(incProposed*(constants.pi/180.0))/np.sin(incLast*(constants.pi/180.0))
        else:
            return 1.0
    else:
        return 1.0
    
def mass1PriorRatio(MProposed,MLast):
    if (sett.settings['mass1MAX']!=0)and True:
        if MProposed!=MLast!=0:
            prop = pdmfPrior(MProposed)
            lst = pdmfPrior(MLast)
            return prop/lst
        else:
            return 1.0
    else:
        return 1.0
    
def mass2PriorRatio(m2Prop,m2Last,m1Prop,m1Last):
    if (sett.settings['mass2MAX']!=0)and True:
        if 0.0 not in [m2Prop,m2Last,m1Prop,m1Last]:
            prop = cmfPrior(m2Prop,m1Prop)
            lst = cmfPrior(m2Last,m1Last)
            return prop/lst
        else:
            return 1.0
    else:
        return 1.0
    
def paraPriorRatio(paraProposed,paraLast):
    if paraProposed!=paraLast!=sett.settings['paraMAX']!=0:
        ratioA = (paraLast**4.0)/(paraProposed**4.0)
        ratioB = 1.0
        if sett.settings['paraEst'][0]!=0:
            ## a Gaussian prior centered on hipparcos and width of hipparcos estimated error
            top = gaussian(paraProposed, sett.settings['paraEst'][0], sett.settings['paraErr'][0])
            btm = gaussian(paraLast, sett.settings['paraEst'][0], sett.settings['paraErr'][0])
            ratioB = top/btm
        return ratioA*ratioB
    else:
        return 1.0
    
def imfPrior(m):
    if m<1.0:
        d = (0.068618528140713786/m)*np.exp((-(np.log10(m)+1.1023729087095586)**2)/0.9521999999999998)
    else:
        d = 0.019239245548314052*(m**(-2.3))
    return d

def pdmfPrior(m):
    if m<1.0:
        d = (0.068618528140713786/m)*np.exp((-(np.log10(m)+1.1023729087095586)**2)/0.9521999999999998)
    elif m<3.47:
        d = 0.019108957203743077*(m**(-5.37))
    elif m<18.20:
        d = 0.0065144172285487769*(m**(-4.53))
    else:
        d = 0.00010857362047581295*(m**(-3.11))
    return d

def cmfPrior(m2,m1):
    beta = -0.39
    d = (m2**(beta))*(m1**(-1.0*beta-1.0))
    return d

def gaussian(x,mu,sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

#END OF FILE