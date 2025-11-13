#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 5000
    DEBUG: bool = True
    SECRET_KEY: str = "default_secret_key"

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "portfolio_user"
    DB_PASSWORD: str = "portfolio_password"
    DB_NAME: str = "portfolio_db"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Construct MariaDB connection string"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False  # Set to True for SQL query debugging

    class Config:
        env_file = ".env"

config = Config()
