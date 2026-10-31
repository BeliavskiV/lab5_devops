# Руководство 6. Define input variables

Имя контейнера вынесено в переменную `container_name` (значение по умолчанию —
`ExampleNginxContainer`). Значение можно задать через `terraform.tfvars`, флаг
`-var` или переменную окружения `TF_VAR_container_name`.

```bash
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
terraform init
terraform apply -auto-approve
terraform apply -auto-approve -var='container_name=CustomNginxContainer'
```

Результат — файл [`output.txt`](output.txt): при смене значения Terraform
пересоздаёт контейнер с новым именем.
