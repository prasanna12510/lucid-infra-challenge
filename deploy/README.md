## Deploy APP using Skaffold

1. Install
```shell
export APP_VERSION=<version>
skaffold deploy -n reminder-api -t ${APP_VERSION}
```
2. Uninstall
```shell
skaffold delete
```
