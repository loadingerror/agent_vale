from langchain_core.tools import BaseToolkit, BaseTool
from .check_weather import check_weather
from langchain_community.tools import DuckDuckGoSearchResults
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_core.language_models import BaseChatModel
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from .check_sql_query import QuerySQLSecurityCheckerTool
import requests
import sqlite3

def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

class AIToolKit(BaseToolkit):
    llm: BaseChatModel

    def get_tools(self) -> list[BaseTool]:
        sqltoolkit = SQLDatabaseToolkit(db=SQLDatabase(get_engine_for_chinook_db()), llm=self.llm)
        return sqltoolkit.get_tools() + [check_weather, DuckDuckGoSearchResults(), QuerySQLSecurityCheckerTool()]

    @classmethod
    def from_llm(cls, llm):
        return cls(llm=llm)