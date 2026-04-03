from __future__ import annotations

import os
from typing import Final

__version__: Final[str] = os.getenv("INKNOTE_VERSION", "0.0.0-dev")
