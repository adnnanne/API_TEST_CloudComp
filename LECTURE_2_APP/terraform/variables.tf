variable "app_name" {
  description = "Name of the App Service"
  default     = "httpcclectureapi"
}

variable "location" {
  description = "Azure region"
  default     = "France Central"
}

variable "resource_group_name" {
  description = "Name of the existing resource group"
  default     = "lec2dbcmdrg"
}

variable "cosmosdb_account_name" {
  description = "Existing Cosmos DB account name"
  default = "lec2dbcmdcosmosdbacc"
}

variable "cosmosdb_database_name" {
  description = "Existing Cosmos DB database name"
  default = "lec2dbcmdcosmosdbdatabase"
}

variable "cosmosdb_container_name" {
  description = "Existing Cosmos DB container name"
  default     = "lec2dbcmdcosmosdbcontainer"
}