ARG ALFRESCO_TAG
FROM quay.io/alfresco/alfresco-content-repository:${ALFRESCO_TAG}

ARG TOMCAT_DIR=/usr/local/tomcat

USER root

# Install modules and addons
RUN mkdir -p $TOMCAT_DIR/amps
COPY modules/amps $TOMCAT_DIR/amps
COPY modules/jars $TOMCAT_DIR/webapps/alfresco/WEB-INF/lib

RUN java -jar $TOMCAT_DIR/alfresco-mmt/alfresco-mmt*.jar install \
    $TOMCAT_DIR/amps $TOMCAT_DIR/webapps/alfresco -directory -nobackup -force

# Install the license
COPY alf70-allenabled.lic /usr/local/tomcat/shared/classes/alfresco/extension/license/alfresco.lic

# Change Repository port to support mitmproxy
RUN sed  -i 's/Connector port="8080"/Connector port="9999"/g' $TOMCAT_DIR/conf/server.xml
