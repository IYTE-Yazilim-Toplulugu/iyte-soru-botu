.PHONY: help setup sync build clean test lint format

# Default target
.DEFAULT_GOAL := help

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo ""
	@echo "$(CYAN)IYTE Soru Botu - Makefile Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(CYAN)%-30s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Setup & Installation

setup: ## Install all dependencies (uv sync for all services)
	@echo "$(GREEN)Setting up IYTE Soru Botu...$(NC)"
	@./scripts/setup.sh

sync: ## Sync dependencies (uv sync)
	@echo "$(GREEN)Syncing dependencies...$(NC)"
	@./scripts/sync-deps.sh

install: setup ## Alias for setup

##@ Local Development (Docker)

dev-up: ## Start all services in Docker
	@echo "$(GREEN)Starting all services...$(NC)"
	@docker compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@make dev-status

dev-down: ## Stop all services
	@echo "$(GREEN)Stopping all services...$(NC)"
	@docker compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

dev-restart: ## Restart all services
	@echo "$(GREEN)Restarting all services...$(NC)"
	@docker compose restart
	@echo "$(GREEN)✓ Services restarted$(NC)"

dev-build: ## Build all Docker images
	@echo "$(GREEN)Building all images...$(NC)"
	@docker compose build
	@echo "$(GREEN)✓ Images built$(NC)"

dev-rebuild: ## Rebuild and restart all services
	@echo "$(GREEN)Rebuilding all services...$(NC)"
	@docker compose down
	@docker compose build --no-cache
	@docker compose up -d
	@echo "$(GREEN)✓ Services rebuilt and started$(NC)"

dev-logs: ## Show logs from all services (Usage: make dev-logs SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then \
		docker compose logs -f; \
	else \
		docker compose logs -f $(SERVICE); \
	fi

dev-status: ## Show status of all services
	@echo ""
	@echo "$(CYAN)Service Status:$(NC)"
	@docker compose ps
	@echo ""

dev-clean: ## Clean all containers, volumes, and images (DESTRUCTIVE!)
	@echo "$(RED)WARNING: This will remove all containers, volumes, and images!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down -v --rmi all; \
		echo "$(GREEN)✓ Cleaned up$(NC)"; \
	else \
		echo "$(YELLOW)Aborted$(NC)"; \
	fi

##@ Service-Specific Commands

auth: ## Start only auth service
	@docker compose up -d auth auth-db
	@echo "$(GREEN)✓ Auth service started$(NC)"

chat: ## Start only chat service
	@docker compose up -d chat chat-db chat-redis chromadb
	@echo "$(GREEN)✓ Chat service started$(NC)"

document: ## Start only document service
	@docker compose up -d document document-db minio
	@echo "$(GREEN)✓ Document service started$(NC)"

gateway: ## Start only gateway service
	@docker compose up -d gateway gateway-redis
	@echo "$(GREEN)✓ Gateway service started$(NC)"

##@ Database Operations

db-migrate: ## Run database migrations (Usage: make db-migrate SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then \
		echo "$(RED)Error: SERVICE required$(NC)"; \
		echo "Usage: make db-migrate SERVICE=auth"; \
		exit 1; \
	fi
	@echo "$(GREEN)Running migrations for $(SERVICE)...$(NC)"
	@docker compose exec $(SERVICE) alembic upgrade head
	@echo "$(GREEN)✓ Migrations complete$(NC)"

db-reset: ## Reset database (DESTRUCTIVE! Usage: make db-reset SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then \
		echo "$(RED)Error: SERVICE required$(NC)"; \
		echo "Usage: make db-reset SERVICE=auth"; \
		exit 1; \
	fi
	@echo "$(RED)WARNING: This will delete all data in $(SERVICE) database!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down $(SERVICE)-db; \
		docker volume rm iyte-$(SERVICE)-db-data || true; \
		docker compose up -d $(SERVICE)-db; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	else \
		echo "$(YELLOW)Aborted$(NC)"; \
	fi

