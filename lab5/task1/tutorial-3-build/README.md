# Руководство 3. Build infrastructure

Конфигурация создаёт Docker-образ `nginx:1.28` и контейнер `tutorial`,
пробрасывая порт 8000 хоста на 80 контейнера.

```bash
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
terraform init
terraform plan
terraform apply -auto-approve
```

Результат — файл [`output.txt`](output.txt). После применения:

```bash
terraform state list
docker ps --filter name=tutorial
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000
```
