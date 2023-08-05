<div style="text-align:center"><img alt="logo" src="https://www.zypp.io/static/assets/img/logos/zypp/white/500px.png" width="200"></div>

Notify
===
> Sending mails and teams messages in a smart way. This project makes it easy to send basic messages through Teams or Email.

# Installation

---

```commandline
pip install zyppnotify
```

## Notify Mail
When using the `NotifyMail` class, the environment variables `EMAIL_USER` and `EMAIL_PW` need to be set.
The initialization of this class will return an error if one of thes variables is not set.

```python
from notify import NotifyMail, NotifyTeams

# versturen van een basis bericht met onderwerp en tekst
mail = NotifyMail(to="reveiver@domain.com",
                  subject="Notify me!",
                  message="This is a test message, send through the notify package")

mail.send_email()
```

## Notify Teams
```python
from notify import NotifyTeams
from notify.utils import import_sample_dfs

webhook = ("REPLACE_ME")

teams = NotifyTeams(webhook=webhook)

# versturen van een basis bericht met onderwerp en tekst
teams.basic_message(title="Notify me!", 
                    message="This is a test message, send through the notify package")

# versturen van een uitgebreid rapport over dataframes.
dfs = import_sample_dfs()
teams.basic_message(title="Notify me!",
                    message="This is optional",
                    buttons={"button_name": "https://www.my_link.nl"},
                    dfs=dfs) #  creates a report on the dataframes processed.

```