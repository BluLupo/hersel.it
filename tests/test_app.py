#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

import pytest
import httpx

BASE_URL = "http://127.0.0.1:5000"

@pytest.mark.asyncio
async def test_home_route():
    """
    Testa la route principale del Blueprint `route_home`.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "Welcome" in response.text

@pytest.mark.asyncio
async def test_404_route():
    """
    Verifica la gestione di una route inesistente.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/nonexistent")
        assert response.status_code == 404

