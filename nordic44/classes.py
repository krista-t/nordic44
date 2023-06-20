from pydantic import BaseModel

class ACLineSegment(BaseModel):
    """ACLineSegment pydantic class according to Nordic 44
    """
    name: str
    rdf_ID: str
    resistance: float


class Substation(BaseModel):
    """Substation pydantic class according to Nordic 44
    """
    rdf_ID: str
    region: str
    name: str