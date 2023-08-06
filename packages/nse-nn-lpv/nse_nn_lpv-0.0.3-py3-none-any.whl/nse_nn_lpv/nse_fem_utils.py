import numpy as np

import dolfin

import dolfin_navier_scipy.dolfin_to_sparrays as dts
import dolfin_navier_scipy.problem_setups as dnsps


def get_fem_utils(meshfile=None, physregs=None, geodata=None,
                  scheme=None, Re=1., vtdc_dict=None):
    femp, stokesmatsc, rhsd = \
        dnsps.get_sysmats(problem='gen_bccont', Re=Re, bccontrol=False,
                          scheme=scheme, mergerhs=True,
                          meshparams=dict(strtomeshfile=meshfile,
                                          strtophysicalregions=physregs,
                                          strtobcsobs=geodata))
    mmat = stokesmatsc['M']

    def convfun(vvec, dirizero=False):
        dbcvals = [0]*len(femp['dbcinds']) if dirizero else femp['dbcvals']
        nvv = dts.get_convvec(u0_vec=vvec, V=femp['V'],  # femp=femp,
                              invinds=femp['invinds'],
                              dbcinds=femp['dbcinds'], dbcvals=dbcvals)
        return nvv

    def getconvmat(vvec, dirizero=False):
        dbcvals = [0]*len(femp['dbcinds']) if dirizero else femp['dbcvals']
        cvm, _, _ = dts.\
            get_convmats(u0_vec=vvec, V=femp['V'], invinds=femp['invinds'],
                         dbcinds=femp['dbcinds'], dbcvals=dbcvals)
        cvmc, _ = dts.condense_velmatsbybcs(cvm,  invinds=femp['invinds'],
                                            dbcinds=femp['dbcinds'],
                                            dbcvals=dbcvals)
        return cvmc

    if vtdc_dict is not None:
        xlims = [vtdc_dict['xmin'], vtdc_dict['xmax']]
        ylims = [vtdc_dict['ymin'], vtdc_dict['ymax']]

        # TODO: boundary conditions

        def vtdc(vvec):
            return vvec_to_datachannels(vvec, xlims=xlims, ylims=ylims,
                                        xmshpoints=vtdc_dict['xmshpoints'],
                                        ymshpoints=vtdc_dict['ymshpoints'],
                                        V=femp['V'])
    else:
        vtdc = None

    return mmat, convfun, getconvmat, vtdc, femp['invinds']


def vvec_to_datachannels(vvec, xlims=[-1, 1], ylims=[-1, 1],
                         xmshpoints=None, ymshpoints=None, V=None):

    curvfun = dts.expand_vp_dolfunc(V=V, vc=vvec)[0]
    xmsh = np.linspace(xlims[0], xlims[1], num=xmshpoints)
    ymsh = np.linspace(ylims[0], ylims[1], num=ymshpoints)

    xdatlist = []
    ydatlist = []
    for cxp in xmsh:
        xcdl = []
        ycdl = []
        for cyp in ymsh:
            cpp = dolfin.Point(cxp, cyp)
            try:
                cvval = curvfun(cpp)
            except RuntimeError:
                cvval = [0, 0]
            xcdl.append(cvval[0])
            ycdl.append(cvval[1])
        xdatlist.append(xcdl)
        ydatlist.append(ycdl)
    xdata = np.array(xdatlist)
    ydata = np.array(ydatlist)

    return xdata, ydata
