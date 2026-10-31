# Задание 2. Управление конфигурацией серверов с помощью Ansible

## Что изучено

- How To Set Up Ansible Inventories
- How To Manage Multiple Servers with Ansible Ad Hoc Commands
- Using Ansible command line tools
- How To Write Ansible Playbooks
- Using Ansible playbooks

## Целевые хосты

В варианте 2 (kind) виртуальных машин нет: ноды Kubernetes — это Docker-контейнеры.
В качестве целевого кластера использован кластер `lab4` из предыдущей лабораторной
работы (1 control-plane + 2 worker). Ansible подключается к контейнерам через
connection-плагин `community.docker.docker`.

Так как образ `kindest/node` не содержит Python, на ноды предварительно установлен
`python3` (через модуль `raw`), после чего доступны обычные модули Ansible.

## Структура

```
task2/ansible/
  ansible.cfg              # inventory, roles_path, inject_facts_as_vars = False
  inventory.yml            # группы: control_plane, workers, k8s_cluster
  playbooks/
    ping.yml               # ping всех нод + вывод фактов
    system-info.yml        # пример из документации: память и CPU
    nginx.yml              # playbook с ролью
  roles/nginx/
    tasks/main.yml         # установка, шаблон, запуск службы
    handlers/main.yml      # перезапуск nginx при изменении шаблона
    templates/index.html.j2
    defaults/main.yml
  logs/                    # вывод выполненных команд
```

## Инвентарь

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

## Ad-hoc команды

```bash
ansible-inventory --graph
ansible k8s_cluster -m ping
ansible workers -m apt -a "name=zsh state=present update_cache=yes"
ansible workers -m shell -a "zsh --version"
ansible workers -m service -a "name=nginx state=restarted"
```

Вывод — в [`logs/adhoc.txt`](logs/adhoc.txt) и [`logs/adhoc-zsh.txt`](logs/adhoc-zsh.txt).

## Playbook'и

```bash
ansible-playbook --syntax-check playbooks/*.yml
ansible-playbook playbooks/ping.yml
ansible-playbook playbooks/system-info.yml
ansible-playbook playbooks/nginx.yml
```

Повторный запуск `nginx.yml` показывает `changed=0` — идемпотентность playbook'а.
Вывод — в каталоге [`logs/`](logs/).
