# Руководство 5. Destroy infrastructure

Уничтожаем созданные ресурсы (контейнер и образ) командой:

```bash
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
cd ../tutorial-3-build
terraform destroy -auto-approve
```

Результат — файл [`output.txt`](output.txt): Terraform показал план на удаление
2 ресурсов и подтвердил `Destroy complete! Resources: 2 destroyed`.
