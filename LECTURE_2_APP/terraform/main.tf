provider "azurerm" {
  features {}
  subscription_id = "9e01d033-be6a-400c-91a9-6376a10e4f16"
}

data "azurerm_resource_group" "existing_rg" {
  name = var.resource_group_name
}

data "azurerm_cosmosdb_account" "existing_cosmosdb" {
  name                = var.cosmosdb_account_name
  resource_group_name = var.resource_group_name
}

data "azurerm_cosmosdb_sql_database" "existing_database" {
  name                = var.cosmosdb_database_name
  resource_group_name = var.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.existing_cosmosdb.name
}

resource "azurerm_service_plan" "appserviceplan" {
  name                = "${var.app_name}-asp"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_app_service" "appservice" {
  name                = var.app_name
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  app_service_plan_id = azurerm_service_plan.appserviceplan.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "COSMOSDB_ACCOUNT_NAME"    = data.azurerm_cosmosdb_account.existing_cosmosdb.name
    "COSMOSDB_DATABASE_NAME"   = data.azurerm_cosmosdb_sql_database.existing_database.name
    "COSMOSDB_URI"             = data.azurerm_cosmosdb_account.existing_cosmosdb.endpoint
    "COSMOSDB_PRIMARY_KEY"     = data.azurerm_cosmosdb_account.existing_cosmosdb.primary_key
  }
}
