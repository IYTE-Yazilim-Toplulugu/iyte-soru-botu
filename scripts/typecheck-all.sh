#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Type Checking Script
# Run mypy type checking on all services

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

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Type check service
typecheck_service() {
    local service=$1
    print_header "Type checking $service service"

    cd "$PROJECT_ROOT/src/services/$service"

    if uv run mypy .; then
        print_success "$service type checking passed"
        return 0
    else
        print_warning "$service type checking failed (non-blocking)"
        return 1
    fi
}

# Type check shared kernel
typecheck_shared_kernel() {
    print_header "Type checking Shared Kernel"

    cd "$PROJECT_ROOT/src/libs/shared-kernel"

    if uv run mypy .; then
        print_success "Shared kernel type checking passed"
        return 0
    else
        print_warning "Shared kernel type checking failed (non-blocking)"
        return 1
    fi
}

# Type check gateway
typecheck_gateway() {
    print_header "Type checking Gateway"

    cd "$PROJECT_ROOT/src/gateway"

    if uv run mypy .; then
        print_success "Gateway type checking passed"
        return 0
    else
        print_warning "Gateway type checking failed (non-blocking)"
        return 1
    fi
}

# Main type check runner
main() {
    print_header "IYTE Soru Botu - Type Checking"

    local failed=0
    local total=0

    ((total++))
    typecheck_shared_kernel || ((failed++))

    for service in auth chat document; do
        ((total++))
        typecheck_service "$service" || ((failed++))
    done

    ((total++))
    typecheck_gateway || ((failed++))

    print_header "Type Checking Summary"

    local passed=$((total - failed))
    echo -e "Total Components: ${BLUE}$total${NC}"
    echo -e "Passed:           ${GREEN}$passed${NC}"
    echo -e "Failed:           ${YELLOW}$failed${NC}"
    echo ""

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All type checks passed!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠ Some type checks failed (non-blocking)${NC}"
        echo -e "${YELLOW}Type checking failures are warnings, not errors${NC}"
        exit 0
    fi
}

main "$@"
