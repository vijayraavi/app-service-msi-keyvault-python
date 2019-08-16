from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials
from azure.keyvault import KeyVaultClient
import os

from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class KVForm(FlaskForm):
    keyVaultName = StringField('Key Vault Name', validators=[DataRequired()])
    secretName = StringField('Secret Name', validators=[DataRequired()])
    submit = SubmitField('Get My Secret')

def get_key_vault_credentials():
    """This tries to get a token using MSI, or fallback to SP env variables.
    """
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource='https://vault.azure.net'
        )
    else:
        return ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID'],
            resource='https://vault.azure.net'
        )


def run_example(key_vault_name, secret_name):
    """MSI Authentication example."""

    # Get credentials
    credentials = get_key_vault_credentials()

    # Create a KeyVault client
    key_vault_client = KeyVaultClient(
        credentials
    )

    # Construct the vault uri
    key_vault_uri = "https://" + key_vault_name + ".vault.azure.net/"

    secret = key_vault_client.get_secret(
        key_vault_uri,  # Your KeyVault URI
        secret_name,       # Name of your secret.
        ""              # The version of the secret. Empty string for latest
    )
    return secret.value


@app.route('/', methods = ['POST', 'GET'])
def default_page():
    try:
        form = KVForm()
        if form.validate_on_submit():
            secret = run_example(form.keyVaultName.data, form.secretName.data)
            return render_template('secret_found.html', title='Secret Found', secret=secret, keyVaultName=form.keyVaultName.data, secretName=form.secretName.data)
        return render_template('submit_secret.html', title='Submit Secret Info', form=form)

    except Exception as err:
        return str(err)


if __name__ == '__main__':
    app.run()
