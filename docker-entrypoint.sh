#!/usr/bin/env bash

# Migrations
make migrate

poetry run python -m app --reload
