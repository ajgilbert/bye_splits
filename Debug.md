Produce events:

`python3 bye_splits/production/produce.py --nevents -1 --particles photons`

Produces `skim_photons_default.root` with 29571 entries.

`python3 bye_splits/scripts/run_default_chain.py --nevents 1000`

Note the code can crash:

```
Traceback (most recent call last):
  File "/grid_mnt/data__data.polcms/cms/gilbert/hgcal-tpg/CMSSW_13_2_6/src/bye_splits/bye_splits/scripts/run_default_chain.py", line 87, in <module>
    run_default_chain(common.dot_dict(vars(FLAGS)), user=FLAGS.user)
  File "/grid_mnt/data__data.polcms/cms/gilbert/hgcal-tpg/CMSSW_13_2_6/src/bye_splits/bye_splits/scripts/run_default_chain.py", line 64, in run_default_chain
    stats_out = collector.collect_cluster(pars, chain_mode='default', **valid_d)
  File "/grid_mnt/data__data.polcms/cms/gilbert/hgcal-tpg/CMSSW_13_2_6/src/bye_splits/bye_splits/tasks/validation.py", line 230, in collect_cluster
    assert len(kall) == len(kcl)
AssertionError
```

`python3 study_cmssw_bye_differences.py`