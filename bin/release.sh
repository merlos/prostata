#!/bin/bash

# Release script for prostata package to PyPI
#
# Usage: 
# Set the PYPI_API_TOKEN environment variable for production releases or the TEST_PYPI_API_TOKEN environment variable for test releases.
# Example: 
#   export PYPI_API_TOKEN="pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#   export TEST_PYPI_API_TOKEN="pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 
# ./bin/release.sh [--test] [-y] [--help]
# 
# 
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TEST_PYPI=false
REPOSITORY="pypi"
SKIP_CONFIRMATION=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_PYPI=true
            REPOSITORY="testpypi"
            shift
            ;;
        -y|--yes)
            SKIP_CONFIRMATION=true
            shift
            ;;
        --help)
            echo "Usage: $0 [--test] [-y|--yes] [--help]"
            echo ""
            echo "Options:"
            echo "  --test        Upload to Test PyPI instead of production PyPI"
            echo "  -y, --yes     Skip confirmation prompts (useful for automation)"
            echo "  --help        Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  PYPI_API_TOKEN        Your PyPI API token (required)"
            echo "  TEST_PYPI_API_TOKEN   Your Test PyPI API token (used with --test)"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check for API token
if [ "$TEST_PYPI" = true ]; then
    if [ -z "$TEST_PYPI_API_TOKEN" ]; then
        echo -e "${RED}Error: TEST_PYPI_API_TOKEN environment variable is not set${NC}"
        echo "Get your Test PyPI API token from: https://test.pypi.org/manage/account/token/"
        exit 1
    fi
    API_TOKEN="$TEST_PYPI_API_TOKEN"
    PYPI_URL="https://test.pypi.org/legacy/"
else
    if [ -z "$PYPI_API_TOKEN" ]; then
        echo -e "${RED}Error: PYPI_API_TOKEN environment variable is not set${NC}"
        echo "Get your PyPI API token from: https://pypi.org/manage/account/token/"
        exit 1
    fi
    API_TOKEN="$PYPI_API_TOKEN"
    PYPI_URL="https://upload.pypi.org/legacy/"
fi

echo -e "${GREEN}Starting release process...${NC}"

# Change to project directory
cd "$PROJECT_DIR"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found. Are you in the project root?${NC}"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Install build dependencies
echo "Installing build dependencies..."
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}Error: Python not found. Please install Python 3.8+${NC}"
    exit 1
fi

$PYTHON_CMD -m pip install --quiet build twine

# Build the package
echo "Building package..."
$PYTHON_CMD -m build

# Check if build succeeded
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo -e "${RED}Error: Build failed or dist directory is empty${NC}"
    exit 1
fi

# Show what will be uploaded
echo "Package files to be uploaded:"
ls -la dist/

# Confirm upload
if [ "$SKIP_CONFIRMATION" = false ]; then
    if [ "$TEST_PYPI" = true ]; then
        echo -e "${YELLOW}Ready to upload to Test PyPI${NC}"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Upload cancelled"
            exit 0
        fi
    else
        echo -e "${YELLOW}Ready to upload to production PyPI${NC}"
        echo -e "${RED}WARNING: This will publish to the real PyPI!${NC}"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Upload cancelled"
            exit 0
        fi
    fi
else
    if [ "$TEST_PYPI" = true ]; then
        echo -e "${YELLOW}Uploading to Test PyPI (skipping confirmation)${NC}"
    else
        echo -e "${YELLOW}Uploading to production PyPI (skipping confirmation)${NC}"
        echo -e "${RED}WARNING: This will publish to the real PyPI!${NC}"
    fi
fi

# Upload to PyPI
echo "Uploading to PyPI..."
$PYTHON_CMD -m twine upload \
    --repository-url "$PYPI_URL" \
    --username __token__ \
    --password "$API_TOKEN" \
    dist/*

if [ $? -eq 0 ]; then
    if [ "$TEST_PYPI" = true ]; then
        echo -e "${GREEN}Successfully uploaded to Test PyPI!${NC}"
        echo "You can test the installation with:"
        echo "pip install --index-url https://test.pypi.org/simple/ prostata"
    else
        echo -e "${GREEN}Successfully uploaded to PyPI!${NC}"
        echo "Users can now install with:"
        echo "pip install prostata"
    fi
else
    echo -e "${RED}Upload failed!${NC}"
    exit 1
fi