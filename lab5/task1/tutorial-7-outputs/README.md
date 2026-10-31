# Руководство 7. Query data with outputs

Добавлены выходные значения `container_name` и `container_id`, которые берутся
из состояния Terraform.

```bash
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
terraform init
terraform apply -auto-approve
terraform output
terraform output -raw container_name
terraform output -raw container_id
```

Результат — файл [`output.txt`](output.txt).
