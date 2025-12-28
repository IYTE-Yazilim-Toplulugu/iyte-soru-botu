I wanna create issues for my team members on this repository.
https://github.com/orgs/IYTE-Yazilim-Toplulugu/projects/22 is the project of this repo. There is no issues yet
You should examine the codebase and understand the missing parts
You should add this tasks with creating issues properly. You can separate tasks if they sizes are huge:
- Add missing authentication use cases
- Use global exception handling on auth, chat, document for error handling (you can check auth service exception_handler.py for that. Use separate tasks for each service)
- Database connections in infrastructure layer. (you can separate service based tasks, use docker not host locally)
- Auth service entity relationships enhancement (there should be other tables for verification/reset tokens etc. we are keeping them on users table for now)
- Chat service agentic workflow with rag service for answer the questions specifically for past exam questions (you should separate task to multiple issues):
  - Use langchain with langgraph for create a agentic workflow. Use OOP standarts. You can use an orchestrator (decision router), guardrails, etic agent, quiz creater
agent, past exam agent, general knowledge agent etc. You can use clusters for some specific scopes. There should be some tools for reach to document service with gRPC,
search knowledge base in vector_db, search on internet, update user persona, memory etc.
- Mapper integrations with generic IMapper interface from shared-kernel (you can check user_mapper.py from auth service application layer
- Add missing use cases on chat service:
  - Paginated data for queries (you should use shared-kernel pagination models
  - Add missing dtos (omitted domain entities)
- Add gRPC server on document service for chat service client.
- Add redis on chat service for reach queries faster (use docker for all infrastructure. Do not host locally anything, you can check @docker-compose.yml)
- Add MinIO buckets to document service for keep documents
- Add chromadb for RAG service on chat
- Enhance auth service sercurity (advanced, explain obviously)
- Write test with pytest (separate tasks for each service, advanced)
- Add missing use cases on document service
- Use auth service file structure on chat and document service (boring refactor thus say that is advanced :) )
- I will change the gateway, but now, you can assume that there is a redis for session caching and route based authorization on gateway. Just create issue but do not give
 example code, I will handle that
- Document (pdf, image, docs etc.) parsing for understanding content. Use LLM APIs, OCR parsers, LLamaParse etc. for that (**use OOP**).
- Swagger documentation and docstrings (good for newly members)
- Document use cases, er diagrams with mermaid (good for newly ones)

Separate tasks as possible. Give steps and example codes. Do not use functional python, just use **OOP** with generic shared-kernel classes if cross services. You can add
 generic ABCs if its better. Assume that we have more than 10 people in our team, thus those tasks for just one month (due 23 Jan 2026). Keep code clean and remind the
member you should run `uv run mypy .` and `uv run ruff check --fix .` before pull requests. Use separate branches for each issues, create them on issues (do not
manually). You should indicate priority and sizes for each issues in content (there is p0(highest) p1(high) p2(medium) priorities and xs-xl sizes). Add status, roadmap,
references, acceptance criteria etc. Firstly, examine the codebase then start with the first issue
