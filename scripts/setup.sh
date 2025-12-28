#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Setup Script
# Install dependencies for all services

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    local missing_tools=()

    if ! command -v uv &> /dev/null; then
        missing_tools+=("uv (install: curl -LsSf https://astral.sh/uv/install.sh | sh)")
    fi

    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi

    if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
        missing_tools+=("docker compose")
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_error "Missing required tools:"
        for tool in "${missing_tools[@]}"; do
            echo "  - $tool"
        done
        exit 1
    fi

    print_success "All prerequisites met"
}

# Setup shared kernel
setup_shared_kernel() {
    print_header "Setting up Shared Kernel"

    cd "$PROJECT_ROOT/src/libs/shared-kernel"

    print_info "Installing shared-kernel dependencies..."
    uv sync

    print_success "Shared kernel setup complete"
}

# Setup service
setup_service() {
    local service=$1

    print_header "Setting up $service service"

    cd "$PROJECT_ROOT/src/services/$service"

    print_info "Installing $service dependencies..."
    uv sync

    print_success "$service service setup complete"
}

# Setup gateway
setup_gateway() {
    print_header "Setting up Gateway"

    cd "$PROJECT_ROOT/src/gateway"

    print_info "Installing gateway dependencies..."
    uv sync

    print_success "Gateway setup complete"
}

# Create .env if it doesn't exist
setup_env() {
    print_header "Setting up Environment Variables"

    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        if [ -f "$PROJECT_ROOT/.env.example" ]; then
            cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
            print_success ".env file created from .env.example"
            print_info "Please edit .env file with your configuration"
        else
            print_info ".env.example not found, skipping"
        fi
    else
        print_info ".env file already exists"
    fi
}

# Main setup
main() {
    print_header "IYTE Soru Botu - Setup"

    check_prerequisites
    setup_env
    setup_shared_kernel
    setup_service "auth"
    setup_service "chat"
    setup_service "document"
    setup_gateway

    print_header "Setup Complete!"

    echo -e "${GREEN}All services are ready!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Edit .env file if needed"
    echo "  2. Start services: ${CYAN}make dev-up${NC}"
    echo "  3. Check status:   ${CYAN}make dev-status${NC}"
    echo "  4. View logs:      ${CYAN}make dev-logs${NC}"
    echo ""
}

main "$@"
