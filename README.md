# Deploying a Reminder API using Flask and MySQL server on Kubernetes

This repo contains code that
1) Deploys a MySQL server on a Kubernetes cluster
2) Attaches a persistent volume to it, so the data remains contained if pods are restarting
3) Deploys a Flask API to add, delete and modify reminders in the MySQL database

## Prerequisites
1. Have `Docker` and the `Kubernetes CLI` (`kubectl`) installed together with `Minikube` (https://kubernetes.io/docs/tasks/tools/)

## Getting started
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: `eval $(minikube docker-env)`
3. Pull the latest mysql image from `Dockerhub`: `Docker pull mysql`
4. Build a kubernetes-api image with the Dockerfile in this repo: `Docker build . -t reminder-api`

## Deployments
Get the secrets, persistent volume in place and apply the deployments for the `MySQL` database and `Flask API`

1. create kind kubernetes cluster using terraform in infra/k8s `terraform plan && terraform apply`
2. Deploy standalone MySQL using skaffold in infra/mysql `skaffold deploy`
4. Deploy `Flask API` in deploy folder: `skaffold deploy -t <version:latest>`

You can check the status of the pods, services and deployments.

## Creating database and schema
The API can only be used if the proper database and schemas are set. This can be done via the terminal.
1. Connect to your `MySQL database` by setting up a temporary pod as a `mysql-client`:
   `kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql.mysql.svc --password=<super-secret-password>`
   make sure to enter the (decoded) password specified in the `kubectl get secrets/reminder-api-mysql-secret --template={{.data.password}} | base64 -D`
2. Create the database schema from infra/mysql
    1. `mysql -hmysql.mysql.svc -uusername -ppassword database_name < db.sql`

## Expose K8s API for GitHub Actions
1. port-forward k8s api
```shell
kubectl proxy --disable-filter=true --port=8080 --accept-hosts='.*\.ngrok.io' & (to run process in background)
```
2. setup ngrok as public proxy that routes requests to your Kubernetes API server.
```shell
ngrok http http://127.0.0.1:8080
```
3. retrieve the kubeconfig and add the ngrok url as server url
```yaml
apiVersion: v1
clusters:
- cluster:
    server: https://f732-180-129-27-255.ngrok.io
    insecure-skip-tls-verify: true
  name: kind-k8s-local
contexts:
- context:
    cluster: kind-k8s-local
    user: kind-k8s-local
  name: kind-k8s-local
current-context: kind-k8s-local
kind: Config
preferences: {}
users:
- name: kind-k8s-local
  user:
    client-certificate-data: <cert>
    client-key-data:  <key>
```
4. create GCR Pull secrets
a.
```shell
echo -n "username:<ghcr_token>" | base64
dXNlcm5hbWU6MTIzMTIzYWRzZmFzZGYxMjMxMjM=
```
b.
```shell
{
    "auths":
    {
        "ghcr.io":
            {
                "auth":"dXNlcm5hbWU6MTIzMTIzYWRzZmFzZGYxMjMxMjM="
            }
    }
}
```

## Expose the API
The API can be accessed by exposing it using minikube: `minikube service reminder-api-service`. This will return a `URL`. If you paste this to your browser you will see the `hello world` message. You can use this `service_URL` to make requests to the `API`

## Start making requests
Now you can use the `API` to `Query` your database
1. add a reminder: `curl -H "Content-Type: application/json" -d '{"message": "please check", "time": "7:30"}' <service_URL>/api/reminders`
2. get all reminders: `curl <service_URL>/api/reminders`



#### AWS Production Grade Architecture

![Alt text](https://github.com/prasanna12510/lucid-infra-challenge/blob/main/doc/img/APIArchicture.png?raw=true "AWSArchitecture")

## API Output
1. List of all Reminders
![Alt text](https://github.com/prasanna12510/lucid-infra-challenge/blob/main/doc/img/APIOutput.png?raw=true "APIOutput")
