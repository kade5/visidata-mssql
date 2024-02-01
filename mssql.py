from urllib.parse import urlparse

from visidata import VisiData, asyncthread, options, TableSheet, ColumnItem, vd

vd.option("mssql_driver", "ODBC Driver 18 for SQL Server", "Name of odbc driver for mssql database")


@VisiData.api
def openurl_mssql(vd, url, filetype=None):
    pyodbc = vd.importExternal("pyodbc")
    driver = options.mssql_driver
    url = urlparse(url.given)
    dbname = url.path[1:]

    connection_string = f"DRIVER={driver};SERVER={url.hostname},{url.port};DATABASE={dbname};UID={url.username};PWD={url.password}"

    connection = pyodbc.connect(connection_string)

    return MsTablesSheet(dbname + "_tables", sql=SQL(connection))


class SQL:
    def __init__(self, conn):
        self.conn = conn

    def cur(self, qstr):
        cur = self.conn.cursor()
        cur.execute(qstr)
        return cur


class MsTablesSheet(TableSheet):
    rowtype = "tables"

    def loader(self):
        qstr = """
        SELECT
          TABLE_SCHEMA,
          TABLE_NAME,
          TABLE_TYPE
        FROM
        INFORMATION_SCHEMA.TABLES;
        """
        columns = ["Schema", "Name", "Type"]

        with self.sql.cur(qstr) as cur:
            self.rows = []

            for i, col in enumerate(columns):
                self.addColumn(ColumnItem(col, i, type=str))

            for r in cur:
                self.addRows([r])
                # self.addRow([r.TABLE_SCHEMA, r.TABLE_NAME, r.TABLE_TYPE])

    def openRow(self, row):

        table_name = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"
        source = f"[{row.TABLE_SCHEMA}].[{row.TABLE_NAME}]"

        return MsTable(table_name, source=source, sql=self.sql)

class MsTable(TableSheet):
    @asyncthread
    def reload(self):
        source = f"{self.source}"

        qsql = f"""
        SELECT *
        FROM {source}
        """

        with self.sql.cur(qsql) as cur:
            self.rows = []

            cols = cur.description

            for i, col in enumerate(cols):
                self.addColumn(ColumnItem(col[0], i, type=col[1]))

            for r in cur:
                self.addRows([r])
