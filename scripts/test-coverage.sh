#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Coverage Report Generator
# Run tests with coverage for all services

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

# Test service with coverage
test_service_coverage() {
    local service=$1
    print_header "Testing $service service with coverage"

    cd "$PROJECT_ROOT/src/services/$service"

    if [ ! -d "src/tests" ]; then
        print_info "No tests found for $service service"
        return 0
    fi

    if uv run pytest -v \
        --cov=src \
        --cov-report=term-missing \
        --cov-report=html:coverage_html \
        --cov-report=xml:coverage.xml; then
        print_success "$service coverage report generated"
        print_info "HTML report: src/services/$service/coverage_html/index.html"
        return 0
    else
        print_error "$service coverage generation failed"
        return 1
    fi
}

# Main coverage runner
main() {
    print_header "IYTE Soru Botu - Coverage Report Generator"

    local failed=0
    local total=0

    for service in auth chat document; do
        ((total++))
        test_service_coverage "$service" || ((failed++))
    done

    print_header "Coverage Summary"

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All coverage reports generated!${NC}"
        echo ""
        echo -e "${CYAN}View HTML reports:${NC}"
        for service in auth chat document; do
            if [ -d "$PROJECT_ROOT/src/services/$service/coverage_html" ]; then
                echo "  • $service: src/services/$service/coverage_html/index.html"
            fi
        done
        echo ""
        exit 0
    else
        echo -e "${RED}✗ Some coverage reports failed${NC}"
        exit 1
    fi
}

main "$@"
