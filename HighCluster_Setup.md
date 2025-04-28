# High Availability Database Cluster with 3 Node

## Postgresql installation
```
sudo apt install -y postgresql-common  
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh

------------------------------------------------------------
sudo apt install curl ca-certificates  
sudo install -d /usr/share/postgresql-common/pgdg  
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc  
sudo sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'  
sudo apt update  
sudo apt -y install postgresql postgresql-server-dev
```
```
sudo ln -s /usr/lib/postgresql/version(eg.15,17)/bin/* /usr/sbin/
```

Optionally you can stop the postgresql server before start patroni.
```
sudo systemctl stop postgresql
```

## Patroni installation

```
sudo apt -y install python3 python3-pip
sudo apt install python3-pip python3-dev libpq-dev -y
sudo pip3 install --upgrade pip
sudo -H pip3 install --upgrade testresources
sudo -H pip3 install --upgrade setuptools
sudo -H pip3 install psycopg2
sudo -H pip3 install patroni
sudo -H pip3 install python-etcd
```
**Edit Configuration YML**
Create yml file at path **/etc/patroni.yml**
 ```
sudo nano /etc/patroni.yml
```
 Edit yml file.
 ```
scope: postgres
namespace: /db/
name: patronidb1

restapi:
  listen: <node_ip>:8008
  connect_address: <node_ip>:8008

etcd:
  host: <etcd_host_ip>:2379

bootstrap:
  dcs:
    synchronous_mode: true
    synchrounus_mode_strict: false
    sync_count: 1
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pq_rewind: true


  initdb:
  - encoding: UTF8
  - data-checksums

  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host replication replicator <node_ip_1>/0 md5
  - host replication replicator <node_ip_2>/0 md5
  - host replication replicator <node_ip_3>/0 md5
  - host all all 0.0.0.0/0 md5
  users:
    admin:
      password: admin
      options:
        - createrole
        - createdb


postgresql:
  listen: <node_ip>
  connect_address: <node_ip>
  data_dir: /data/patroni
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: **********
    superuser:
      username: postgres
      password: **********
    parameters:
      unix_socket_directories: '.'

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false

```

Create and assign directory to postgres user.
```
sudo mkdir -p /data/patroni
sudo chown postgres:postgres /data/patroni
sudo chmod 700 /data/patroni 
```
Create patroni service file at /etc/systemd/system/patroni.service

```
[Unit]
Description=Runners to orchestrate a high-availability PostgreSQL
After=syslog.target network.target

[Service]
Type=simple

User=postgres
Group=postgres

ExecStart=/usr/local/bin/patroni /etc/patroni.yml
KillMode=process
Timeout=30
Restart=no

[Install]
WantedBy=multi-user.targ
```
## Etcd Installation
````
sudo apt install etcd
````

Configure etcd 
```
sudo nano /etc/default/etcd

ETCD_LISTEN_PEER_URLS="http://<etcd_host_ip>:2380"
ETCD_LISTEN_CLIENT_URLS="http://127.0.0.1:2379,http://<etcd_host_ip>:2379"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://<etcd_host_ip>:2380"
ETCD_INITIAL_CLUSTER="default=http://<etcd_host_ip>:2380,"
ETCD_ADVERTISE_CLIENT_URLS="http://<etcd_host_ip>:2379"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster"
ETCD_INITIAL_CLUSTER_STATE="new"
```
## Keepalived Installation

For giving virtual ip for haproxy to ensure service availability by routing network traffic to a backup server if the primary server fails.
```
sudo apt install keepalived
```
Edit configure file.
```
vrrp_instance VI_1 {
        state MASTER
        interface enp0s3
        virtual_router_id 51
        priority 100
        advert_int 1

        authentication {
                auth_type PASS
                auth_pass secret
        }

        virtual_ipaddress {
                <virtual_ip>
        }

}
```

## Haproxy Installation
It can be downloaded on same host with etcd or seperatly
```
sudo apt install haproxy
```
Edit configuration file

```
sudo nano /etc/haproxy/haproxy.cfg
global
        maxconn 4000

defaults
        log global
        mode tcp
        retries 2
        timeout connect 4s
        timeout client 30m
        timeout server 30m
        timeout check 5s

listen stats
        mode http
        bind <haproxy_host_ip or virtual_ip>:7000
        stats enable
        stats uri /

listen postgres
        bind <haproxy_host_ip or virtual_ip>:5000
        option httpchk
        http-check expect status 200
        default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
        server node1 <node_ip_1>:5432 maxconn 1000 check port 8008
        server node2 <node_ip_2>:5432 maxconn 1000 check port 8008
        server node3 <node_ip_3>:5432 maxconn 1000 check port 8008
```



# Starting Servers
*  Etcd Server on etcd node
```
sudo systemctl start etcd
sudo systemctl status etcd
```

* Patroni servers on nodes
```
sudo systemctl daemon-reload

sudo systemctl enable patroni 
sudo systemctl enable postgresql

sudo systemctl start patroni
sudo systemctl start postgresql

# Patroni service status
sudo systemctl status patroni.service

# Check patroni cluster
sudo patronictl -c /etc/patroni.yml list
```

* Haproxy and Keepalived on etcd node or different node
```
sudo systemctl start haproxy
sudo systemctl start keepalived

sudo systemctl enable haproxy
sudo systemctl enable keepalived

sudo systemctl status haproxy
sudo systemctl status keepalived

```


