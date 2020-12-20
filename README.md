## Run Prometheus with Docker

```bash
# create volume for Prometheus data
$ docker volume create prometheus_data

# launch container
$ docker run \
    -p 9090:9090 \
    -v /home/renato/Projects/willful/gitrepo/k8s-ansible-raspi-experience/prom/phrometheus.yml:/etc/prometheus/prometheus.yml \
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

## Execute playbook

```
ansible-playbook playbook.yml -l dca632266607 -i inventory --user=pi
```