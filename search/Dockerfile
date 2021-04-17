ARG SEARCH_TAG
FROM alfresco/alfresco-search-services:${SEARCH_TAG}

# COMMON
ARG ALFRESCO_HOSTNAME
ARG SOLR_HOSTNAME
ENV ALFRESCO_HOSTNAME $ALFRESCO_HOSTNAME
ENV SOLR_HOSTNAME $SOLR_HOSTNAME

# Configure Alfresco Service Name
RUN sed -i '/^bash.*/i sed -i "'"s/alfresco.host=localhost/alfresco.host=${ALFRESCO_HOSTNAME}/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
    ${DIST_DIR}/solr/bin/search_config_setup.sh && \
    sed -i '/^bash.*/i sed -i "'"s/solr.host=localhost/solr.host=${SOLR_HOSTNAME}/g"'" ${DIST_DIR}/solrhome/conf/shared.properties\n' \
    ${DIST_DIR}/solr/bin/search_config_setup.sh

# COMMS
ARG ALFRESCO_COMMS
ENV ALFRESCO_COMMS $ALFRESCO_COMMS

# Configure SOLR cores to run in HTTPs mode from template
RUN if [ "$ALFRESCO_COMMS" == "https" ] ; then \
    sed -i '/^bash.*/i sed -i "'"s/alfresco.secureComms=none/alfresco.secureComms=https/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
    ${DIST_DIR}/solr/bin/search_config_setup.sh; \
else \
    sed -i '/^bash.*/i sed -i "'"s/alfresco.secureComms=https/alfresco.secureComms=none/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
    ${DIST_DIR}/solr/bin/search_config_setup.sh; \
fi

# Cache size
ARG NO_CACHE
ENV NO_CACHE $NO_CACHE
RUN if [ "$NO_CACHE" == "true" ] ; then \
  sed -i '/^bash.*/i sed -i "'"s/solr.documentCache.autowarmCount=512/solr.documentCache.autowarmCount=0/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
  ${DIST_DIR}/solr/bin/search_config_setup.sh && \
  sed -i '/^bash.*/i sed -i "'"s/solr.documentCache.size=1024/solr.documentCache.size=0/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
  ${DIST_DIR}/solr/bin/search_config_setup.sh && \
  sed -i '/^bash.*/i sed -i "'"s/solr.documentCache.initialSize=1024/solr.documentCache.initialSize=0/g"'" ${DIST_DIR}/solrhome/templates/rerank/conf/solrcore.properties\n' \
  ${DIST_DIR}/solr/bin/search_config_setup.sh; \
fi
