# visidata-mssql
A visidata plugin to add MS SQL Server support to visidata.

## Requirements
Requires pyodbc python package and ODBC Driver for SQL server.

For pyodbc check your distribution's package manager or pip install into local python environment where you have visidata installed.

[ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) is recommended. 

## Installation
```bash
mkdir -p ~/.visidata/plugins
cd ~/.visidata/plugins
wget https://raw.githubusercontent.com/kade5/visidata-mssql/main/mssql.py
```

Add the following code to ~/.visidatarc

```python
import plugins.mssql
```

## Usage
Currently only supports sql server login with username and password.

To start
```bash
visidata mssql://username:password@hostname:port/database
```

## Other
If you need to use another ODBC driver set it as an option under the name mssql_driver. Defaults to ODBC Driver 18 for SQL Server.
