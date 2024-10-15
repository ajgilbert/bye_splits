import h5py
import pandas as pd
import uproot
import sys
events = "1000"

read = h5py.File("data/new_algos/cluster_valid_ThresholdDummyHistomaxnoareath20_SEL_all_REG_Si_SW_1_SK_default_CA_min_distance_NEV_{}.hdf5".format(events), mode='r')
print(read.keys())
keys = set([X.replace("_tclist", "") for X in read.keys()])

event_dict = {int(X.split("_")[1]) : X for X in keys}
print(event_dict)


tree = uproot.open("/data_CMS/cms/alves/L1HGCAL/photons_0PU_bc_stc_hadd.root:FloatingpointMixedbcstcrealsig4DummyHistomaxxydr015GenmatchGenclustersntuple/HGCalTriggerNtuple")
print(tree.keys())
sys.exit(0)
# print(tree_events[:10])

cl3d_energy_cmssw = []
cl3d_energy_bye = []

ntc_cmssw = []
ntc_bye = []

for batch in tree.iterate(step_size="20 MB", filter_name=["event", "cl3d_*", "tc_multicluster_id"]):
    arrs = batch
    for idx, evt in enumerate(arrs["event"]):
        if evt in event_dict.keys():
            print("Found event {}".format(evt))
            cmssw = arrs[idx]
            # print(cmssw.tolist())
            read = pd.read_hdf("data/new_algos/cluster_valid_ThresholdDummyHistomaxnoareath20_SEL_all_REG_Si_SW_1_SK_default_CA_min_distance_NEV_{}.hdf5".format(events), key=event_dict[evt])
            # print(read)
            readtc = pd.read_hdf("data/new_algos/cluster_valid_ThresholdDummyHistomaxnoareath20_SEL_all_REG_Si_SW_1_SK_default_CA_min_distance_NEV_{}.hdf5".format(events), key="{}_tclist".format(event_dict[evt]))
            # print(readtc)

            # Look for CMSSW clusters with +ve eta
            cl3d_eta = cmssw["cl3d_eta"]
            idxs_eta_p = [i for i in range(len(cl3d_eta)) if cl3d_eta[i] > 0]
            if len(idxs_eta_p) != 1:
                continue
            if read.shape[0] != 1:
                continue
            idx_eta_p = idxs_eta_p[0]
            id_sc = cmssw["cl3d_id"][idx_eta_p]
            ntc_cmssw.append(cmssw["tc_multicluster_id"].tolist().count(id_sc))
            ntc_bye.append(readtc.shape[0])
            # print(n_tc_cmssw, n_tc_bye)
            cl3d_energy_cmssw.append(cmssw["cl3d_energy"][idx_eta_p])
            cl3d_energy_bye.append(read.at[0, "en"])


# print(cl3d_energy_cmssw, cl3d_energy_bye)

import matplotlib.pyplot as plt
import numpy as np
# Calculate the difference between the two lists
energy_diff = [((bye - cmssw) / cmssw) for cmssw, bye in zip(cl3d_energy_cmssw, cl3d_energy_bye)]
countdiff = [((bye - cmssw)) for cmssw, bye in zip(ntc_cmssw, ntc_bye)]


# Create a histogram of the differences
plt.figure()
plt.hist(energy_diff, bins=50, alpha=0.75, edgecolor='black')
plt.xlabel('Energy (Bye-CMSSW)/CMSSW')
plt.ylabel('Events')
plt.savefig('diff_energy.png')
plt.savefig('diff_energy.pdf')

plt.figure()
plt.hist(countdiff, bins=50, alpha=0.75, edgecolor='black')
plt.xlabel('nTCs (Bye-CMSSW)')
plt.ylabel('Events')
plt.savefig('diff_ntc.png')
plt.savefig('diff_ntc.pdf')

energy_diff_eq_tc = np.array(energy_diff)[np.array(countdiff) == 0]
plt.figure()
plt.hist(energy_diff_eq_tc, bins=50, alpha=0.75, edgecolor='black')
plt.xlabel('Energy (Bye-CMSSW)/CMSSW')
plt.ylabel('Events')
plt.savefig('diff_energy_eq_tc.png')
plt.savefig('diff_energy_eq_tc.pdf')
# Show the plot (optional)
# plt.show()
        #     tree_events = tree.arrays(cut="event=={}".format(evt))
        #     print(tree_events)

# for evt in list(sorted(event_dict.keys()))[:1]:


# ThresholdDummyHistomaxnoareath20_171602_ev_tclist

"""
branch: tc_n                    468934

branch: tc_id                1266636926

branch: tc_subdet             94377607

branch: tc_zside             158635478

branch: tc_layer             360836598

branch: tc_waferu            383646413

branch: tc_waferv            382891805

branch: tc_wafertype         122853939

branch: tc_cellu             312014730

branch: tc_cellv             312443375

branch: tc_data              136029999

branch: tc_uncompressedCharge 328628834

branch: tc_compressedCharge  182440417

branch: tc_pt                1381293215

branch: tc_mipPt             1345637499

branch: tc_energy            427418047

branch: tc_eta               1373037986

branch: tc_phi               1298364631

branch: tc_x                 832929081

branch: tc_y                 887988672

branch: tc_z                 458429389

branch: tc_cluster_id         91513843

branch: tc_multicluster_id    39117017

branch: tc_multicluster_pt    39509070
    """