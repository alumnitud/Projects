terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azapi = {
      source  = "Azure/azapi"
      version = "~> 1.5"
    }
  }
}

provider "azapi" {
  subscription_id = var.subscription_id
}