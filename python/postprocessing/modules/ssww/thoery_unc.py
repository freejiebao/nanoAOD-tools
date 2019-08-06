import ROOT
import SAMPLE

ROOT.ROOT.EnableImplicitMT()

def theory_unc(df):
    #df = ROOT.ROOT.RDataFrame("Events", files)
    df.Define('qcd_unc','float sum=0;for(int i=0, i < nLHEPdfWeight; i++){sum += LHEPdfWeight[i];};\
                         float mean=sum/nLHEPdfWeight;sum=0;for(int i=0, i < nLHEPdfWeight; i++){sum+=LHEPdfWeight[i]*LHEPdfWeight[i];};\
                         return sqrt((sum-nLHEPdfWeight*mean*mean)/(nLHEPdfWeight-1));')
    df.Define('scale_unc','float max=0,min=0,central=LHEScaleWeight[4];\
                           for(int i=0, i < nLHEScaleWeight; i++){\
                           if(i!=2 && i!=6){if(max<LHEScaleWeight[i]){max=LHEScaleWeight[i];};if(min>LHEScaleWeight[i]){min=LHEScaleWeight[i];};};};\
                           return max(abs(max-central),abs(min-central))/central;')
    return df