.PHONY:generate
generate:
	cd experiment && \
	xsdata generate "./schemas/" \
	--config ./xsdata_config.xml && \
	cd -
