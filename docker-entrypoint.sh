#!/bin/sh

set -e

hasura migrate apply --all-databases
hasura metadata apply
