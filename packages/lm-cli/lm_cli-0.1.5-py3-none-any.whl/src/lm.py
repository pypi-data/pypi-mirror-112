import configparser
import os
from pathlib import Path

import click
import pkg_resources

from src.client import vendor, RestClient

HOME_DIR = Path.home()
LM_PROXY_URL = "https://license-dkube.com"


@click.group(name="lm")
@click.pass_context
def lm_cli(ctx):
    """
    Cli for lm proxy
    """
    ctx.obj = {}
    if not os.path.exists("%s/.lm.ini" % HOME_DIR) and (
        ctx.invoked_subcommand != "login"
    ):
        raise click.ClickException(message="Please login before you use cli")
    if ctx.invoked_subcommand in ["login", "logout"]:
        return
    ctx.obj.update(rc=RestClient())


@lm_cli.command()
@click.option("-v", "--vendor_name", required=True, help="name of vendor")
@click.option("-e", "--email", required=True, help="vendor's email address")
@click.pass_context
def create_vendor(ctx, vendor_name, email):
    rc = ctx.obj["rc"]
    req = {"name": vendor_name, "email": email}
    rc.post(rc.url + "/partners", req, table=vendor)


@lm_cli.command()
@click.option("-v", "--vendor_name", required=True, help="name")
@click.pass_context
def get_customers_of_a_vendor(ctx, vendor_name):
    rc = ctx.obj["rc"]
    rc.get(rc.url + "/licenses/partners/%s" % vendor_name)


@lm_cli.command()
@click.option("-c", "--customer_name", required=True, help="name of customer")
@click.option(
    "-e", "--customer_email", required=True, help="customer's email address"
)
@click.option("-vn", "--vendor", required=True, help="vendor name")
@click.option("-vi", "--vendor_id", default=None, help="vendor id")
@click.option(
    "-ve",
    "--vendor_email",
    required=True,
    help="vendor's email address",
)
@click.option(
    "-su",
    "--subscription",
    default=None,
    help="subscription period of dkube license eg. '1y' for 1 "
    "year, '1m' for 1 month, '1w' for 1 week",
)
@click.option(
    "-q", "--quota", default=None, type=int, help="no of users " "quota"
)
@click.option(
    "-si", "--sites", default=None, type=int, help="no of dkube " "sites"
)
@click.pass_context
def create_customer(
    ctx,
    customer_name,
    customer_email,
    vendor,
    vendor_id,
    vendor_email,
    subscription,
    quota,
    sites,
):
    rc = ctx.obj["rc"]
    licenses = format_license_input(subscription, quota, sites)
    req = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "vendor": vendor,
        "vendor_email": vendor_email,
        "vendor_id": vendor_id,
        "licenses": licenses,
    }
    if not vendor_id:
        req.pop("vendor_id")
    rc.post(rc.url + "/customers", req)


@lm_cli.command()
@click.option("-n", "--name", required=True, help="name of the customer")
@click.pass_context
def get_customer_licenses(ctx, name):
    rc = ctx.obj["rc"]
    rc.get_customers_licenses(rc.url + "/licenses/%s" % name)


@lm_cli.command()
@click.option("--id", "_id", required=True, help="name of the customer")
@click.pass_context
def get_customer_licenses_by_id(ctx, _id):
    rc = ctx.obj["rc"]
    rc.get_customers_licenses(rc.url + "/licenses/customers/%s" % _id)


@lm_cli.command()
@click.option("-v", "--vendor_id", required=True, help="Vendor Id")
@click.pass_context
def delete_vendor(ctx, vendor_id):
    rc = ctx.obj["rc"]
    rc.delete(rc.url + "/partners/%s" % vendor_id)


@lm_cli.command()
@click.option("-c", "--customer_id", required=True, help="Customer Id")
@click.pass_context
def delete_customer(ctx, customer_id):
    rc = ctx.obj["rc"]
    rc.delete(rc.url + "/customers/%s" % customer_id)


@lm_cli.command()
@click.pass_context
def list_customers(ctx):
    rc = ctx.obj["rc"]
    rc.get(rc.url + "/customers")


@lm_cli.command()
@click.pass_context
def list_vendors(ctx):
    rc = ctx.obj["rc"]
    rc.get(rc.url + "/partners", table=vendor)


@lm_cli.command()
@click.option("--id", "_id", required=True, help="Customer Id")
@click.pass_context
def get_customer(ctx, _id):
    rc = ctx.obj["rc"]
    rc.get(rc.url + "/customers/%s" % _id)


@lm_cli.command()
@click.option("-s", "--session_id", required=True, help="Session Id")
@click.option("-c", "--customer_id", help="Customer Id")
@click.pass_context
def clear_session(ctx, session_id, customer_id):
    req = {}
    rc = ctx.obj["rc"]
    if customer_id:
        req = {"customer_id": customer_id}
    rc.post(rc.url + "/licenses/clear/%s" % session_id, req, table=None)


@lm_cli.command()
@click.option("-c", "--customer_id", required=True, help="Customer Id")
@click.option(
    "-su",
    "--subscription",
    default=None,
    help="subscription period of dkube license eg. '1y' for 1 "
    "year, '1m' for 1 month, '1w' for 1 week",
)
@click.option(
    "-q", "--quota", default=None, type=int, help="no of users " "quota"
)
@click.option(
    "-si", "--sites", default=None, type=int, help="no of dkube " "sites"
)
@click.pass_context
def update_license(ctx, customer_id, subscription, quota, sites):
    rc = ctx.obj["rc"]
    _license = format_update_license(subscription, quota, sites)
    rc.update_lic(rc.url + "/customers/%s/license" % customer_id, _license)


@lm_cli.command()
def login():
    _license = click.prompt("Please enter your license")
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"URL": LM_PROXY_URL, "Token": _license}
    cfg = open("%s/.lm.ini" % HOME_DIR, "w")
    config.write(cfg)
    cfg.close()


@lm_cli.command()
def logout():
    click.confirm("Do you want to logout ?", abort=True)
    if not os.path.exists("%s/.lm.ini" % HOME_DIR):
        return
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"URL": LM_PROXY_URL}
    cfg = open("%s/.lm.ini" % HOME_DIR, "w")
    config.write(cfg)
    cfg.close()


@lm_cli.command()
def version():
    _version = pkg_resources.require("lm-cli")[0].version
    print(_version)


def format_update_license(subscription, quota, sites):
    _license = dict()
    if subscription:
        _license.update(subscription=subscription)
    if quota:
        _license.update(quota=quota)
    if sites:
        _license.update(sites=sites)
    return _license


def format_license_input(subscription, quota, sites):
    licenses, lic = [], {}
    if subscription:
        lic["subscription"] = {"time": subscription}
    if quota:
        lic["quota"] = {"users": quota}
    if sites:
        lic["multisite"] = {"sites": sites}
    licenses.append(lic)
    return licenses
