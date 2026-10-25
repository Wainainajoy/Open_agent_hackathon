# County Policy & Budget Analyst

## Overview
The County Policy & Budget Analyst is a sophisticated multi-agent system designed to bridge the gap between local government operations and citizen access to information. Deployed on Google Cloud's Vertex AI Agent Engine, this system leverages the Google Agent Development Kit (ADK) to provide intelligent, accessible insights into county policies, budgets, and services.

## Core Features
- **Document Intelligence**: Indexes and analyzes local government documents using Model Context Protocol (MCP)
- **Multi-Agent Coordination**: Utilizes Agent-to-Agent (A2A) protocol for specialized task handling
- **Smart Information Retrieval**: Provides rapid, concise, and fully-cited summaries
- **Geographic Context Awareness**: Integrates location-based services for region-specific information
- **Policy Translation**: Converts complex government language into citizen-friendly explanations

## Architecture

### Agent Components
1. **ADK MCP Server** (`adk_mcp_tools/adk_mcp_server/`)
   - Core server implementation
   - Handles document indexing and retrieval
   - Manages agent coordination

2. **Google Maps Integration** (`adk_mcp_tools/google_maps_mcp_agent/`)
   - Provides location-based context
   - Maps service locations and jurisdictions

3. **Nyeri Information Agent** (`google_search_on_nyeri_agent/`)
   - Specialized agent for Nyeri County information
   - Handles region-specific queries and data

## Technical Stack
- **Platform**: Google Vertex AI Agent Engine
- **Framework**: Google Agent Development Kit (ADK)
- **Protocols**: 
  - Model Context Protocol (MCP) for document processing
  - Agent-to-Agent (A2A) Protocol for inter-agent communication
- **Language**: Python

## Setup and Installation

### Prerequisites
- Python 3.8+
- Google Cloud account with Vertex AI access
- ADK CLI tools

### Installation Steps
1. Clone the repository
2. Install dependencies:
   ```bash
   cd adk_mcp_tools
   pip install -r requirements.txt
   ```
3. Configure Google Cloud credentials
4. Start the MCP server:
   ```bash
   cd adk_mcp_server
   python adk_server.py
   ```

## Usage
The system provides various interfaces for accessing county information:

1. **Policy Queries**
   - Request summaries of specific policies
   - Get updates on policy changes
   - Access historical policy information

2. **Budget Analysis**
   - View budget allocations by department
   - Track spending patterns
   - Compare year-over-year changes

3. **Service Information**
   - Locate county services
   - Understanding service requirements
   - Access service delivery metrics

## Contributing
We welcome contributions to improve the system's capabilities:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description of changes




