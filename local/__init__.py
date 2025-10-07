"""
Local settings package.

This directory contains environment-specific Django settings that should NOT be committed to git.
Files in this directory override the base settings in core/backend/settings/.

Usage:
    - Copy templates from core/backend/settings/templates/ to this directory
    - Customize with your local/environment-specific values
    - Never commit these files (they're in .gitignore)

Example:
    cp core/backend/settings/templates/settings.dev.py local/settings.dev.py
"""
