from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sqlglot import parse_one, exp

class _QuerySQLSecurityCheckerToolInput(BaseModel):
    query: str = Field(..., description="A detailed and SQL query to be checked.")

class QuerySQLSecurityCheckerTool(BaseTool):
    name: str = "sql_db_security_checker"
    description: str = """
    Use a sqlglot to check if a query is secure. Use this tool to make a security check.
    Always use this tool before executing a query with sql_db_query!
    """
    args_schema: Type[BaseModel] = _QuerySQLSecurityCheckerToolInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        expression = parse_one(query)
        if not any([list(expression.find_all(item)) for item in [exp.Delete, exp.Insert, exp.Update, exp.Drop]]):
            return f'Secure, you could execute {query}!'
        return f'ERROR!!! DO NOT EXECUTE {query}!!!'

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        return self.run(query, run_manager.get_sync())

def test_run_negative():
    tool = QuerySQLSecurityCheckerTool()
    assert 'ERROR' in tool._run('DROP TABLE Artists', None)
    
def test_run_positive():
    tool = QuerySQLSecurityCheckerTool()
    assert 'ERROR' not in tool._run('SELECT * FROM Artists LIMIT 10', None)
