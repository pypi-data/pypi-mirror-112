# GCP
Main source material:
https://github.com/GoogleCloudPlatform/deploymentmanager-samples/tree/master/examples/v2/htcondor
https://cloud.google.com/solutions/analyzing-portfolio-risk-using-htcondor-and-compute-engine
While the tutorial is inspired by the github repo,
one difference between the two is that the tutorial creates custom images,
including an installation of HTCondor.
This is necessary when you're gonna have many nodes,
in which case you won't give them internet access.
So the following follows the tutorial more than the github repo.

# Notable Changes Made:
- Tutorial bug was resolved by waiting for internet in startup scripts:
  sh``
  while ! ping -c1 google.com >/dev/null; do sleep 1 ; done
  ``
- I use `Ubuntu` 2020 Focal Fossa, rather than `Debian-9-stretch,`
  which allows installing htcondor from
  [Ubuntu's standard software repositories](https://launchpad.net/ubuntu/+source/condor),
  rather than following the installation at
  https://research.cs.wisc.edu/htcondor/debian/
  which is what the GCP tutorial/github-repo do.
  Thus, my condor is newer (8.6 rather than 8.4),
  which means `condor_submit` and `condor_q` allows option ``-batch-name``.
- Anaconda and DAPPER's requirements have been installed on the compute-node images.
  DAPPER is updated every time experiments are run on GCP,
  but the python libraries in Anaconda are not.
  For example, dill may have been updated on your local computer,
  which could result in the dill version on GCP not knowing how to
  unpack the experiment data you upload to it.
  Dill also requires that the python version (3.8, 3.7, etc) is the same.

# Quotas:

Description:
I wish to increase the computing power of my cluster, which is used for HTC in
science. This has been agreed beforehand with my Google Cloud account manager,
eloven@google.com.

Last time around, I just went to the quotas panel,
and selected the quotas that were running close to capacity
(my cluster was already operating at full capacity).
This meant:
+----------------+-------------+-----------------+
|      Name      |    Region   | Requested Limit |
+----------------+-------------+-----------------+
|      CPUS      | us-central1 |      10000      |
| DISKS_TOTAL_GB | us-central1 |      40000      | ie 40 TB
|    NETWORKS    |    GLOBAL   |       100       |
|  SUBNETWORKS   |    GLOBAL   |       996       |
+----------------+-------------+-----------------+

The previous time around I requested:
+----------------+------------------+----------+--------+-------------+
|    Request     | CPUS_ALL_REGIONS | NETWORKS | ROUTES | SUBNETWORKS |
+----------------+------------------+----------+--------+-------------+
| Region: GLOBAL |       1000       |    10    |  500   |     500     |
+----------------+------------------+----------+--------+-------------+
+---------------------+------+
|       Request       | CPUS |
+---------------------+------+
| Region: us-central1 | 1000 |
+---------------------+------+

In general, these are the options I imagine are relevant:
Regions: us-central1-f AND global
CPUs (preemptible?)
Persistent disk standard, SSD, preemptible?
subnetworks
networks
firewall rules


# Reasons why GCP isn't n-nodes x-faster than my workstation:
- Its processors (Xenon) are almost 2x slower
- Communication, and loading DAPPER
- Not the case: Truth simulations are not re-run for local runs.
- Not the case: np itself uses mp.



# ssh to compute-nodes
Even though the compute nodes are configured without internet access, 
`gcloud` is still smart enough to ssh into them (using `IAP tunneling`). 
As far as I know, I've done nothing special to enable this. 
Use (run on my local desktop) for ex:
`gcloud compute ssh condor-compute-pvm-instance-02x5`

# Using standard ssh
This can be enabled with `gcloud compute config-ssh`, which edits a blob in `~/.ssh/config`
Run it "routinely" to update the list.
Another option is to manually look up and use the public IP addresses.

# Creating the condor-submit image:
**NB:** condor-submit.sh startup script must be adapted to OS

    curl https://bootstrap.pypa.io/get-pip.py | python3 # for Ubuntu
    curl https://bootstrap.pypa.io/get-pip.py | python # for Debian

In addition, the autoscaler script must be adapted to python3 for Ubuntu.


# Creating the condor-compute image:
Follow this recipe
https://cloud.google.com/solutions/analyzing-portfolio-risk-using-htcondor-and-compute-engine#creating_an_htcondor_cluster_by_using_cloud_deployment_manager_templates
but before stopping the instance and creating the image, do:

- Install dotfiles?

- Install anaconda for all users in `/opt` (as `root`).
  (following https://docs.anaconda.com/anaconda/install/multi-user/ ):
  - `wget` one of the links from https://repo.anaconda.com/archive/
  - Launch installer w/ `sudo bash Anaconda3...sh`
  - Choose to install in `/opt/anaconda`
  - Choose not to initialize Anaconda
  - Create group `sudo groupadd mygroup` (use `group add` on Debian)
  - **NB copy-paste one line at a time!**
    It seems the permissions etc are a bit slow to update!
  - Add group `mygroup` for anaconda:
    sh``
    sudo chown -R root:mygroup /opt/anaconda
    sudo chmod 770 -R /opt/anaconda
    ``
  - Add `nobody` and `pnr` to `mygroup.`
    sh``
    sudo adduser nobody mygroup
    sudo adduser nobody pnr
    ``
  - Also, put this activation in the `run_job.sh` scripts:
    sh``
    __conda_setup=$(/opt/anaconda/bin/conda shell.bash hook)
    eval "$__conda_setup"
    conda activate base
    ``
    Ensure the right env name is used to by conda in `run_job.sh`.
- Install DAPPER requirements (`setup.py`) while you have internet:
  - Activate conda env. NB: make sure the python version agrees with setup.py:python_requires.
  - As your ssh login (`pnr`), clone DAPPER, `g co dev1`, and do `pip install -e .`
  - Test installation: python `example_1.py`
  - Then `pip uninstall DA-DAPPER` to avoid conflicts with job-time DAPPER installs.
- Redo `chown`ing following the above `pip`ing:
  sh``
  sudo chown -R root:mygroup /opt/anaconda
  sudo chmod 770 -R /opt/anaconda
  ``
- Ensure this has worked by inspecting:
  sh``
  ls -l /opt/anaconda/lib/python3.8/site-packages/easy*
  ls -l /opt/anaconda/lib/python3.8/site-packages/tabulate*
  ``

After you've created the new compute image,
make sure to insert its name in `condor-cluster.yaml`.


# (Re-)creating the cluster

#### Update submit-image:
```sh
gcloud deployment-manager deployments stop htcluster102
gcloud compute images create condor-submit-v[INSERT_DATE] --source-disk condor-submit --source-disk-zone us-central1-f --family htcondor-ubuntu
```
Update submitimage field in
`~/P/DAPPER/dapper/tools/remote/deployment/condor-cluster.yaml`

#### Delete deployment
```sh
gcloud deployment-manager deployments delete htcluster102
```

#### Create deployment
```sh
gcloud deployment-manager deployments create htcluster102 --config ~/P/DAPPER/dapper/tools/remote/deployment/condor-cluster.yaml
```

Update `autoscaler.py`, and send it with
```sh
gcloud compute scp ~/P/DAPPER/dapper/tools/remote/autoscaler.py pnr@condor-submit:~/
```
**NB**: Immediately (so you don't forget) set-up autoscaler cron job,
**as described in autoscaler.py**.
This should also be in effect for other users of htcondor.



One issue that has occured is that condor-submit didnt get an external IP,
so that ssh didnt work. The IP should be listed doing this:
`gcloud compute instances list`
In that case it sufficed to delete and re- create the deployment.

To enable
Run
`gcloud compute ssh condor-submit`
`gcloud compute config-ssh`
Now try normal `ssh`. It might complain that the authenticity
of host `<IP>` can't be established. I believe that's because
of an outdated identification or something
(from previous versions of the cluster) in ~/.ssh/known_hosts,
which the error message should indicate (with linenumber).
Just delete this line and try again.

Note: For uplink.py to work, you
also need to update to latest rsync,
and make sure that your .ssh/config enables
login without typing passphrase even once.


## Other useful commands

```sh
gcloud compute instances list | wc -l
gcloud compute instance-groups managed list-instances condor-compute-pvm-igm
gcloud compute instance-groups managed describe condor-compute-pvm-igm --zone us-central1-f
gcloud compute instance-groups managed resize condor-compute-pvm-igm --zone=us-central1-f --size 100
```


## Logs on condor-submit

```sh
grep CRON /var/log/syslog | tail
cat autoscaler.log 
du -hs xp # When this is >0, then the job is done
```









# Old stuff

## Transfering DAPPER
I used to copy DAPPER and xp.com to each rundir/initialdir of the submission:
python``
remote_cmd(f"""cd {xps_path.name}; for ixp in ixp_*; do cp -r ~/DAPPER $ixp/; done""")
remote_cmd(f"""cd {xps_path.name}; for ixp in ixp_*; do cp xp.com $ixp/; done""")
``
But then I figured out you can use relative paths in transfer_input_files of the submission-description.


## gsutil
Another way to communicate updated common data to the compute nodes
is to use cloud storage (gsutil).
python``
xcldd=".git|scripts|docs|.*__pycache__.*|.pytest_cache|DA_DAPPER.egg-info|old_version.zip" 
cmd(f"gsutil -m rsync -r -d -x {xcldd} {dirs['DAPPER']} gs://pb2/DAPPER")
``
With this in run_job.sh to pull into compute-nodes:
sh``
mkdir $HOME/DAPPER
CLOUDSDK_PYTHON=/usr/bin/python gsutil -m rsync -d -r gs://pb2/DAPPER DAPPER
``
Drawbacks:
- gsutil requires user to have access to gs bucket.
- gsutil rsync doesnt have --include or --files-from option.


## Dotfiles installation via startup-script.
Startup-script runs as sudo, but need to install for your user.
[insipration](https://stackoverflow.com/q/43900350)

    sudo useradd -m pnr
    sudo -u pnr bash -c 'git clone --bare https://github.com/patricknraanes/dotfiles.git $HOME/.cfg'
    _HOME=$(su - pnr -c 'echo $HOME')
    cd $_HOME
    gitopt="--git-dir=$_HOME/.cfg/ --work-tree=$_HOME"
    sudo -u pnr bash -c "git $gitopt config --local status.showUntrackedFiles no"
    sudo -u pnr bash -c "git $gitopt checkout --force condor-submit"
    sudo -u pnr bash -c "git $gitopt submodule update --init"
