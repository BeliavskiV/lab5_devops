output "cluster_name" {
  description = "Имя созданного кластера"
  value       = terraform_data.cluster.triggers_replace
}

output "kubeconfig_path" {
  description = "Путь к kubeconfig кластера"
  value       = "${path.module}/kubeconfig"
}

output "kind_config_path" {
  description = "Путь к конфигурации кластера kind"
  value       = local_file.kind_config.filename
}
