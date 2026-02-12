from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
    FREELANCER = "FREELANCER"
    USER = "USER"
