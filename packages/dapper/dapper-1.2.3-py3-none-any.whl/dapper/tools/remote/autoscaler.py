#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This script is used to resize a managed instance group (MIG) cluster
based on the number of jobs in the HTCondor queue.

The script comes from a Google Cloud Platform (GCP) tutorial,
and has only been slightly modified since.

gcloud compute scp autoscaler.py condor-submit:~/
gcloud compute ssh condor-submit
chmod u+x autoscaler.py
crontab -e # and then add:
sh``
*/2 * * * *  /usr/bin/python3 /home/pnr/autoscaler.py -p mc-tut -z us-central1-f -g condor-compute-pvm-igm -v 1 >> /home/pnr/autoscaler.log 2>&1
``
"""

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pprint import pprint
try:
    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials
except ImportError:
    from sys import exit; exit()

import os
import math
import argparse


####################
#  Args, defaults  #
####################

parser = argparse.ArgumentParser("autoscaler.py")
parser.add_argument("-p" , "--project_id"           , help="Project id"                                                                   , type=str)
parser.add_argument("-r" , "--region"               , help="GCP region where the managed instance group is located"                       , type=str)
parser.add_argument("-z" , "--zone"                 , help="Name of GCP zone where the managed instance group is located"                 , type=str)
parser.add_argument("-g" , "--group_manager"        , help="Name of the managed instance group"                                           , type=str)
parser.add_argument("-c" , "--computeinstancelimit" , help="Maximum number of compute instances"                                          , type=int)
parser.add_argument("-v" , "--verbosity"            , help="Increase output verbosity. 1-show basic debug info. 2-show detail debug info" , type=int  , choices=[0 , 1 , 2])
args = parser.parse_args()

# Project ID
project = args.project_id  # Ex:'slurm-var-demo'

# Region where the managed instance group is located
region = args.region  # Ex: 'us-central1'

# Name of the zone where the managed instance group is located
zone = args.zone  # Ex: 'us-central1-f'

# The name of the managed instance group.
instance_group_manager = args.group_manager  # Ex: 'condor-compute-igm'

# Default number of cores per intance, will be replaced with actual value
cores_per_node = 4

# Dont create more cores than: nJobs * min_jobs_per_core
# NB: bad idea -- see Zeno's paradox about the tortoise and Achilles.
# min_jobs_per_core = 3

# Default number of running instances that the managed instance group should maintain at any given time.
# This number will go up and down based on the load (number of jobs in the queue)
size = 0

# Debug level: 1-print debug information, 2 - print detail debug information
debug = 0
if (args.verbosity):
    debug = args.verbosity

# Timestamp to enable probing if script is being run as cron job.
print('') # new line
from datetime import datetime
now = datetime.now()
timestamp = now.strftime("%Y / %m / %d - %H:%M:%S")
print(timestamp)


# Limit for the maximum number of compute instance.
# If zero (default setting), no limit will be enforced by the  script 
compute_instance_limit = 0
if (args.computeinstancelimit):
    compute_instance_limit = abs(args.computeinstancelimit)


if debug > 0:
    print('autoscaler.py launched with the following arguments:')
    print('    project_id:'           , project)
    print('    region:'               , region)
    print('    zone:'                 , zone)
    print('    group_manager:'        , instance_group_manager)
    print('    computeinstancelimit:' , str(compute_instance_limit))
    print('    debuglevel:'           , str(debug))



############################
#  Misc API functionality  #
############################

# Obtain credentials
credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)

# Remove specified instance from MIG and decrease MIG size
def deleteFromMig(instance):
    instanceUrl = 'https://www.googleapis.com/compute/v1/projects/' \
        + project + '/zones/' + zone + '/instances/' + instance
    instances_to_delete = {'instances': [instanceUrl]}

    requestDelInstance = \
        service.instanceGroupManagers().deleteInstances(project=project,
            zone=zone, instanceGroupManager=instance_group_manager,
            body=instances_to_delete)
    response = requestDelInstance.execute()
    if debug > 1:
        print('Request to delete instance ' + instance)
        pprint(response)

    return response

def getInstanceTemplateInfo():
    requestTemplateName = \
        service.instanceGroupManagers().get(project=project, zone=zone,
            instanceGroupManager=instance_group_manager,
            field23s='instanceTemplate')
    responseTemplateName = requestTemplateName.execute()
    template_name = ''

    if debug > 1:
        print('Request for the template name')
        pprint(responseTemplateName)

    if len(responseTemplateName) > 0:
        template_url = responseTemplateName.get('instanceTemplate')
        template_url_partitioned = template_url.split('/')
        template_name = \
            template_url_partitioned[len(template_url_partitioned) - 1]

    requestInstanceTemplate = \
        service.instanceTemplates().get(project=project,
            instanceTemplate=template_name, field23s='properties')
    responseInstanceTemplateInfo = requestInstanceTemplate.execute()

    if debug > 1:
        print('Template information')
        pprint(responseInstanceTemplateInfo['properties'])

    machine_type = responseInstanceTemplateInfo['properties']['machineType']
    is_preemtible = responseInstanceTemplateInfo['properties']['scheduling']['preemptible']
    if debug > 0:
        print('Machine Type: ' + machine_type)
        print('Is preemtible: ' + str(is_preemtible))
    request = service.machineTypes().get(project=project, zone=zone,
            machineType=machine_type)
    response = request.execute()
    guest_cpus = response['guestCpus']
    if debug > 1:
        print('Machine information')
        pprint(responseInstanceTemplateInfo['properties'])
    if debug > 0:
        print('Guest CPUs: ' + str(guest_cpus))

    instanceTemlateInfo = {'machine_type': machine_type,
                           'is_preemtible': is_preemtible,
                           'guest_cpus': guest_cpus}
    return instanceTemlateInfo


###################
#  Instance info  #
###################

instanceTemlateInfo = getInstanceTemplateInfo()
if debug > 0:
    print('Information about the compute instance template')
    pprint(instanceTemlateInfo)

cores_per_node = instanceTemlateInfo['guest_cpus']
print('Number of CPU per compute node: ' + str(cores_per_node))


##############
#  MIG info  #
##############

requestGroupInfo = service.instanceGroupManagers().get(project=project,
        zone=zone, instanceGroupManager=instance_group_manager)
responseGroupInfo = requestGroupInfo.execute()

MIG_maxSurge = responseGroupInfo["updatePolicy"]["maxSurge"]["calculated"]
if compute_instance_limit==0:
    compute_instance_limit = MIG_maxSurge

currentTarget = int(responseGroupInfo['targetSize'])
print('Current MIG target size: ' + str(currentTarget))

if debug > 1:
    print('MIG Information:')
    print(responseGroupInfo)


##############
#  Job info  #
##############

# in the queue that includes number of jos waiting as well as number of jobs already assigned to nodes
# queue_length_req = 'condor_q -totals -format "%d " Jobs -format "%d " Idle -format "%d " Held'
queue_length_req = 'condor_q -totals'
queue_length_resp = os.popen(queue_length_req).read().split()
# Parse output
if len(queue_length_resp) > 1:
    inds = {k[:-1]: queue_length_resp.index(k)-1 for k in ["jobs;","idle,","held,"]}

    queue        = int(queue_length_resp[inds["jobs"]])
    idle_jobs    = int(queue_length_resp[inds["idle"]])
    on_hold_jobs = int(queue_length_resp[inds["held"]])
else:
    queue        = 0
    idle_jobs    = 0
    on_hold_jobs = 0

print('Total queue length: ' + str(queue))
print('Idle jobs: '          + str(idle_jobs))
print('Jobs on hold: '       + str(on_hold_jobs))

# Get state for for all jobs in Condor
name_req = 'condor_status  -af name state'
slot_names = os.popen(name_req).read().splitlines()
if debug > 1:
    print('Currently running jobs in Condor')
    print(slot_names)

# Adjust current queue length by the number of jos that are on-hold
queue -=on_hold_jobs
if on_hold_jobs>0:
    print("Adjusted queue length: " + str(queue) )


###########################################
#  Calculate instance numbers (MIG size)  #
###########################################

# Calculate max number of instances necessary for current job queue length
if queue > 0:
    size = int(math.ceil(float(queue) / float(cores_per_node)))
    if debug>0:
        print("=> Max. required MIG size (num. of instances): %d/%d = %d"
              %(queue, cores_per_node, size))
else:
    size = 0

# Limit/bound instance numbers
if size > compute_instance_limit:
    size = compute_instance_limit;
    print("But MIG size is limited at " + str(compute_instance_limit))


print('=> New MIG target size: ' + str(size))


#################
#  Adjustments  #
#################

if size == 0 and currentTarget == 0:
    print('No jobs in the queue and no compute instances running. Nothing to do')
    exit()

if size == currentTarget:
    print('Running correct number of compute nodes to handle number of jobs in the queue')
    exit()

if size < currentTarget:

    # TODO
    # Allow manual rescaling to 2 to stick.
    # if currentTarget<=2:
        # print("Machines are idle, but there's so few, so we wont downscale.")                                          
        # import sys
        # sys.exit(0)

    print('Scaling down. Looking for nodes that are not busy and so can be shut down' )
    # Find nodes that are not busy (all slots showing status as "Unclaimed")

    node_busy = {}
    for slot_name in slot_names:
        name_status = slot_name.split()
        if len(name_status) > 1:
            name = name_status[0]
            status = name_status[1]
            slot = "NO-SLOT"
            slot_server = name.split('@')
            if len(slot_server) > 1:
                slot = slot_server[0]
                server = slot_server[1].split('.')[0]
            else:
                server = slot_server[0].split('.')[0]

            if debug > 1:
                print(slot + ', ' + server + ', ' + status + '\n')

            if server not in node_busy:
                if status == 'Unclaimed':
                    node_busy[server] = False
                else:
                    node_busy[server] = True
            else:
                if status != 'Unclaimed':
                    node_busy[server] = True
                    
    if debug > 1:
        print('Compuute node busy status:')
        print(node_busy)

    # Shut down nodes that are not busy
    for node in node_busy:
        if not node_busy[node]:
            print('Will shut down: ' + node + ' ...')
            respDel = deleteFromMig(node)
            if debug > 1:
                print("Shut down request for compute node " + node)
                pprint(respDel)
                
    if debug > 1:
        print("Scaling down complete")

if size > currentTarget:
    print("Scaling up. Need to increase number of instances to " + str(size))
    #Request to resize
    request = service.instanceGroupManagers().resize(project=project,
            zone=zone, 
            instanceGroupManager=instance_group_manager,
            size=size)
    response = request.execute()
    if debug > 1:
        print('Requesting to increase MIG size')
        pprint(response)
        print("Scaling up complete")
