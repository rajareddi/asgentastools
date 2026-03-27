"""
Setup configuration for A2A Communication Package
"""

from setuptools import setup, find_packages

with open("a2a_package/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="a2a-communication",
    version="1.0.0",
    author="Agent Development Team",
    description="Agent-to-Agent Communication Protocol for OpenAI Agents Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rajareddi/asgentastools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "openai>=2.26.0",
        "openai-agents>=0.13.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)

