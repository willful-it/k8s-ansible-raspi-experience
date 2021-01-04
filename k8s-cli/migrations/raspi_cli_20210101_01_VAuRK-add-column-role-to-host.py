"""
Add column role to Host
"""

from yoyo import step

__depends__ = {}

steps = [
    step("ALTER TABLE Host ADD COLUMN role TEXT")
]
