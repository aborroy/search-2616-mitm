# Docker Compose template for SEARCH-2616 using mitmproxy

This project includes a Docker Compose template to deploy:

* Alfresco Repository using S3 for storage
* Search Services 1.4.3
* Search Services 2.0.1

Volumes are configured so the information is persisted.

The `alfresco-proxy` Docker service intercepts requests to get Metadata and Content from SOLR in order to provide auto-generated random data (instead of recovering metadata from Database and content from Transform Service). The indexing process is faster but the indexed data is not real.

>> Use this approach only for performance testing!

## Starting the project

Review the configuration file in order to add S3 credentials and Docker Image release tags.

```
$ cat .env

# Docker Image versions
ALFRESCO_TAG=7.0.0
SEARCH_CE_TAG=2.0.1
SHARE_TAG=7.0.0
ACA_TAG=2.3.0
POSTGRES_TAG=13.1
API_EXPLORER_TAG=7.0.0
TRANSFORM_ENGINE_TAG=2.3.10
ACTIVEMQ_TAG=5.16.1

# Server properties
SERVER_NAME=localhost

# S3 Repository Bucket for alf_data folder
S3_ACCESS_KEY=<S3_ACCESS_KEY>
S3_SECRET_KEY=<S3_SECRET_KEY>
S3_BUCKET_NAME=search-services-search-2616
S3_BUCKET_LOCATION=eu-west-1
S3_OBJECT_NAME_PREFIX=alf-data/
```

Start Docker Compose from project path.

```
$ docker-compose up --build --force-recreate
```

## Endpoints

Default credential: `admin/admin`

* Repository: http://localhost:8080/alfresco
* Solr 1.4.3: http://localhost:8091/solr
* Solr 2.0.1: http://localhost:8092/solr
