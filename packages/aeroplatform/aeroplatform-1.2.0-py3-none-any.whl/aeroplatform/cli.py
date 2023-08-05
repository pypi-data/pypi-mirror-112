import click
import time
import os
import logging
import sys

from .version import __version__
from .account import Account, ComputeStatus

logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOGLEVEL', 'INFO').upper())

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

site_base = "https://site.aeroplatform.co.uk"
name_lower = "aero"
name_upper = "Aero"

def echo(line, **kwargs):
    click.secho(line, **kwargs)

def cyan(string):
    return click.style(string, fg='cyan')

def magenta(string):
    return click.style(string, fg='magenta')

def red(string):
    return click.style(string, fg='red')

@click.group()
def cli():
    echo(f'{magenta(name_upper + " Platform")} {magenta("v" + __version__)}')
    echo("A Data Platform designed to put developers first.")
    echo(f"For more information, visit {cyan(site_base)}")
    echo("")
    pass

@cli.group(help="Account management")
def account():
    pass

@account.command(help="Login to an account")
@click.option("--email", default=None,
    help="Email address")
@click.option("--password", default=None,
    help="Password")
def login(password, email):

    if not email and not password:
        email = click.prompt("Email > ")
        password = click.prompt("Password > ", hide_input=True)

    try:
        account = Account(email, password)
        _login(account)
    except Exception as e:
        raise e
        echo("An error occured when attempting to log in, please try again")
        logger.debug(e)
        return

    try:
        _provision(account)

    except Exception as e:
        echo("An error occured when attempting to provision, please try again")
        logger.debug(e)

    return

@account.command(help="Create an account")
def create():

    echo(f'Welcome to {magenta(name_upper)}!')
    echo(f'Please create an account from our website, {site_base}.')

    return


def _login(account):

    try:
        account.login()
    except Exception as e:

        if str(e) == "403":
            echo(f'{red("Error: ")} Incorrect email/password')
            raise e
        elif str(e) == "404":
            echo(f'{red("Error: ")} User doesnt exist')
            raise e
        else:
            echo("An error has occurred")
            raise e
    
    echo(f'{cyan("Login Successful")}')

def _provision(account):

    status = ComputeStatus.NO_VALUE
    i = 0
    is_first_provision = False

    while status != ComputeStatus.CREATED:
        status = account.provision(is_first_provision)
        logger.debug(f"Current Status is {status}, iteration {i}")

        if status == ComputeStatus.INIT:
            echo(f"Initialised Compute Environment Creation")
            is_first_provision = True

        if status == ComputeStatus.CREATING:
            echo(f"Creating Compute Environment...")   
            is_first_provision = True

        if status == ComputeStatus.CREATED:
            echo(f"Compute Environment Created")
            echo(f"You are now ready to run Flows with Aero. For some basic tutorials, visit: {site_base}/commands")
            break  

        time.sleep(30)
        i += 1
