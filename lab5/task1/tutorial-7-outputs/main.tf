terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {}

variable "container_name" {
  description = "Value of the name for the Docker container"
  type        = string
  default     = "ExampleNginxContainer"
}

resource "docker_image" "nginx" {
  name         = "nginx:1.28"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = var.container_name

  ports {
    internal = 80
    external = 8000
  }
}

output "container_name" {
  value       = docker_container.nginx.name
  description = "The name of the Docker container"
}

output "container_id" {
  value       = docker_container.nginx.id
  description = "The ID of the Docker container"
}
