# Задание 3. Создание кластера с помощью Terraform и Ansible локально

## Вариант

Вариант **2** — кластер на основе Docker-контейнеров (kind, Docker-in-Docker).
Хостовая машина работает на Apple Silicon, поэтому локальные гипервизоры
варианта 1 (VirtualBox, Libvirt/KVM) недоступны.

Обязательное условие варианта 2 выполнено: используются **Terraform**,
**Ansible**, **Kubernetes** и **Docker**.

## Состав

```
task3/
  terraform/            # создание кластера kind
    main.tf             # terraform_data + local_file, вызов kind CLI
    providers.tf
    variables.tf
    outputs.tf
    kind-config.yaml    # генерируется Terraform
    kubeconfig          # генерируется Terraform (в .gitignore)
  ansible/
    inventory.yml       # localhost
    playbooks/
      deploy-app.yml    # метки нод, применение манифестов, ожидание готовности
      verify.yml        # вывод состояния кластера
  k8s/                  # манифесты приложения
    00-namespace.yaml
    01-secret.yaml
    02-configmap-liquibase.yaml
    03-postgres.yaml
    04-liquibase-job.yaml
    05-app.yaml
    06-nginx-configmap.yaml
    07-nginx.yaml
  app/                  # исходники приложения из лабораторной №1 (задание 5)
  liquibase/Dockerfile  # образ Liquibase с JDBC-драйвером PostgreSQL
  logs/                 # вывод выполненных команд
```

## Инфраструктура

Terraform создаёт кластер `lab5` из трёх нод (1 control-plane + 2 worker) и
выгружает kubeconfig. Кластер создаётся вызовом kind CLI из `terraform_data`,
конфигурация кластера формируется через `yamlencode`.

```bash
cd task3/terraform
terraform init
terraform apply -auto-approve
```

## Развёртывание приложения

Приложение — проект из задания 5 лабораторной работы №1: FastAPI + PostgreSQL
+ миграции Liquibase. Перед ним стоит nginx (задание 4 лабораторной №1).

```bash
cd task3/ansible
ansible-playbook playbooks/deploy-app.yml
ansible-playbook playbooks/verify.yml
```

Playbook помечает ноды (`node-role=web`, `node-role=db`), применяет манифесты и
дожидается готовности компонентов.

## Размещение сервисов по нодам

| Компонент | Нода | Как задано |
|-----------|------|------------|
| nginx | `lab5-worker` | `nodeSelector: node-role=web` |
| app (FastAPI) | `lab5-worker` | `nodeSelector: node-role=web` |
| db (PostgreSQL) | `lab5-worker2` | `nodeSelector: node-role=db` |
| liquibase (Job) | `lab5-worker` | планировщик |

## Проверка

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:30080/docs
curl -s http://localhost:30080/students
curl -s http://localhost:30080/reports/summary
```

Результаты — в [`logs/`](logs/).

## Образы

| Образ | Назначение |
|-------|------------|
| `nrashchynski/lab5-students-app:v1` | FastAPI-приложение |
| `nrashchynski/lab5-liquibase:v1` | Liquibase + JDBC-драйвер PostgreSQL |

Драйвер добавляется в образ, потому что переменная `INSTALL_POSTGRESQL_DRIVER`
в актуальной версии образа Liquibase не устанавливает его автоматически.
JAR скачивается при сборке и получает права `644`, иначе контейнер работает
под пользователем `liquibase` и не может прочитать файл.
