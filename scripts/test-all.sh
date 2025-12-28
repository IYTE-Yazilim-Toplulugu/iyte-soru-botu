#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Test Runner
# Run tests for all services

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

# Test service
test_service() {
    local service=$1
    print_header "Testing $service service"

    cd "$PROJECT_ROOT/src/services/$service"

    if [ ! -d "src/tests" ]; then
        print_info "No tests found for $service service"
        return 0
    fi

    if uv run pytest -v; then
        print_success "$service tests passed"
        return 0
    else
        print_error "$service tests failed"
        return 1
    fi
}

# Main test runner
main() {
    print_header "IYTE Soru Botu - Test Runner"

    local failed=0
    local total=0

    for service in auth chat document; do
        ((total++))
        test_service "$service" || ((failed++))
    done

    print_header "Test Summary"

    local passed=$((total - failed))
    echo -e "Total Services: ${BLUE}$total${NC}"
    echo -e "Passed:         ${GREEN}$passed${NC}"
    echo -e "Failed:         ${RED}$failed${NC}"
    echo ""

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        exit 1
    fi
}

main "$@"
