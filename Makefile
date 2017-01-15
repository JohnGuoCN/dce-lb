include ../Makefile.variable

all: dceLBContainer

dceLBContainer: 
	docker build -t $(HUB_PREFIX)/$(DCE_LB):$(DCE_VERSION) .

release: dceLBContainer
	docker push $(HUB_PREFIX)/$(DCE_LB):$(DCE_VERSION)

clean:
	

latest:
	docker tag $(HUB_PREFIX)/$(DCE_LB):$(DCE_VERSION) $(HUB_PREFIX)/$(DCE_LB):latest
	docker push $(HUB_PREFIX)/$(DCE_LB):latest
	
.PHONY: all clean
