## Run Prometheus with Docker

```bash
# create volume for Prometheus data
$ docker volume create prometheus_data

# launch container
$ docker run \
    -p 9090:9090 \
    -v $PROM_CONFIG_LOCATION:/etc/prometheus/prometheus.yml \
    -v prometheus_data:/prometheus \
    prom/prometheus

# open shell in container
$ docker exec -it 997012faa239 sh

```

## Run Graphana

```
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

## Graphana Metrics

List of important metrics:

* node_thermal_zone_temp

## Generate kubadm token:

```
source .venv/bin/activate && \
export KUBEADM_INIT_TOKEN=`python3 tools/generate_k8s_token.py`
```

## Export kubernetes master hostname

```
export KUBEADM_MASTER_HOST=master-dca6322666c6
```

## Execute playbook


All machines:

```
ansible-playbook playbook.yml -i inventory -e@~/.ansible/vault.yml --ask-vault-pass
```


Single machine:

```
ansible-playbook playbook.yml -l dca632266607 ... (all other parameters)
```


All machines but starting from a specific tastk:

```
ansible-playbook playbook.yml --start-at-task="task name" ... (all other parameters)
```

## Manage Ansible vault

Create vault
```
ansible-vault create ~/.ansible/vault.yml
```

Edit vault
```
ansible-vault edit ~/.ansible/vault.yml
```

## Endpoints

* Prometheus: http://localhost:9090
* Graphana: http://localhost:3000

## Check Raspberry Pi temperature

```
/opt/vc/bin/vcgencmd measure_temp
```

### yoyo migrations commands

```
yoyo new -m "Add column role to Host"
```

```
yoyo apply
```