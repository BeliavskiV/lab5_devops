# Задание 1. Terraform Get Started — Docker

Официальный трек [Get Started — Docker](https://developer.hashicorp.com/terraform/tutorials/docker-get-started)
состоит из 7 руководств. Для каждого руководства в этой папке лежит отдельный каталог
с конфигурацией Terraform и выводом команд.

| № | Руководство | Каталог |
|---|-------------|---------|
| 1 | What is Infrastructure as Code with Terraform? | [`tutorial-1-iac/`](tutorial-1-iac/) |
| 2 | Install Terraform | [`tutorial-2-install/`](tutorial-2-install/) |
| 3 | Build infrastructure | [`tutorial-3-build/`](tutorial-3-build/) |
| 4 | Change infrastructure | [`tutorial-4-change/`](tutorial-4-change/) |
| 5 | Destroy infrastructure | [`tutorial-5-destroy/`](tutorial-5-destroy/) |
| 6 | Define input variables | [`tutorial-6-variables/`](tutorial-6-variables/) |
| 7 | Query data with outputs | [`tutorial-7-outputs/`](tutorial-7-outputs/) |

## Особенности окружения

- Провайдер `kreuzwerker/docker` скачивается через зеркало
  `terraform-mirror.yandexcloud.net`, т.к. `registry.terraform.io` недоступен из сети
  выполнения работы (настраивается в `~/.terraformrc`).
- Docker-провайдер подключается к сокету Docker Desktop:
  `export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock`.
- Образ `nginx` зафиксирован на версии `1.28`, чтобы не конфликтовать с уже
  существующими локальными контейнерами на `nginx:latest`.
