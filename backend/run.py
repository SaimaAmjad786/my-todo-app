#!/usr/bin/env python
"""Backend runner script that properly configures the environment."""
import os
import uvicorn

# Change to backend directory so .env is loaded correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")],
    )