db-shell: ## Open database shell (Usage: make db-shell SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then \
		echo "$(RED)Error: SERVICE required$(NC)"; \
		echo "Usage: make db-shell SERVICE=auth"; \
		exit 1; \
	fi
	@if [ "$(SERVICE)" = "document" ]; then \
		docker compose exec document-db mongosh -u root -p root; \
	else \
		docker compose exec $(SERVICE)-db psql -U postgres -d $(SERVICE)_db; \
	fi

##@ Testing

test: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	@./scripts/test-all.sh

test-auth: ## Run auth service tests
	@echo "$(GREEN)Running auth service tests...$(NC)"
	@cd src/services/auth && uv run pytest -v

test-chat: ## Run chat service tests
	@echo "$(GREEN)Running chat service tests...$(NC)"
	@cd src/services/chat && uv run pytest -v

test-document: ## Run document service tests
	@echo "$(GREEN)Running document service tests...$(NC)"
	@cd src/services/document && uv run pytest -v

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	@./scripts/test-coverage.sh

##@ Code Quality

lint: ## Run linting on all services
	@echo "$(GREEN)Running linting...$(NC)"
	@./scripts/lint-all.sh

lint-auth: ## Lint auth service
	@cd src/services/auth && uv run ruff check .

lint-chat: ## Lint chat service
	@cd src/services/chat && uv run ruff check .

lint-document: ## Lint document service
	@cd src/services/document && uv run ruff check .

lint-fix: ## Auto-fix linting issues
	@echo "$(GREEN)Auto-fixing linting issues...$(NC)"
	@cd src/services/auth && uv run ruff check --fix .
	@cd src/services/chat && uv run ruff check --fix .
	@cd src/services/document && uv run ruff check --fix .
	@echo "$(GREEN)✓ Linting fixes applied$(NC)"

format: ## Format code with ruff
	@echo "$(GREEN)Formatting code...$(NC)"
	@cd src/services/auth && uv run ruff format .
	@cd src/services/chat && uv run ruff format .
	@cd src/services/document && uv run ruff format .
	@echo "$(GREEN)✓ Code formatted$(NC)"

typecheck: ## Run mypy type checking on all services
	@echo "$(GREEN)Running type checking...$(NC)"
	@./scripts/typecheck-all.sh

typecheck-auth: ## Type check auth service
	@cd src/services/auth && uv run mypy .

typecheck-chat: ## Type check chat service
	@cd src/services/chat && uv run mypy .

typecheck-document: ## Type check document service
	@cd src/services/document && uv run mypy .

##@ Code Analysis

check: lint typecheck ## Run all code quality checks
	@echo "$(GREEN)✓ All checks complete$(NC)"

ci: check test ## Run all CI checks locally
	@echo "$(GREEN)✓ CI checks complete$(NC)"

##@ Monitoring & Debugging

logs-auth: ## Show auth service logs
	@docker compose logs -f auth

logs-chat: ## Show chat service logs
	@docker compose logs -f chat

logs-document: ## Show document service logs
	@docker compose logs -f document

logs-gateway: ## Show gateway logs
	@docker compose logs -f gateway

shell-auth: ## Open shell in auth service container
	@docker compose exec auth bash

shell-chat: ## Open shell in chat service container
	@docker compose exec chat bash

shell-document: ## Open shell in document service container
	@docker compose exec document bash

shell-gateway: ## Open shell in gateway container
	@docker compose exec gateway bash

##@ Health Checks

health: ## Check health of all services
	@echo ""
	@echo "$(CYAN)Checking service health...$(NC)"
	@echo ""
	@./scripts/health-check.sh

ping: ## Ping all service endpoints
	@echo "$(CYAN)Pinging services...$(NC)"
	@echo "Gateway:  " && curl -s http://localhost:8000/health | jq '.' || echo "$(RED)✗ Down$(NC)"
	@echo "Auth:     " && curl -s http://localhost:8081/health | jq '.' || echo "$(RED)✗ Down$(NC)"
	@echo "Chat:     " && curl -s http://localhost:8080/health | jq '.' || echo "$(RED)✗ Down$(NC)"
	@echo "Document: " && curl -s http://localhost:8082/health | jq '.' || echo "$(RED)✗ Down$(NC)"

##@ Documentation

