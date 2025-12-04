# Fullstack Nextjs-Langgraph Agent
> **A production-ready Next.js template for building AI agents with LangGraph.js, featuring Model Context Protocol (MCP) integration, human-in-the-loop tool approval, and persistent memory.**


Complete agent workflow: user input → tool approval → execution → streaming response

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-16.0.5-black?logo=nextdotjs)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph.js-1-green?logo=langchain)](https://langchain-ai.github.io/langgraphjs/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-blue?logo=postgresql)](https://www.postgresql.org/)
[![Prisma](https://img.shields.io/badge/Prisma-6-2D3748?logo=prisma)](https://www.prisma.io/)

## Features 

### **Dynamic Tool Loading with MCP**
- Integrated Model Context Protocol for flexible, on-demand tool handling

- Add new tools directly through the web interface — no source-code updates needed

- Works with both HTTP-based and stdio MCP servers

- Automatic tool-name prefixing to avoid naming collisions

### **Human-in-the-Loop Tool Approval**

- Interactive confirmation before any tool is run  
- Fine-grained control with approve, reject, or edit actions  
- Optional automatic approval mode for trusted setups  
- Real-time streaming output with pauses at tool-call checkpoints  

<!-- <div align="center">
  <img src="docs/images/tool-approval.png" alt="Tool Approval Dialog" width="600" />
  <p><em>A tool-approval interface showing detailed parameter review</em></p>
</div> -->

### **Persistent Conversation Memory**

- LangGraph checkpointer backed by PostgreSQL for durable state  
- Full preservation of all dialogue context  
- Thread-structured organization for clean history management  
- Smooth session continuation without losing progr

### **Real-time Streaming Interface**

- Live updates delivered through Server-Sent Events (SSE)  
- Optimistic UI rendering powered by React Query  
- Strongly typed message flow for safe communication  
- Built-in error handling with smooth fallback behavior  

### **Modern Tech Stack**

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS  
- **Backend**: Node.js, Prisma ORM, PostgreSQL  
- **AI**: LangGraph.js, OpenAI/Google model integrations  
- **UI**: shadcn/ui component library and Lucide icon set

## Quick Start

### Prerequisites

- Node.js 20+ and pnpm
- Docker Compose (for PostgreSQL)
- OpenAI API key or Google AI API key

### 1. Clone and Install

```bash
git clone https://github.com/Khim3/fullstack_nextjs_ai_agent.git
cd fullstack_nextjs_ai_agent
pnpm install
```

### 2. Environment Setup

```bash
touch .env
```
Fill in the `.env` file with your configuration:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api/agent
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
DATABASE_URL="postgresql://user:password@localhost:5432/yourdb"
OPENAI_API_KEY="your-openai-api-key"
# or for Google AI
GOOGLE_API_KEY="your-google-api-key"
```
### 3. Start Database Service

```bash
docker compose up -d
```

### 4. Database Setup

```bash
pnpm prisma:generate
pnpm prisma:migrate
```

### 5. Run Development Server

```bash
pnpm dev
```
Use browser to navigate to `http://localhost:3000` and start interacting with the AI agent!

### 6. Customize your mcp tools via Python server.py
To start the MCP server, run:

```bash
python server.py
```

Feel free to modify the `server.py` file to add or change MCP tools as needed. Restart the server after making changes. Or you could build your own MCP server in any language you prefer!

## Usage Guide

### Adding MCP Servers

1. **Open Settings** — Click the gear icon in the sidebar  
2. **Create a New MCP Server** — Select **"Add MCP Server"**  
3. **Fill in Server Details**:  
   - **Name**: A unique label for the server (e.g., `"filesystem"`)  
   - **Type**: Select either `stdio` or `http`  
   - **Command**: Used for stdio-based servers (e.g., `npx @modelcontextprotocol/server-filesystem`)  
   - **Args**: Provide any required arguments (e.g., `["/path/to/allow"]`)  
   - **URL**: Specify when using an HTTP-based MCP server  

![Add MCP Server](docs/images/add-mcp-server.png)  
*Example configuration screen for setting up a filesystem-based MCP server.*

### Example MCP Server Configurations

#### Filesystem Server (stdio)

```json
{
  "name": "filesystem",
  "type": "stdio",
  "command": "npx",
  "args": ["@modelcontextprotocol/server-filesystem", "/Users/yourname/Documents"]
}
```

#### HTTP API Server

```json
{
  "name": "some web service",
  "type": "http",
  "url": "http://localhost:8080/mcp",
  "headers": {
    "Authorization": "Bearer your-token"
  }
}
```

### Tool Approval Workflow

1. **Agent Requests Tool** - AI suggests using a tool
2. **Approval Prompt** - Interface shows tool details and asks for approval
3. **User Decision**:
   - ✅ **Allow**: Execute tool as requested
   - ❌ **Deny**: Skip tool execution
   - ✏️ **Modify**: Edit tool parameters before execution
4. **Continue Conversation** - Agent responds with tool results

## Architecture

### High-Level Overview

Next.js UI (React 19)
        ↓
Agent Service (SSE streaming API)
        ↓
LangGraph.js Agent
        ↓
────────────────────────────────────────
• React Query (client-side state)
• Prisma ORM (data access)
• MCP Tool Clients (external tools)
────────────────────────────────────────
        ↓
PostgreSQL (persistent storage)

### Core Elements

#### Agent Builder (`src/lib/agent/builder.ts`)

- Constructs the StateGraph with the agent → tool_approval → tools execution pipeline  
- Manages interruption points for tool approval  
- Configures model bindings and global system instructions  

#### MCP Integration (`src/lib/agent/mcp.ts`)

- Loads tools dynamically based on MCP server entries stored in the database  
- Works with both stdio-based and HTTP-based MCP transports  
- Applies name-spacing to avoid tool naming collisions  

#### Streaming Service (`src/services/agentService.ts`)

- Uses Server-Sent Events to deliver live agent responses  
- Processes incoming chunks and assembles complete messages  
- Coordinates the tool-approval pause/resume flow  

#### Chat Hook (`src/hooks/useChatThread.ts`)

- Integrates with React Query for optimistic UI updates  
- Manages message streams and error recovery  
- Provides the UI layer for tool approval interactions  

### Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── api/            # API routes
│   └── thread/         # Thread-specific pages
├── components/         # React components
├── hooks/              # Custom React hooks
├── lib/                # Core utilities
│   └── agent/          # Agent-related logic
├── services/           # Business logic
└── types/              # TypeScript definitions

prisma/
├── schema.prisma       # Database schema
└── migrations/         # Database migrations
server.py              # Example MCP server implementation
README.md              # Project documentation
```

### Key Files

- **Agent Configuration**: `src/lib/agent/builder.ts`, `src/lib/agent/mcp.ts`
- **API Endpoints**: `src/app/api/agent/stream/route.ts`
- **Database Models**: `prisma/schema.prisma`
- **Main Chat Interface**: `src/components/Thread.tsx`
- **Streaming Logic**: `src/hooks/useChatThread.ts`

## Acknowledgments
This project was inspired by and built upon the following amazing open-source projects:
- https://github.com/IBJunior/fullstack-langgraph-nextjs-agent/

- [LangChain](https://github.com/langchain-ai) for the incredible AI framework
- [LangGraph.js](https://langchain-ai.github.io/langgraphjs/) for the powerful agent-building library
- [Model Context Protocol](https://modelcontextprotocol.io/) for the tool integration standard
- [Next.js](https://nextjs.org/) team for the amazing React framework
- Prisma and PostgreSQL communities for the robust database solutions.


---