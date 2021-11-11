# PyPorta - Python library for Portaone Softswitch API 
PyPorta is a python library of functions to consume [PortaOne PortaSwitch](https://www.portaone.com/) APIs.

## Requirements :

### Python version:
```
Python 3 or higher
```

### Extensions required :
```
requests
json
os.path
```

## How to

To get access to Portaone API an authenticated to the server and get session-ID to be used on the API requests.

Example :

```
import pyporta

MyPO = pyporta.PortaServer('myportaserver.local','myportauser','myportapass')
MyPO.Connect()
```

### Available functions

- Connect : Connects on PortaSwitch API Server
- GetAccountList : Get a list of accounts from a customer;
- GetAccountInfo : Get information from a customer account;
- AddAccountSipInfo : Set SIP contact information on a customer account;
- AddAccount : Add a customer account
- AddCustomer : Add a customer
- SetCustomerTrafficLimit : Set customer traffic profile;
- SetCustomField  :  Set a customer custom field ;  
- GetCustomerInfo : Get customer information;
- GetCustomerNameFromAccount : Get customer own from passing an account as parameter;
- GetTrafficProfile : Get customer traffic profile ID applied;
- GetTrafficProfileName : Get traffic profile name;
- GetCustomerI : Get customer ID;
- GetCustomField : Get values from a customer custom field;
- GetCustomerList : Get customer list from the DB;
- GetTrafficProfileList :  Get traffic profile list from the DB;
- GetCustomerClassList : Get customer class list from the DB;
- GetSessionList : Get active sessions list in the server;
- GetCallList : Get active call list in the server;
- GetXDRSList : Get call's XDRs list from a customer ;
- GetAccXDRSList : Get call's XDRs list from a customer account;
- RevertXDRS : Revert call XDRs;
- GetServiceFeatures : Get service feature from a customer;
- GetAccountsfromCustomer :  Get list of accounts from customer;
- GetCustomersfromReseller : Get a list customer from a reseller;