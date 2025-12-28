#!/usr/bin/env bash
set -euo pipefail

# IYTE Soru Botu Health Check Script
# Check health of all services

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_service_health() {
    local service=$1
    local url=$2
    local port=$3

    if curl -sf "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $service (port $port) - ${GREEN}HEALTHY${NC}"
        return 0
    else
        echo -e "${RED}✗${NC} $service (port $port) - ${RED}DOWN${NC}"
        return 1
    fi
}

print_docker_health() {
    local container=$1
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "not-found")

    case $health in
        "healthy")
            echo -e "${GREEN}✓${NC} $container - ${GREEN}HEALTHY${NC}"
            return 0
            ;;
        "unhealthy")
            echo -e "${RED}✗${NC} $container - ${RED}UNHEALTHY${NC}"
            return 1
            ;;
        "starting")
            echo -e "${YELLOW}⚠${NC} $container - ${YELLOW}STARTING${NC}"
            return 1
            ;;
        "not-found")
            echo -e "${RED}✗${NC} $container - ${RED}NOT RUNNING${NC}"
            return 1
            ;;
        *)
            echo -e "${YELLOW}?${NC} $container - ${YELLOW}NO HEALTHCHECK${NC}"
            # Check if container is running
            if docker ps --format '{{.Names}}' | grep -q "^$container$"; then
                echo -e "  ${GREEN}→${NC} Container is running"
                return 0
            else
                echo -e "  ${RED}→${NC} Container is not running"
                return 1
            fi
            ;;
    esac
}

main() {
    print_header "Service Health Check"
    echo ""

    local failed=0

    echo -e "${CYAN}Application Services:${NC}"
    print_service_health "Gateway" "http://localhost:8000/health" "8000" || ((failed++))
    print_service_health "Auth Service" "http://localhost:8081/health" "8081" || ((failed++))
    print_service_health "Chat Service" "http://localhost:8080/health" "8080" || ((failed++))
    print_service_health "Document Service" "http://localhost:8082/health" "8082" || ((failed++))

    echo ""
    echo -e "${CYAN}Infrastructure Services:${NC}"
    print_docker_health "iyte-auth-db" || ((failed++))
    print_docker_health "iyte-chat-db" || ((failed++))
    print_docker_health "iyte-document-db" || ((failed++))
    print_docker_health "iyte-gateway-redis" || ((failed++))
    print_docker_health "iyte-chat-redis" || ((failed++))
    print_docker_health "iyte-chromadb" || ((failed++))
    print_docker_health "iyte-minio" || ((failed++))

    echo ""
    print_header "Summary"

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✓ All services are healthy!${NC}"
        exit 0
    else
        echo -e "${RED}✗ $failed service(s) are unhealthy or down${NC}"
        echo ""
        echo -e "${YELLOW}Troubleshooting:${NC}"
        echo "  1. Check service logs: make dev-logs"
        echo "  2. Restart services:   make dev-restart"
        echo "  3. Rebuild services:   make dev-rebuild"
        exit 1
    fi
}

main "$@"
