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

# Changes
Version | Description
--------|------------
0.0.2   | Fixed plugin imports
0.0.1   | Initial