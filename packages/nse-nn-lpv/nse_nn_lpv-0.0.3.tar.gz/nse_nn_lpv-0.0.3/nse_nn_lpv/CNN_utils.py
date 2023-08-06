import numpy as np

import torch

import torch.nn as nn
import torch.nn.functional as tnf


def comptheshapes(inputdatashape, channellist,
                  stride=2, padding=0, dilation=1, kernelsize=5):
    """Compute the shapes of the data in the CNN a priori

    as with the formulas provided in the pytorch docs [1]_

    Parameters
    ----------
    x: tuple
        shape of the initial data point, i.e. (N_batch, C_in, H, W)

    References
    ----------

    ..[1] pytorch.org/docs/1.8.1/generated/torch.nn.Conv2d.html#torch.nn.Conv2d
    """

    layerss = [inputdatashape]
    Nbatch = inputdatashape[0]
    Hin = inputdatashape[2]
    Win = inputdatashape[3]
    for lcn in channellist[1:]:
        flhout = (Hin + 2*padding - dilation*(kernelsize-1) - 1)/stride + 1
        Hout = np.int(np.floor(flhout))
        flwout = (Win + 2*padding - dilation*(kernelsize-1) - 1)/stride + 1
        Wout = np.int(np.floor(flwout))
        layerss.append((Nbatch, lcn, Hout, Wout))
        Hin, Win = Hout, Wout

    return layerss


class DynamicConvAutoencoder(nn.Module):
    """ CNN encoder/decoder of variable sizes/channels

    Parameters:
    -----------

    sngl_lnr_lyr_dec : bool, optional
        whether the decoding is a single linear layer (without activation)
        defaults to `False`
    sll_code_size : int, optional
        size of the output layer in the `sngl_lnr_lyr_dec` case
    """
    def __init__(self, code_size, channellist=None, stride=None,
                 kernelsize=None, padding=None, cnnaeoutshape=None,
                 sngl_lnr_lyr_dec=False, sll_decode_size=None):
        # super(ConvAutoencoder, self).__init__()
        super().__init__()  # similar for Python 3
        self.code_size = code_size
        self.stride = stride
        self.ks = kernelsize
        self.channellist = channellist
        self.cnnparams = dict(kernel_size=self.ks, stride=self.stride,
                              padding=padding)
        nncnnaeout = cnnaeoutshape[1]*cnnaeoutshape[2]*cnnaeoutshape[3]
        self.cnnaeoutnn = nncnnaeout
        self.cnnaeoutheight = cnnaeoutshape[2]
        self.cnnaeoutwidth = cnnaeoutshape[3]

        # Encoder
        self.cvenclayers = []
        for layerid in range(len(channellist)-1):
            self.cvenclayers.append(nn.Conv2d(channellist[layerid],
                                              channellist[layerid+1],
                                              **self.cnnparams))
        self.fcenc = nn.Linear(self.cnnaeoutnn, self.code_size)

        # Decoder
        self.sngl_lnr_lyr_dec = sngl_lnr_lyr_dec
        if sngl_lnr_lyr_dec:
            self.sll_decode_size = sll_decode_size
            # a single linear layer for decoding
            self.decll = nn.Linear(self.code_size, self.sll_decode_size)
        else:
            self.fcdec = nn.Linear(self.code_size, self.cnnaeoutnn)
            self.cvdeclayers = []
            for layerid in reversed(range(len(channellist)-1)):
                self.cvdeclayers.\
                    append(nn.ConvTranspose2d(channellist[layerid+1],
                                              channellist[layerid],
                                              **self.cnnparams))

    def encode(self, x):
        Nbatch = x.size(0)
        for cvenclayer in self.cvenclayers:
            # print('enc-in: shape x:', x.shape)
            x = tnf.elu(cvenclayer(x))
            # print('enc-out: shape x:', x.shape)
        x = x.view([Nbatch, -1])  # vectorize per batch (=x.size(0))
        x = tnf.elu(self.fcenc(x))
        return x

    def decode(self, x):
        if self.sngl_lnr_lyr_dec:
            return self.decll(x)
        else:
            Nbatch = x.size(0)
            # print(x.shape)
            x = tnf.elu(self.fcdec(x))
            # print(x.shape)
            x = x.view([Nbatch, self.channellist[-1],
                        self.cnnaeoutheight, self.cnnaeoutwidth])
            # print(x.shape)
            # reshape to tensor (as it came out of the CNN part of the encoder)
            for cvdeclayer in self.cvdeclayers:
                # print('dec-in: shape x:', x.shape)
                x = tnf.elu(cvdeclayer(x))
                # print('dec-out: shape x:', x.shape)
            return x

    def forward(self, x):
        gofx = self.encode(x)
        invgofx = self.decode(gofx)
        return gofx, invgofx


class CNNllPODLoss(nn.Module):
    def __init__(self, mmatfac=None, podbas=None):
        super(CNNllPODLoss, self).__init__()
        ttcolidx = torch.from_numpy(mmatfac.indices)
        ttcrowidx = torch.from_numpy(mmatfac.indptr)
        ttdata = torch.from_numpy(mmatfac.data)
        ttmf = torch._sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
                                        size=mmatfac.shape, dtype=torch.double)
        self.mmatfac = ttmf
        self.podbas = podbas

    def forward(self, podcoeffs, cvvec):
        pcfs = podcoeffs.detach().numpy().reshape((-1, 1))
        lftpoddif = self.podbas @ pcfs - cvvec
        return (lftpoddif.T @ self.mmat @ lftpoddif).flatten()[0]


def get_podbas_mmat_mseloss(podbas, mmat=None, mmatf=None):
    ''' get a loss function that measures

    `|vk - V*rk|_M`

    where `V` is a (POD) basis for the state, `rk` is the encoded variable,
    and `M` is the mass matrix of the FEM discretization.
    '''

    if mmatf is not None or mmat is not None:
        raise UserWarning('CSR multiplication in pytorch somehow flawed')
        # ttcolidx = torch.from_numpy(mmatf.indices)
        # ttcrowidx = torch.from_numpy(mmatf.indptr)
        # ttdata = torch.from_numpy(mmatf.data)
        # ttmf = torch._sparse_csr_tensor(ttcrowidx, ttcolidx, ttdata,
        #                                 size=mmatf.shape, dtype=torch.float)
        # ttpodbas = torch.from_numpy(podbas)
        # ttpodbas = ttpodbas.float()
        # mfttpb = ttmf.matmul(ttpodbas)

    # mfttpb = mfttpb.float()
    ttpb = torch.from_numpy(podbas).float()
    xdim = podbas.shape[0]

    mselossfn = nn.MSELoss(reduction='sum')

    def podbas_mmat_mseloss(nnoutput, target):
        (bs, cs) = nnoutput.shape
        stackvecasmat = nnoutput.view((bs, cs)).T
        ttpbsvm = ttpb @ stackvecasmat
        return mselossfn(ttpbsvm.T.view((bs, xdim, 1)), target)

    return podbas_mmat_mseloss
