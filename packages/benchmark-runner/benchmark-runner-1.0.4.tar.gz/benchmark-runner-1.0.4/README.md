
[![Actions Status](https://github.com/redhat-performance/cloud-governance/workflows/CI/badge.svg)](https://github.com/redhat-performance/cloud-governance/actions)
[![Coverage Status](https://coveralls.io/repos/github/redhat-performance/cloud-governance/badge.svg?branch=master)](https://coveralls.io/github/redhat-performance/cloud-governance?branch=master)

<h3 align="right">![](media/op.png)

<h3 align="center">Benchmark-Runner ![](media/run.png) </h3>

This tool provides a lightweight and flexible framework for running benchmark workloads 
on Kubernetes/OpenShift Pod or VM.

This tool support the following workloads:

* [hammerdb](https://hammerdb.com/): running hammerdb workload on the following databases: MSSQL, Mariadb, Postgresql on Pod and VM with [Configuration](benchmark_runner/benchmark_operator/templates/hammerdb)
* [stressng](https://wiki.ubuntu.com/Kernel/Reference/stress-ng): running stressng workload on Pod or VM with [Configuration](benchmark_runner/benchmark_operator/templates/stressng)
* [uperf](http://uperf.org/): running uperf workload on Pod or VM with [Configuration](benchmark_runner/benchmark_operator/templates/uperf)

** First Phase: support [benchmark-operator workload](https://github.com/cloud-bulldozer/benchmark-operator)
 
![](media/kiban.png)

Reference:
* The benchmark-runner package is placed in [PyPi](https://pypi.org/project/cloud-governance/)
* The benchmark-runner container image is placed in [Quay.io](https://quay.io/repository/ebattat/cloud-governance)

![](media/docker1.png)

_**Table of Contents**_

<!-- TOC -->
- [Installation](#installation)
- [Run workload using Docker/Podman](#run-policy-using-docker-podman)
- [Run workload in Pod using Kubernetes/OpenShift](#run-policy-using-pod)
- [Post Installation](#post-installation)

<!-- /TOC -->

## Installation

#### Download benchmark-runner image from quay.io
```sh
podman pull quay.io/ebattat/benchmark-runner:latest
```

#### Environment variables description:

(mandatory)KUBECONFIG=$KUBECONFIG

(mandatory)KUBEADMIN_PASSWORD=$KUBEADMIN_PASSWORD

(mandatory)workload=$workload

Choose one from the following list:

`['stressng_pod', 'stressng_vm','uperf_pod', 'uperf_vm', 'hammerdb_pod_mariadb', 'hammerdb_pod_mssql', 'hammerdb_pod_postgres', 'hammerdb_vm_mariadb', 'hammerdb_vm_mssql', 'hammerdb_vm_postgres']`

(mandatory)elasticsearch=elasticsearch

(optional)pin_node1=pin_node1

(optional)pin_node2=pin_node2

## Run workload using Podman/Docker 
```sh
# workload=stressng_pod
sudo podman run --rm --name benchmark-runner -e KUBECONFIG=$KUBECONFIG -e KUBEADMIN_PASSWORD=$KUBEADMIN_PASSWORD -e workload=stressng_pod -e elasticsearch=elasticsearch -e pin_node1=pin_node1 -e log_level=INFO quay.io/ebattat/benchmark-runner:latest

# custom workload data configuration (path for custom workload data: -v /home/user/workload/workload_data.yaml:/benchmark_runner/benchmark_operator/template/workload/workload_data.yaml)
sudo podman run --rm --name benchmark-runner -e KUBECONFIG=$KUBECONFIG -e KUBEADMIN_PASSWORD=$KUBEADMIN_PASSWORD -e workload=stressng_pod -e elasticsearch=elasticsearch -e pin_node1=pin_node1 -e log_level=INFO -v /home/user/stressng/stressng_data.yaml:/benchmark_runner/benchmark_operator/template/stressng/stressng_data.yaml --privileged quay.io/ebattat/benchmark-runner:latest

```

## Run workload in Pod using Kubernetes/OpenShift]
[TBD]

## Post Installation

#### Delete benchmark-runner image
```sh
sudo podman rmi quay.io/ebattat/benchmark-runner:latest
```
