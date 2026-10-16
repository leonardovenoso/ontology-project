from sqlalchemy.orm import Session
from models.staff import Staff
from models.diagnosis import Diagnosis
from langchain.tools import tool, ToolRuntime
from langchain_core.tools import BaseTool
from actions.find_diagnosis_action import find_diagnosis

class DoctorToolsContext:
  def __init__(self, caller: Staff, db_session: Session, mrn: str):
    self.caller = caller
    self.db_session = db_session
    self.mrn = mrn


@tool(description="This tool is to fetch patient's diagnosis")
def get_diagnosis_list(runtime: ToolRuntime[DoctorToolsContext]) -> list[Diagnosis]:
  return find_diagnosis(mrn=runtime.context.mrn, staff=runtime.context.caller, db_session=runtime.context.db_session)


@tool(description="This tool is to discover hidden disease patterns in the diagnosis")
def get_ai_hidden_disease_patterns(runtime: ToolRuntime[DoctorToolsContext]) -> str:
  return ""


@tool(description="This tool gets an AI based diagnosis for one specific disease")
def get_ai_diagnosis(runtime: ToolRuntime[DoctorToolsContext]) -> str:
  return ""


@tool(description="This tool gets citation links from pubmed")
def get_pub_med_citations(runtime: ToolRuntime) -> list[str]:
  return []


TOOLS_BY_ROLE: dict[str, list[BaseTool]]  = {
  "doctor": [get_diagnosis_list, get_ai_hidden_disease_patterns, get_ai_diagnosis, get_pub_med_citations]
}

def build_tools(caller: Staff) -> list[BaseTool]:
  tools = TOOLS_BY_ROLE.get(caller.role)
  if tools is None:
    raise PermissionError("Invalid role")
  return tools