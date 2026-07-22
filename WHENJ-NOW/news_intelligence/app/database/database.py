import os
import socket
from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def _resolve_host_ipv4_preferred(database_url: str) -> str:
    """
    Resolve the database hostname preferring IPv4 (AF_INET).
    Falls back to IPv6 (AF_INET6) if no IPv4 address is available.
    Returns the resolved IP address string.
    """
    parsed = urlparse(database_url)
    hostname = parsed.hostname
    port = parsed.port or 5432

    # Try IPv4 first
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            results = socket.getaddrinfo(hostname, port, family, socket.SOCK_STREAM)
            if results:
                resolved_ip = results[0][4][0]
                return resolved_ip
        except socket.gaierror:
            continue

    # Final fallback — let psycopg3 resolve it itself
    return hostname


# Resolve once at startup so every connection uses the same resolved IP
_resolved_hostaddr = _resolve_host_ipv4_preferred(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        # hostaddr bypasses further DNS lookups in psycopg3/libpq.
        # The 'host' in the URL is still used for SSL certificate verification.
        "hostaddr": _resolved_hostaddr,
    }
)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()
