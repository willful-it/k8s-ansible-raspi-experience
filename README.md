## Run Prometheus
```
docker run \
    -p 9090:9090 \
    -v /home/renato/Projects/willful/gitrepo/k8s-ansible-raspi-experience/prom/phrometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

## Run Graphana
```
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

## Execute playbook

```
ansible-playbook playbook.yml -l dca632266607 -i inventory --user=pi
```