from sqlalchemy import Column, Integer, String, Float
from ..database import Base
from spacenet.schemas.node import NodeType

class Node(Base):
    __tablename__ = "Nodes"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    description = Column(String)
    body_1 = Column(String)

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "node"}


class SurfaceNode(Node):
    latitude = Column(Float)
    longitude = Column(Float)

    __mapper_args__ = {"polymorphic_identity": NodeType.Surface.value}


class OrbitalNode(Node):
    apoapsis = Column(Float)
    periapsis = Column(Float)
    inclination = Column(Float)

    __mapper_args__ = {"polymorphic_identity": NodeType.Orbital.value}


class LagrangeNode(Node):
    body_2 = Column(String)
    lp_number = Column(Integer)

    __mapper_args__ = {"polymorphic_identity": NodeType.Lagrange.value}
