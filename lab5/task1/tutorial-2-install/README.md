# Руководство 2. Install Terraform

## Установка

Штатная установка через Homebrew:

```bash
brew install hashicorp/tap/terraform
```

В сети выполнения работы загрузка с `releases.hashicorp.com` блокируется, поэтому
бинарник установлен с зеркала `hashicorp-releases.yandexcloud.net`:

```bash
curl -fsSL -o terraform.zip \
  https://hashicorp-releases.yandexcloud.net/terraform/1.16.5/terraform_1.16.5_darwin_arm64.zip
unzip terraform.zip
mv terraform /opt/homebrew/bin/terraform
chmod +x /opt/homebrew/bin/terraform
```

## Проверка

```bash
$ terraform version
Terraform v1.16.5
on darwin_arm64
```

Установленная версия корректно запускается и сообщает платформу `darwin_arm64`
(Apple Silicon).
