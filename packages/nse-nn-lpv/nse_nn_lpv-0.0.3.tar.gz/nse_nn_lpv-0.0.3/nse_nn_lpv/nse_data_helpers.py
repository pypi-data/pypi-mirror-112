import numpy as np
import matplotlib.pyplot as plt
import json

import torch
from torch.utils.data import Dataset

from scipy.io import savemat


class NSEDataset(Dataset):
    def __init__(self, dtchnnll, vvecl, meanv=0., invinds=None, mmatfac=None):
        self.dtchnnll = dtchnnll
        self.vvecl = vvecl
        self.meanv = meanv
        self.invinds = invinds

        if mmatfac is None:
            self.mmatfac = None
        else:
            ttcolidx = torch.from_numpy(mmatfac.indices)
            ttcrowidx = torch.from_numpy(mmatfac.indptr)
            ttdata = torch.from_numpy(mmatfac.data)
            ttmf = torch.\
                _sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
                                   size=mmatfac.shape, dtype=torch.float)
            self.mmatfac = ttmf

    def __len__(self):
        try:
            return len(self.vvecl)
        except TypeError:
            return len(self.dtchnnll)

    def __getitem__(self, idx):
        vimgdt = convert_torchtens(self.dtchnnll[idx])
        if self.vvecl is None:
            return vimgdt
        else:
            if self.invinds is not None:
                vvec = torch.from_numpy(self.vvecl[idx][self.invinds]
                                        - self.meanv).float()
            else:
                vvec = torch.from_numpy(self.vvecl[idx] - self.meanv).float()
            if self.mmatfac is not None:
                vvec = self.mmatfac @ vvec
            return vimgdt, vvec


def get_check_podprjerror(mmat=None, myfac=None, prjvecs=None, podvecs=None,
                          meanv=0.):
    # fiprjvecs = myfac.solve_F(prjvecs)
    # if not meanv == 0.:
    #     ftmeanv = myfac.Ft @ meanv
    # else:
    #     ftmeanv = 0.
    def check_pod_prjerror(tstvec, poddim=None, ret_rho=False):
        tstvecnp = myfac.solve_Ft(tstvec.view((-1, 1)).numpy())
        # the tstvecs have been multiplied by Ft in the NSEDataSet
        crho = prjvecs[:, :poddim].T @ (tstvecnp - meanv)
        prjlftv = podvecs[:, :poddim] @ crho
        pdiff = tstvecnp - prjlftv - meanv
        perr = (pdiff.T @ mmat @ pdiff).flatten()[0]
        if ret_rho:
            return perr, crho
        return perr

    return check_pod_prjerror


def batch_avrg_poderr(xbatch, poddim=None, cpe_fn=None):
    accupe = 0
    for x in xbatch:
        accupe += cpe_fn(x, poddim=poddim)
    return accupe/xbatch.shape[0]


def convert_torchtens(nsedatapt):
    velptx = nsedatapt[0]
    velpty = nsedatapt[1]
    velptxy = np.stack([velptx, velpty])
    tstset = (torch.from_numpy(velptxy)).float()
    # tstshp = tstset.shape
    # ttstset = tstset.reshape((1, tstshp[0], tstshp[1], tstshp[2]))
    return tstset


def get_nse_img_data(strtodata, plotplease=False, single_save=False,
                     return_vvecs=False,
                     return_fem_info=False):
    with open(strtodata) as jsf:
        datadict = json.load(jsf)

    gddct = datadict['geometry']
    xmin, xmax = gddct['xmin'], gddct['xmax'],
    ymin, ymax = gddct['ymin'], gddct['ymax']

    if single_save:
        ckey = list(datadict)[-2]  # the last key is the 'geodata'
        print('saved the data for key={0} ...'.format(ckey))
        cxdatamat = np.array(datadict[ckey]['vmatx'])
        cydatamat = np.array(datadict[ckey]['vmaty'])
        savemat('./data/veldata.mat', {"vxmat": cxdatamat, "vymat": cydatamat})
        print('... to ./data/veldata.mat')
        return

    datal = []
    vvcsl = []
    figidx = 0
    for ckey in datadict.keys():
        try:
            # the solution has two components: x and y
            cxdatamat = np.array(datadict[ckey]['vmatx'])
            cydatamat = np.array(datadict[ckey]['vmaty'])
            datal.append((cxdatamat, cydatamat, '{0}'.format(ckey)))
            # the solution as *the real* data vector
            # vvec = np.array(datadict[ckey]['vvec'])
            if plotplease:
                plt.figure(100+figidx)
                plt.imshow(cxdatamat,
                           extent=[xmin, xmax, ymin, ymax],
                           cmap=plt.get_cmap('gist_earth'))
                plt.figure(200+figidx)
                plt.imshow(cydatamat,
                           extent=[xmin, xmax, ymin, ymax],
                           cmap=plt.get_cmap('gist_earth'))
                figidx += 1
            if return_vvecs:
                vvcsl.append(np.array(datadict[ckey]['vvec']).reshape((-1, 1)))
        except (TypeError, KeyError) as e:
            print(e, 'Nondata key:', ckey)
            pass
        plt.show()

    rttpl = (datal, vvcsl) if return_vvecs else datal

    if return_fem_info:
        femdata = dict(velstrs=datadict['velstrs'],
                       meshfile=datadict['meshfile'],
                       physregs=datadict['physregs'],
                       geodata=datadict['geodata'],
                       femscheme=datadict['femscheme'],
                       geometry=gddct)
        return rttpl, femdata
    else:
        return rttpl


if __name__ == '__main__':
    strtodata = '../simulations-training-data/train-data/firsttry.json'
    get_nse_img_data(strtodata, plotplease=False, single_save=True)
