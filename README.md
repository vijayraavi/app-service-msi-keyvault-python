# App Service on Linux using Python to Access Key Vault

This sample python application is meant to demonstrate the ability to retrieve a secret from Azure Key Vault from an App Service on Linux Web App that has a Managed Identity configured.

## Prerequisites

This sample python application is meant to be used in tandem with the Pluralsight course *Managing and Configuring Microsoft Azure Key Vault*.  The process for creating the necessary components is included in the [GitHub repository for the course](https://github.com/ned1313/Configuring-and-Managing-Microsoft-Azure-Key-Vault).  You will need to create the following:

- An Azure Key Vault
- A secret within Azure Key Vault to retrieve
- An Azure Web App on Linux with Git deployment enabled and a System Assigned identity
- An access policy on the Key Vault granting the WebApp MSI *get* permissions to secrets

##  Process

Deploy the application using Git deployment to the Web App.  Browse to the Web App and fill out the form fields.  The Key Vault name should just be the name, not the full URI.  The secret name should just be the name of the secret and not the URI either.  The Web App will get a token for Key Vault using its MSI and then attempt to access the value of the secret.  It will return a page with the secret value if it is successful.