
import os

# when adding new environment variables update environment_variables_dict
environment_variables_dict = {}

workloads_list = ['hammerdb_pod_mariadb', 'hammerdb_pod_mssql', 'hammerdb_pod_postgres',
                  'hammerdb_vm_mariadb', 'hammerdb_vm_mssql', 'hammerdb_vm_postgres',
                  'stressng_pod', 'stressng_vm',
                  'uperf_pod', 'uperf_vm']

# os.environ['KUBECONFIG'] = ''
environment_variables_dict['KUBECONFIG'] = os.environ.get('KUBECONFIG', '')

# os.environ['KUBEADMIN_PASSWORD'] = ''
environment_variables_dict['KUBEADMIN_PASSWORD'] = os.environ.get('KUBEADMIN_PASSWORD', '')

# workload
# os.environ['workload'] = ''
environment_variables_dict['workload'] = os.environ.get('workload', '')

# elasticsearch
# os.environ['elasticsearch'] = ''
environment_variables_dict['elasticsearch'] = os.environ.get('elasticsearch', '')

# node selectors
# os.environ['pin_node1'] = ''
environment_variables_dict['pin_node1'] = os.environ.get('pin_node1', '')
# uperf server node
# os.environ['pin_node2'] = ''
environment_variables_dict['pin_node2'] = os.environ.get('pin_node2', '')
