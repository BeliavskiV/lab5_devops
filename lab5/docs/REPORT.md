# БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ
**Факультет прикладной математики и информатики**
**Кафедра технологий программирования**

## Отчет по лабораторной работе №5
**Тема:** Проектирование модели управления версиями ПО, конфигурациями и непрерывной поставкой
**Дисциплина:** Непрерывное интегрирование и сборка программного обеспечения

**Выполнил:** студент 11 группы Белявский Владислав Алексеевич  
**Вариант:** 2 (Terraform + Ansible + kind / Docker-in-Docker)  
**Преподаватель:** ст. преподаватель Давидовская М. И.  

Минск, 2026 г.

---

## 1. Цель работы

Изучение решений для автоматизации управления инфраструктурой и установки приложений: Terraform, Ansible и Kubernetes.

---

## 2. Вариант задания

Группа **11**: согласно критериям оценивания для групп 10–12 выполняются **все три задания** лабораторной работы.

Задание 3 выполнено по **варианту 2** (`kind`, Docker-in-Docker): хостовая машина работает на Apple Silicon / современной ОС, поэтому локальные гипервизоры варианта 1 (VirtualBox, Libvirt/KVM) заменены на контейнерную виртуализацию через `kind`. Обязательное условие варианта 2 — использование Terraform, Ansible, Kubernetes и Docker — полностью соблюдено.

---

## 3. Задание 1. Основы управления конфигурацией инфраструктуры с Terraform

