#2017 TheBinaryEdge.net --- Happy trading!

import pandas as pd
import numpy as np
import quandl

Key = raw_input("Enter Quandl Key:")
SelectedContract = " "

print "Select Contract: (Type the number associated with the contract to retrieve information.)\n"
print "1: Yen  ||  2: Ruble  ||  3: Real  ||  4: VIX  ||  5: Peso  ||  6: Canadian Dollar  ||  7: Eurodollar  ||  8: Aussie Dollar"
print "9: U.S Dollar  ||  10: British Pound  ||  11: Ten Year U.S T-Bonds  ||  12: Emerging Markets Mini Index  ||  13: Russell 2000 E-Mini"
print "14: S&P 500 Index\n"
Contract = int(raw_input("Enter Contract Number:"))

if (Contract == 1):
    SelectedContract = "CFTC/TIFF_CME_JY_ALL"
elif (Contract == 2):
    SelectedContract = "CFTC/TIFF_CME_RU_ALL"
elif (Contract == 3):
    SelectedContract = "CFTC/TIFF_CME_BR_ALL"
elif (Contract == 4):
    SelectedContract = "CFTC/TIFF_CBOE_VX_ALL"
elif (Contract == 5):
    SelectedContract = "CFTC/TIFF_CBOE_VX_ALL"
elif (Contract == 6):
    SelectedContract = "CFTC/TIFF_CME_CD_ALL"
elif (Contract == 7):
    SelectedContract = "CFTC/TIFF_CME_3E_ALL"
elif (Contract == 8):
    SelectedContract = "CFTC/TIFF_CME_AD_ALL"
elif (Contract == 9):
    SelectedContract = "CFTC/TIFF_ICE_DX_ALL"
elif (Contract == 10):
    SelectedContract = "CFTC/TIFF_CME_BP_ALL"
elif (Contract == 11):
    SelectedContract = "CFTC/TIFF_CBOT_TY_ALL"
elif (Contract == 12):
    SelectedContract = "CFTC/TIFF_LIFFE_MME_ALL"
elif (Contract == 13):
    SelectedContract = "CFTC/TIFF_ICE_G2_ALL"
elif (Contract == 14):
    SelectedContract = "CFTC/TIFF_CME_SP_ALL"
else:
    print "Error"

print "\n"

W =  quandl.get(SelectedContract, authtoken=Key)


W['OR'] = W['Open Interest']
W['DLong'] = W['Dealer Long Positions']
W['DShort'] = W['Dealer Short Positions']
W['DSpread'] = W['Dealer Spread Positions']
W['ALong'] = W['Asset Mgr LongPositions']
W['AShort'] = W['Asset Mgr Short Positions']
W['ASpread'] = W['Asset Mgr Spread Positions']
W['LLong'] = W['Lev Money Long Positions']
W['LShort'] = W['Lev Money Short Positions']
W['LSpread'] = W['Lev Money Spread Positions']
W['OLong'] = W['Other Reportable Long Positions']
W['OShort'] = W['Other Reportable Short Positions']
W['OSpread'] = W['Other Reportable Spread Positions']
W['NRLong'] = W['Non-Reportable Long Positions']
W['NRShort'] = W['Non-Reportable Reportable Positions']



def ReturnPercent(LongArray, ShortArray, Shift):
    RP =  float(LongArray[Shift] / (LongArray[Shift] + ShortArray[Shift]) * 100)
    return "{}%".format(int(round(RP)))

def ReturnChange(LongArray, ShortArray, Shift):
    CurrentValue = float(LongArray[0] / (LongArray[0] + ShortArray[0]) * 100)
    OldValue = float(LongArray[Shift] / (LongArray[Shift] + ShortArray[Shift]) * 100)
    Change = ((CurrentValue - OldValue) / OldValue) * 100
    return "{}%".format(int(round(Change)))

def ReturnSign(LongArray, ShortArray, Shift):
    if (LongArray[Shift] / (LongArray[Shift] + ShortArray[Shift]) * 100)  > (LongArray[Shift] / (LongArray[Shift] + ShortArray[Shift]) * 100):
        return "+"
    else:
        return ""

def ReturnAverage(LongArray, ShortArray):
    Length = len(LongArray)
    Array = [0] * Length
    for i in range(len(LongArray)):
        Array[i] = float(LongArray[i] / (LongArray[i] + ShortArray[i]) * 100)
    Result =  np.mean(Array)
    return "{}%".format(int(round(Result)))



def PrintSummary(Type, LongArray, ShortArray):
    return Type + " Long: " + ReturnPercent(LongArray, ShortArray, 0) + " ||  Previous Week: " + ReturnPercent(LongArray, ShortArray, 1) + " (" + ReturnSign(LongArray, ShortArray, 1) \
      + ReturnChange(LongArray, ShortArray, 1) +")" + " ||  Previous Month: " + ReturnPercent(LongArray, ShortArray, 3) + " (" + ReturnSign(LongArray, ShortArray, 3)\
      + ReturnChange(LongArray, ShortArray, 3) +")" + " || 3 Month: " + ReturnPercent(LongArray, ShortArray, 11) + " (" + ReturnSign(LongArray, ShortArray, 11)\
      + ReturnChange(LongArray, ShortArray, 11) +")" + " || Year: " + ReturnPercent(LongArray, ShortArray, 47) + " (" + ReturnSign(LongArray, ShortArray, 47) \
      + ReturnChange(LongArray, ShortArray, 47) + ")" + " || Running Average: " + ReturnAverage(LongArray, ShortArray)


#print "|| Date of Last Update:" + W.StoreDate[0] + "||"+'\n'

if (W.DLong[0] > 1000):
    print PrintSummary("Dealer", W.DLong, W.DShort) +'\n'
else:
    print "Error"
if (W.ALong[0] > 1000):
    print PrintSummary("Asset Manager", W.ALong, W.AShort)+'\n'
else:
    print "Error"
if (W.LLong[0] > 1000):
    print PrintSummary("Leveraged Money", W.LLong, W.LShort)+'\n'
else:
    print "Error"
if (W.OLong[0] > 1000):
    print PrintSummary("Other Reportable Positions", W.OLong, W.OShort)+'\n'
else:
    print "Error"
if (W.NRLong[0] > 1000):
    print PrintSummary("Non-Reportable Positions", W.NRLong, W.NRShort)+'\n'
else:
    print "Error"


