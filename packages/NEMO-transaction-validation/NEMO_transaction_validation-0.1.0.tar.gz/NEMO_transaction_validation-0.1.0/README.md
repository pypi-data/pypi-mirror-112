This NEMO plugin is inspired from the transaction validation features implemented by Penn State's LEO.

# Description
This plugin allows staff members to validate and contest transactions performed on behalf of a customer. Once contests are reviewed and approved by an administrator, the plugin automatically revises the transaction according to the contest submission. The plugin also saves a copy of the original transaction data as a contest item for historical data.

A transaction can be validated if no contests are required. Else, if contests have been submitted for approval, then it can be validated once all contests are approved by the administrator.

# Installation
1. Install plugin.
```
pip install NEMO-transaction-validation
```

2. Add the plugin to `INSTALLED_APPS` in your `settings.py` file.
```
INSTALLED_APPS = [
    ...
    'NEMO_transaction_validation', #must be placed before 'NEMO'
    'NEMO',
    ...
]
```

3. Add the function `auto_validate_transactions` to the list of cron tasks. For this example, transactions at least five days old are checked and validated every 5 minutes.
```
sudo crontab -e

---> In the root crontab <---
...
*/5 * * * * /snap/bin/docker exec nemo django-admin auto_validate_transactions

```

**N.B.:** Ensure that there is a newline at the end of the crontab file

Let's breakdown the crontab line that was added:  
`*/5 * * * *` Time and date fields  
`/snap/bin/docker` Path to the docker executable file. You may omit this if the docker executable file has already been included in your `PATH` variable. Otherwise, you will need to provide the directory path to the executable file.  
`exec` In the following container, execute the following command  
`nemo` Name of the docker container  
`django-admin auto_validate_transactions` Custom django-admin command

# Changes
Version | Description
--------|------------
0.1.0   | Cron job added by using system crontab instead of django packages
0.0.4   | Fixed plugin import error in cron function
0.0.3   | Added cron job function for auto validating transactions every 5 minutes
0.0.2   | Fixed plugin imports
0.0.1   | Initial