#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Dependency Sync Script
# Sync dependencies for all services

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

# Sync shared kernel
sync_shared_kernel() {
    print_header "Syncing Shared Kernel"
    cd "$PROJECT_ROOT/src/libs/shared-kernel"

    if uv sync; then
        print_success "Shared kernel synced"
    else
        print_error "Failed to sync shared kernel"
        return 1
    fi
}

# Sync service
sync_service() {
    local service=$1
    print_header "Syncing $service service"

    cd "$PROJECT_ROOT/src/services/$service"

    if uv sync; then
        print_success "$service service synced"
    else
        print_error "Failed to sync $service service"
        return 1
    fi
}

# Sync gateway
sync_gateway() {
    print_header "Syncing Gateway"
    cd "$PROJECT_ROOT/src/gateway"

    if uv sync; then
        print_success "Gateway synced"
    else
        print_error "Failed to sync gateway"
        return 1
    fi
}

# Main sync
main() {
    print_header "IYTE Soru Botu - Dependency Sync"

    local failed=0

    sync_shared_kernel || ((failed++))
    sync_service "auth" || ((failed++))
    sync_service "chat" || ((failed++))
    sync_service "document" || ((failed++))
    sync_gateway || ((failed++))

    if [ $failed -eq 0 ]; then
        print_header "Sync Complete!"
        echo -e "${GREEN}All dependencies synced successfully!${NC}"
    else
        print_header "Sync Failed!"
        echo -e "${RED}$failed component(s) failed to sync${NC}"
        exit 1
    fi
}

main "$@"
