# Руководство 4. Change infrastructure

Меняем внешний порт контейнера с 8000 на 8001. Terraform показывает, что контейнер
будет пересоздан (`forces replacement`), и применяет изменение.

```bash
sed -i '' 's/external = 8000/external = 8001/' ../tutorial-3-build/main.tf
cd ../tutorial-3-build && terraform apply -auto-approve
```

Результат — файл [`output.txt`](output.txt). В этом каталоге лежит снимок
конфигурации после изменения.
