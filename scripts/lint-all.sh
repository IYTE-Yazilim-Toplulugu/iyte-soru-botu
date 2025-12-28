#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Linting Script
# Run ruff linting on all services

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

# Lint service
lint_service() {
    local service=$1
    print_header "Linting $service service"

    cd "$PROJECT_ROOT/src/services/$service"

    if uv run ruff check .; then
        print_success "$service linting passed"
        return 0
    else
        print_error "$service linting failed"
        return 1
    fi
}

# Lint shared kernel
lint_shared_kernel() {
    print_header "Linting Shared Kernel"

    cd "$PROJECT_ROOT/src/libs/shared-kernel"

    if uv run ruff check .; then
        print_success "Shared kernel linting passed"
        return 0
    else
        print_error "Shared kernel linting failed"
        return 1
    fi
}

# Lint gateway
lint_gateway() {
    print_header "Linting Gateway"

    cd "$PROJECT_ROOT/src/gateway"

    if uv run ruff check .; then
        print_success "Gateway linting passed"
        return 0
    else
        print_error "Gateway linting failed"
        return 1
    fi
}

# Main lint runner
main() {
    print_header "IYTE Soru Botu - Linting"

    local failed=0
    local total=0

    ((total++))
    lint_shared_kernel || ((failed++))

    for service in auth chat document; do
        ((total++))
        lint_service "$service" || ((failed++))
    done

    ((total++))
    lint_gateway || ((failed++))

    print_header "Linting Summary"

    local passed=$((total - failed))
    echo -e "Total Components: ${BLUE}$total${NC}"
    echo -e "Passed:           ${GREEN}$passed${NC}"
    echo -e "Failed:           ${RED}$failed${NC}"
    echo ""

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All linting checks passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some linting checks failed${NC}"
        echo -e "${YELLOW}Run 'make lint-fix' to auto-fix issues${NC}"
        exit 1
    fi
}

main "$@"
