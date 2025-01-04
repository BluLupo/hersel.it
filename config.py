#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 5000
    DEBUG: bool = True
    SECRET_KEY: str = "default_secret_key"

    class Config:
        env_file = ".env"

config = Config()
