terraform {
  required_version = ">= 1.6"
}

locals {
  kind_config = {
    kind       = "Cluster"
    apiVersion = "kind.x-k8s.io/v1alpha4"
    nodes = [
      {
        role = "control-plane"
        extraPortMappings = [
          {
            containerPort = 30080
            hostPort      = 30080
            protocol      = "TCP"
          }
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
      kind create cluster \
        --name "${self.triggers_replace}" \
        --config "${local_file.kind_config.filename}"
      kind export kubeconfig \
        --name "${self.triggers_replace}" \
        --kubeconfig "${path.module}/kubeconfig"
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = "kind delete cluster --name ${self.triggers_replace}"
  }

  depends_on = [local_file.kind_config]
}