docs: ## Generate API documentation
	@echo "$(GREEN)Generating API documentation...$(NC)"
	@echo "Opening Swagger UI..."
	@open http://localhost:8000/docs || xdg-open http://localhost:8000/docs

docs-auth: ## Open auth service docs
	@open http://localhost:8081/docs || xdg-open http://localhost:8081/docs

docs-chat: ## Open chat service docs
	@open http://localhost:8080/docs || xdg-open http://localhost:8080/docs

docs-document: ## Open document service docs
	@open http://localhost:8082/docs || xdg-open http://localhost:8082/docs

##@ Git Workflow

branch: ## Create new feature branch (Usage: make branch NAME=feature-name)
	@if [ -z "$(NAME)" ]; then \
		echo "$(RED)Error: NAME required$(NC)"; \
		echo "Usage: make branch NAME=feature-name"; \
		exit 1; \
	fi
	@git checkout dev
	@git pull origin dev
	@git checkout -b $(NAME)
	@echo "$(GREEN)✓ Created and switched to branch: $(NAME)$(NC)"

commit: ## Quick commit (Usage: make commit MSG="commit message")
	@if [ -z "$(MSG)" ]; then \
		echo "$(RED)Error: MSG required$(NC)"; \
		echo "Usage: make commit MSG=\"your commit message\""; \
		exit 1; \
	fi
	@git add .
	@git commit -m "$(MSG)"
	@echo "$(GREEN)✓ Changes committed$(NC)"

push: ## Push current branch to origin
	@BRANCH=$$(git rev-parse --abbrev-ref HEAD); \
	git push origin $$BRANCH
	@echo "$(GREEN)✓ Pushed to origin$(NC)"

pull: ## Pull latest changes from dev
	@git checkout dev
	@git pull origin dev
	@echo "$(GREEN)✓ Pulled latest changes$(NC)"

status: ## Show git status
	@git status

##@ Quick Commands

start: dev-up ## Alias for dev-up

stop: dev-down ## Alias for dev-down

restart: dev-restart ## Alias for dev-restart

logs: dev-logs ## Alias for dev-logs

build: dev-build ## Alias for dev-build

rebuild: dev-rebuild ## Alias for dev-rebuild

clean: dev-clean ## Alias for dev-clean

up: dev-up ## Alias for dev-up

down: dev-down ## Alias for dev-down

ps: dev-status ## Alias for dev-status

##@ Information

info: ## Show project information
	@echo ""
	@echo "$(CYAN)IYTE Soru Botu - Project Information$(NC)"
	@echo ""
	@echo "$(YELLOW)Services:$(NC)"
	@echo "  • Gateway:  http://localhost:8000"
	@echo "  • Auth:     http://localhost:8081"
	@echo "  • Chat:     http://localhost:8080"
	@echo "  • Document: http://localhost:8082"
	@echo ""
	@echo "$(YELLOW)Databases:$(NC)"
	@echo "  • Auth DB:     PostgreSQL (port 5433)"
	@echo "  • Chat DB:     PostgreSQL (port 5432)"
	@echo "  • Document DB: MongoDB (port 27017)"
	@echo ""
	@echo "$(YELLOW)Infrastructure:$(NC)"
	@echo "  • Redis (Gateway): port 6380"
	@echo "  • Redis (Chat):    port 6379"
	@echo "  • ChromaDB:        port 8001"
	@echo "  • MinIO:           port 9000 (Console: 9001)"
	@echo ""

ports: ## Show all exposed ports
	@echo ""
	@echo "$(CYAN)Exposed Ports:$(NC)"
	@echo ""
	@docker compose ps --format "table {{.Name}}\t{{.Ports}}" | sed 's/0.0.0.0://g'
	@echo ""

list: ## List all services
	@echo ""
	@echo "$(CYAN)Available Services:$(NC)"
	@echo ""
	@echo "  $(GREEN)gateway$(NC)   - API Gateway"
	@echo "  $(GREEN)auth$(NC)      - Authentication Service"
	@echo "  $(GREEN)chat$(NC)      - Chat Service (with AI agents)"
	@echo "  $(GREEN)document$(NC)  - Document Management Service"
	@echo ""
