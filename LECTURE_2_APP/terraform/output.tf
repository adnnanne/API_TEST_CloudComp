output "app_service_url" {
  value = azurerm_app_service.appservice.default_site_hostname
}