Изучено официальное руководство [Terraform Tutorial — Get Started: Docker](https://developer.hashicorp.com/terraform/tutorials/docker-get-started) и выполнены все 7 руководств. Для каждого руководства в каталоге `task1/` лежит отдельная папка с конфигурацией и выводом команд.

### 3.1. Окружение

| Инструмент | Версия | Назначение |
|------------|--------|------------|
| Terraform | v1.16.5 | управление инфраструктурой |
| Docker Desktop / Engine | 29.8.0 | запуск контейнеров (провайдер `kreuzwerker/docker`) |
| Хост | macOS / Linux | хостовая система |

### 3.2. Руководство 1. What is Infrastructure as Code with Terraform?

Вводное интерактивное руководство. Конфигурационных файлов не содержит: объясняет принципы Infrastructure as Code (инфраструктура описывается декларативно, хранится в системе контроля версий, изменения проходят через `plan` и `apply`, состояние отслеживается в state-файле).

### 3.3. Руководство 2. Install Terraform

Установка и проверка версии:

```bash
$ terraform version
Terraform v1.16.5
```

### 3.4. Руководство 3. Build infrastructure

Конфигурация (`task1/tutorial-3-build/main.tf`):

```hcl
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:1.28"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial"

  ports {
    internal = 80
    external = 8000
  }
}
```

Команды и результат:

```bash
$ terraform init
Terraform has been successfully initialized!

$ terraform plan
Plan: 2 to add, 0 to change, 0 to destroy.

$ terraform apply -auto-approve
docker_image.nginx: Creation complete after 0s [id=sha256:146adea4768b...nginx:1.28]
docker_container.nginx: Creation complete after 0s [id=58272821e4e2...]
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

$ terraform state list
docker_container.nginx
docker_image.nginx

$ docker ps --filter name=tutorial
tutorial   146adea4768b   0.0.0.0:8000->80/tcp

$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000
200
```

Terraform создал образ и контейнер, состояние сохранено в `terraform.tfstate`.

### 3.5. Руководство 4. Change infrastructure

Внешний порт контейнера изменён с 8000 на 8001:

```bash
$ terraform apply -auto-approve
  # docker_container.nginx must be replaced
      ~ external = 8000 -> 8001 # forces replacement
Plan: 1 to add, 0 to change, 1 to destroy.
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.

$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8001
200
```

### 3.6. Руководство 5. Destroy infrastructure

```bash
$ terraform destroy -auto-approve
  # docker_container.nginx will be destroyed
  # docker_image.nginx will be destroyed
Plan: 0 to add, 0 to change, 2 to destroy.
docker_container.nginx: Destruction complete after 0s
docker_image.nginx: Destruction complete after 0s
Destroy complete! Resources: 2 destroyed.
```

### 3.7. Руководство 6. Define input variables

Имя контейнера вынесено в переменную `container_name`:

```hcl
variable "container_name" {
  description = "Value of the name for the Docker container"
  type        = string
  default     = "ExampleNginxContainer"
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = var.container_name
  # ...
}
```

Применение со значением по умолчанию и с переопределением через флаг `-var`:

```bash
$ terraform apply -auto-approve
Plan: 2 to add, 0 to change, 0 to destroy.
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

$ terraform apply -auto-approve -var='container_name=CustomNginxContainer'
Plan: 1 to add, 0 to change, 1 to destroy.
Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

### 3.8. Руководство 7. Query data with outputs

Добавлены выходные значения:

```hcl
output "container_name" {
  value       = docker_container.nginx.name
  description = "The name of the Docker container"
}

output "container_id" {
  value       = docker_container.nginx.id
  description = "The ID of the Docker container"
}
```

```bash
$ terraform output
container_id   = "a830138849c5f88afd63f2ab02054836d8a19b848ca29aaef4a61b187916262b"
container_name = "ExampleNginxContainer"
```

### 3.9. Вывод по заданию 1

Выполнены все 7 руководств Terraform Get Started — Docker. Код и вывод команд опубликованы в каталоге `task1/`.

---

## 4. Задание 2. Управление конфигурацией серверов с помощью Ansible

Изучены статьи *How To Set Up Ansible Inventories*, *How To Manage Multiple Servers with Ansible Ad Hoc Commands* и *How To Write Ansible Playbooks*.

### 4.1. Целевые хосты

В качестве целевых хостов используются ноды кластера `lab4` (1 control-plane + 2 worker), запущенные как Docker-контейнеры. Подключение осуществляется через connection-плагин `community.docker.docker`:

```yaml
all:
  vars:
    ansible_connection: community.docker.docker
    ansible_python_interpreter: /usr/bin/python3
  children:
    control_plane:
      hosts:
        lab4-control-plane:
    workers:
      hosts:
        lab4-worker:
        lab4-worker2:
    k8s_cluster:
      children:
        control_plane:
        workers:
```

### 4.2. Ad-hoc команды

Ping группы узлов:

```bash
$ ansible k8s_cluster -m ping
lab4-worker | SUCCESS => {"changed": false, "ping": "pong"}
lab4-control-plane | SUCCESS => {"changed": false, "ping": "pong"}
lab4-worker2 | SUCCESS => {"changed": false, "ping": "pong"}
```

Установка пакета `zsh`:

```bash
$ ansible workers -m apt -a "name=zsh state=present update_cache=yes"
```

### 4.3. Playbook'и

Пример роли `nginx`:

```yaml
# roles/nginx/tasks/main.yml
- name: Ensure nginx is installed
  ansible.builtin.apt:
    name: "{{ nginx_package }}"
    state: present
    update_cache: true

- name: Deploy the index page from a template
  ansible.builtin.template:
    src: index.html.j2
    dest: "{{ nginx_document_root }}/index.html"
    mode: "0644"
  notify: Restart nginx

- name: Ensure nginx is running and enabled
  ansible.builtin.service:
    name: "{{ nginx_package }}"
    state: started
    enabled: true
```

Запуск playbook:

```bash
$ ansible-playbook playbooks/nginx.yml
PLAY RECAP
lab4-worker  : ok=6 changed=2 failed=0
lab4-worker2 : ok=6 changed=2 failed=0
```

### 4.4. Вывод по заданию 2

Освоены inventory, ad-hoc команды и playbook'и с ролями и шаблонами.

---

## 5. Задание 3. Создание кластера с помощью Terraform и Ansible локально (Вариант 2)

### 5.1. Вариант и инструменты

Использован **вариант 2** (kind / Docker-in-Docker). Инфраструктура оркестрируется через Terraform, настройка и деплой приложений выполняются Ansible.

### 5.2. Создание кластера Terraform

Terraform формирует конфигурацию `kind-config.yaml` с пробросом порта `30080`:

```hcl
locals {
  kind_config = {
    kind       = "Cluster"
    apiVersion = "kind.x-k8s.io/v1alpha4"
    nodes = [
      {
        role = "control-plane"
        extraPortMappings = [
          { containerPort = 30080, hostPort = 30080, protocol = "TCP" }
        ]
      },
      { role = "worker" },
      { role = "worker" },
    ]
  }
}

resource "local_file" "kind_config" {
  content  = yamlencode(local.kind_config)
  filename = "${path.module}/kind-config.yaml"
}

resource "terraform_data" "cluster" {
  triggers_replace = var.cluster_name

  provisioner "local-exec" {
    command = <<-EOT
      kind create cluster --name "${self.triggers_replace}" \
        --config "${local_file.kind_config.filename}"
      kind export kubeconfig --name "${self.triggers_replace}" \
        --kubeconfig "${path.module}/kubeconfig"
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = "kind delete cluster --name ${self.triggers_replace}"
  }
}
```

```bash
$ terraform apply -auto-approve
terraform_data.cluster: Creation complete after 16s
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

### 5.3. Развёртывание приложения через Ansible

Развёрнут проект из лабораторной работы №1 (FastAPI + PostgreSQL + Liquibase + Nginx).
* **Размещение сервисов по нодам:**
  * `nginx` и `app` привязаны к ноде `lab5-worker` через `nodeSelector: node-role=web`.
  * `db` (PostgreSQL) привязана к ноде `lab5-worker2` через `nodeSelector: node-role=db`.

```bash
$ ansible-playbook playbooks/deploy-app.yml
PLAY RECAP
localhost : ok=15 changed=13 failed=0
```

Проверка доступности через NodePort (30080):

```bash
$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:30080/docs
200

$ curl -s http://localhost:30080/students
[{"full_name":"Иванов Иван","specialty":"ПМ","id":1,"status":"enrolled"}]
```

### 5.4. Вывод по заданию 3

Кластер Kubernetes из трёх нод создан через Terraform (kind), приложение развёрнуто через Ansible, сервисы разнесены по нодам согласно заданию.

---

## 6. Контрольные вопросы

1. **Для каких задач применяется Ansible?**  
   Для настройки серверов, установки и обновления ПО, развёртывания приложений и автоматизации инфраструктуры без агентов.
2. **Какие способы управления серверами применяются в Ansible?**  
   Ad-hoc команды, Playbooks и Роли.
3. **Что входит в состав файла Ansible playbook?**  
   Список пьес (`plays`), содержащих выборку хостов (`hosts`), переменные (`vars`), задачи (`tasks`), обработчики (`handlers`) и роли (`roles`).
4. **Что такое группы узлов (хостов) в Ansible?**  
   Именованные логические объединения хостов в inventory для массового применения команд и конфигураций.
5. **Как одной командой выполнить ping группы узлов (хостов)?**  
   `ansible <группа> -m ping`.
6. **Что такое роль Ansible?**  
   Стандартизированная структура каталогов для организации и повторного использования задач, файлов и шаблонов.
7. **Что такое файл инвентаризации Ansible и как он используется?**  
   Inventory (INI или YAML) со списком управляемых узлов и параметров подключения к ним.
8. **Что такое специальная команда Ansible?**  
   Ad-hoc команда для выполнения разовых операций без написания playbook.
9. **Как перезапустить службу с помощью Ansible?**  
   Использованием модуля `service` с параметром `state: restarted`.
10. **Что такое Hashicorp Terraform?**  
    Инструмент Infrastructure as Code (IaC) для декларативного описания и управления инфраструктурой.
11. **Что такое инфраструктура как код (Infrastructure as Code — IaC)?**  
    Подход к управлению инфраструктурой с помощью текстовых файлов в системах контроля версий.
12. **Как установить Terraform?**  
    Скачать бинарный файл с сайта HashiCorp или установить через пакетный менеджер (`brew install terraform`).
13. **Что такое провайдер (поставщик) в Terraform?**  
    Плагин для взаимодействия Terraform с API конкретной платформы или облака (AWS, Docker, Kubernetes).
14. **Базовая структура файла конфигурации Terraform:**  
    Блоки `terraform`, `provider`, `resource`, `variable` и `output`.
15. **Что такое файл состояния Terraform?**  
    State-файл (`terraform.tfstate`), хранящий соответствие между конфигурацией и реальными ресурсами.
16. **Для чего нужна terraform destroy команда?**  
    Для полного удаления инфраструктуры, созданной в рамках конфигурации.
17. **Что такое состояние в Terraform?**  
    Снимок текущей развёрнутой инфраструктуры, используемый для вычисления изменений.
18. **Как определить зависимости в Terraform?**  
    Через неявные ссылки на атрибуты других ресурсов либо явно через метааргумент `depends_on`.