#!/bin/bash
gunicorn testes.main:app --bind 0.0.0.0:$PORT
