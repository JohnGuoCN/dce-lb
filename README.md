# DCE Haproxy
========

可用于生成级别的Haproxy，支持DNS-SRV

## Features

* **Everything in a single container** — no dependeny, no spf
* **Simple & Replayable** — based on nginx and inotify
* **Swarm Support** — hahaha
* **Extendable** — can work with haproxy


## Quick Start

### Prerequisites

docker compose installed

### Run a 2048 game like Herok

A docker-compose.yml looks like this:

	version: '2'
	services:
	  lb:
	    build: .
	    ports: 
	    - 8080:80
	    - 1936
	    environment:
	      MODE: http
	      SERVICE_NAME: web
	      SERVICE_PORT: 80
	  web:
	    image: alexwhen/docker-2048
      
Run Command
      
	docker-compose up -d
	docker-compose scale web=3
	
## Configuration

### Global and default settings of HAProxy###

Settings in this part is immutable, you have to redeploy HAProxy service to make the changes take effects

|Environment Variable|Default|Description|
|:-----:|:-----:|:----------|
|SERVICE_NAME| | 服务名|
|SERVICE_PORT|80|服务端口|
|BALANCE_ALGORITHM|roundrobin|`roundrobin`, `static-rr`, `source`, `leastconn`. See:[HAProxy:balance](https://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-balance)|
|MODE|http|http, tcp|
|MAXCONN|50000|concurrent connections|
|CONNECT_TIMEOUT|5000||
|CLIENT_TIMEOUT|50000||
|SERVER_TIMEOUT|50000||
|STATS_AUTH_USER|admin|Haproxy stats user.|
|STATS_AUTH_PASS|admin|Haproxy stats pass.|
|CHECK_INTERVAL|2000||
|CHECK_RISE_THRESHOLD|2||
|CHECK_FAIL_THRESHOLD|3||
|APPSESSION||sticky session option, possible value `JSESSIONID len 52 timeout 3h`. See:[HAProxy:appsession](http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-appsession)|
|COOKIE||sticky session option. Possible value `SRV insert indirect nocache`. See:[HAProxy:cookie](http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-cookie)|
|SSL_CERT||ssl cert, a pem file with private key followed by public certificate, '\n'(two chars) as the line separator|


## Affinity and session stickiness

There are three method to setup affinity and sticky session:

1. set `BALANCE=source` in your application service. When setting `source` method of balance, HAProxy will hash the client IP address and make sure that the same IP always goes to the same server.
2. set `APPSESSION=<value>`. use application session to determine which server a client should connect to. Possible value of `<value>` could be `JSESSIONID len 52 timeout 3h`
2. set `COOKIE=<value>`. use application cookie to determine which server a client should connect to. Possible value of `<value>` could be `SRV insert indirect nocache`

Check [HAProxy:appsession](http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-appsession) and [HAProxy:cookie](http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#4-cookie) for more information.


## 参考

[在 HAproxy 1.5 中使用 SSL 证书](http://www.oschina.net/translate/haproxy-ssl-termation-pass-through)
