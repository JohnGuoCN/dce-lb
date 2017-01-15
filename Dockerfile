FROM haproxy:1.6.5-alpine

MAINTAINER Kay.Yan <kay.yan@daocloud.io> 

RUN apk update && \
    apk --no-cache add py-pip

COPY requirements.txt /dce-lb/requirements.txt

RUN cd /dce-lb && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV SERVICE_PORT=80 \
	RSYSLOG_DESTINATION=127.0.0.1 \
	MAXCONN=50000 \
	CONNECT_TIMEOUT=5000 \
	CLIENT_TIMEOUT=50000 \
	SERVER_TIMEOUT=50000 \
	MODE=http \
    BALANCE_ALGORITHM=roundrobin \
    CHECK_INTERVAL=2000 \
    CHECK_RISE_THRESHOLD=2 \
    CHECK_FAIL_THRESHOLD=3 \
    STATS_AUTH_USER="admin" \
    STATS_AUTH_PASS="admin"

EXPOSE 80 443 1936

ENTRYPOINT ["sh"]
CMD ["/dce-lb/entrypoint.sh"]

COPY . /dce-lb
