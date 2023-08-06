import click
import mijn_simpel
from mijn_simpel.client import Session, Subscription
from mijn_simpel.utils import fmt_output
from os.path import expanduser

@click.group()
@click.option('--cookie-jar', default=expanduser("~") + '/.config/mijn-simpel-cookie',
              show_default='~/.config/mijn-simpel-cookie',
              help='Cookie jar for session storing.', envvar='MIJN_SIMPEL_COOKIE_JAR')
@click.option('--json/--no-json', default=False,
              help='Output in JSON', envvar='MIJN_SIMPEL_JSON_OUTPUT')
def main(cookie_jar, json):
    global json_output
    json_output = json
    global s
    s = Session(cookie_jar)
    pass

@main.command(help='Login to service.')
@click.option('--username', prompt='Mijn Simpel username',
              help='Username on mijn.simpel.nl.', envvar='MIJN_SIMPEL_USERNAME')
@click.password_option(envvar='MIJN_SIMPEL_PASSWORD',
                       help='Password on mijn.simpel.nl.')
def login(username, password):
    resp = s.login(username, password)
    if resp:
        click.echo('Logged in')

@main.command(help='List subscriptions.')
def subscriptions():
    resp = s.account_subscription_overview()
    if resp:
        click.echo(fmt_output(json_output, resp))

@main.group(help="Information for subscription.")
@click.argument('subscription-id',
              envvar='MIJN_SIMPEL_SUBSCRIPTION_ID')
def subscription(subscription_id):
    global subscription
    subscription = s.subscription(subscription_id)
    pass
        
@subscription.command(help='Show dashboard.')
def dashboard():
    resp = subscription.dashboard()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show products.')
def products():
    resp = subscription.products()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show ceiling.')
def ceiling():
    resp = subscription.ceiling()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show latest invoice.')
def latest_invoice():
    resp = subscription.latest_invoice()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show correction for billing period.')
def correction_for_billing_period():
    resp = subscription.correction_for_billing_period()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show usage summary.')
def usage_summary():
    resp = subscription.usage_summary()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show other costs.')
def other_costs():
    resp = subscription.usage_other_costs()
    if resp:
        click.echo(fmt_output(json_output, resp))

@subscription.command(help='Show cdrs.')
def cdrs():
    resp = subscription.usage_cdrs()
    if resp:
        click.echo(fmt_output(json_output, resp))


if __name__ == '__main__':
    main()
