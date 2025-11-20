# -------------------------------------------------------------
# 1. Resource Group
# -------------------------------------------------------------
resource "azapi_resource" "rg" {
  type      = "Microsoft.Resources/resourceGroups@2021-04-01"
  name = "terraform-foundry-rg"
  location = var.location
}

# -------------------------------------------------------------
# 2. Azure AI Foundry Workspace (Foundry Resource)
# -------------------------------------------------------------
resource "azapi_resource" "foundry" {
  type      = "Microsoft.CognitiveServices/accounts@2025-06-01"
  name                = "terraform-foundry"
  parent_id = azapi_resource.rg.id
  location            = var.location
  schema_validation_enabled = false

  body = {
    kind = "AIServices"
    sku= {
      name = "S0"
    }
    identity = {
      type = "SystemAssigned"
    }

    properties = {
        disableLocalAuth = false
        allowProjectManagement = true
        customSubDomainName = "terraformsubdomain"
    }
  }
}

# -------------------------------------------------------------
# 3. AI Foundry Project
# -------------------------------------------------------------
resource "azapi_resource" "project" {
    type = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
    name = "terraform-foundry-project"
    parent_id = azapi_resource.foundry.id
    location = var.location
    schema_validation_enabled = false

    body = {
        sku = {
            name = "S0"
        }
        identity = {
            type = "SystemAssigned"
        }
        properties = {
            displayName = "terraformproject"
            description = "AI Foundry Project deployed by Terraform"
        }
    }
}

# -------------------------------------------------------------
# 4. Deploy a model 
# -------------------------------------------------------------
resource "azapi_resource" "model" {
    type = "Microsoft.CognitiveServices/accounts/deployments@2023-05-01"
    name = "gpt-4o"
    parent_id = azapi_resource.foundry.id
    depends_on = [azapi_resource.foundry]

    body= {
        sku = {
            name = "DataZoneStandard"
            capacity = 1
        }
        properties = {
            model = {
                format = "OpenAI"
                name = "gpt-4o"
                version = "2024-11-20"
            }
        }
    }
}
