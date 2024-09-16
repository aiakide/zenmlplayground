#!make
include .env

envs:
	echo "${OBJC_DISABLE_INITIALIZE_FORK_SAFETY}"

zenml-connect:
	zenml connect --url http://localhost:8080 --api-key ${ZENML_API_KEY}

zenml-create-minio-secret:
	zenml secret create minio_secret \
    --aws_access_key_id=${MINIO_ACCESS_KEY} \
    --aws_secret_access_key=${MINIO_SECRET_KEY}

zenml-register-artifact-store-minio:
	zenml artifact-store register minio_store -f s3 \
    --path='s3://zenml' \
    --authentication_secret=minio_secret \
    --client_kwargs='{"endpoint_url": "http://localhost:9000", "region_name": "eu-east-1"}'

zenml-register-container-registry:
	zenml container-registry register local-docker-registry \
    --flavor=default \
    --uri=localhost:5000

zenml-register-docker-service-connector:
	zenml service-connector register local-docker-registry-service-connector --type docker --username=${DOCKER_REGISTRY_USER} --password=${DOCKER_REGISTRY_PASSWORD} --registry=localhost:5000

zenml-connect-container-registry:
	zenml container-registry connect local-docker-registry --connector=local-docker-registry-service-connector

zenml-register-docker-orchestrator:
	zenml orchestrator register docker \
    --flavor=local_docker
zenml-local-image-builder:
	zenml image-builder register local-image-builder --flavor=local


zenml-register-stack:
	zenml stack register docker-minio -o docker -a minio_store -c local-docker-registry -i local-image-builder

zenml-connect-github-repo:
	zenml code-repository register ${REPO_NAME} --type=github \
	--url=https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git \
	--owner=${GITHUB_USERNAME} --repository=${REPO_NAME} \
	--token=${GITHUB_TOKEN}

zenml-create-service-account:
	zenml service-account create nils
