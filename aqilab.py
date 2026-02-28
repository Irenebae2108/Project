# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 20:54:37 2026

@author: 91952
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. LOAD AIR QUALITY DATA
# -----------------------------
df = pd.read_csv(r"C:\Users\91952\Desktop\231BCADA58\air1.csv")
df.info()
# Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Use existing AQI
df["AQI"] = df["AQI Value"]

# -----------------------------
# 2. CMAQ-LIKE GRID ENVIRONMENT
# -----------------------------
grid_size = (20, 20)
time_steps = len(df)

cmaq_grid = np.zeros((time_steps, grid_size[0], grid_size[1]))

# Emission agent locations
np.random.seed(1)
num_emitters = 10
emit_x = np.random.randint(0, grid_size[0], num_emitters)
emit_y = np.random.randint(0, grid_size[1], num_emitters)

# -----------------------------
# 3. AGENT-BASED SIMULATION
# -----------------------------
for t in range(1, time_steps):

    # Chemical decay
    cmaq_grid[t] = cmaq_grid[t-1] * 0.9

    # Emissions scaled by PM2.5 AQI
    emission_strength = df.loc[t, "PM2.5 AQI Value"] / 50

    for i in range(num_emitters):
        cmaq_grid[t, emit_x[i], emit_y[i]] += emission_strength

    # CMAQ-style diffusion
    cmaq_grid[t] = (
        np.roll(cmaq_grid[t], 1, axis=0) +
        np.roll(cmaq_grid[t], -1, axis=0) +
        np.roll(cmaq_grid[t], 1, axis=1) +
        np.roll(cmaq_grid[t], -1, axis=1)
    ) / 4

# -----------------------------
# 4. OSSE SENSOR AGENTS
# -----------------------------
num_sensors = 6
sensor_x = np.random.randint(0, grid_size[0], num_sensors)
sensor_y = np.random.randint(0, grid_size[1], num_sensors)

osse_aqi = []

for t in range(time_steps):
    readings = [
        cmaq_grid[t, sensor_x[i], sensor_y[i]]
        for i in range(num_sensors)
    ]
    osse_aqi.append(np.mean(readings) * 40)

osse_aqi = np.array(osse_aqi)

# -----------------------------
# 5. VISUALIZATIONS
# -----------------------------

# AQI comparison
plt.figure(figsize=(8,4))
plt.plot(df["AQI"], label="Observed AQI")
plt.plot(osse_aqi, label="Simulated AQI (Hybrid Model)")
plt.xlabel("Time")
plt.ylabel("AQI")
plt.title("Hybrid Agent-Based CMAQ–OSSE AQI Simulation")
plt.legend()
plt.grid()
plt.show()

# Final spatial pollution map
plt.figure(figsize=(5,5))
plt.imshow(cmaq_grid[-1], cmap="inferno")
plt.colorbar(label="Pollutant Concentration")
plt.title("Final Spatial Pollution Distribution")
plt.show()

df["AQI"] = df["AQI Value"]

# Create Day/Night flags (OSSE assumption)
df["TimeType"] = ["Day" if i % 2 == 0 else "Night" for i in range(len(df))]

# Day vs Night AQI scaling
df["AQI_Day"] = df["AQI"] * 1.2      # higher emissions
df["AQI_Night"] = df["AQI"] * 0.8    # reduced activity

# Plot
plt.figure(figsize=(9,4))
plt.plot(df["AQI_Day"], label="Day AQI", alpha=0.8)
plt.plot(df["AQI_Night"], label="Night AQI", alpha=0.8)
plt.xlabel("Time")
plt.ylabel("AQI")
plt.title("Day vs Night AQI Simulation (air1.csv)")
plt.legend()
plt.grid()
plt.show()

# Latitude–Longitude grid
lat = np.linspace(-90, 90, 180)
lon = np.linspace(-180, 180, 360)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Base pollution field
base_pollution = (
    45
    + 30 * np.sin(np.radians(lat_grid))     # latitude effect
    + 20 * np.cos(np.radians(lon_grid / 2)) # continental pattern
)

# Day vs Night
world_day = base_pollution * 1.25
world_night = base_pollution * 0.75

# DAY MAP
plt.figure(figsize=(12,5))
plt.imshow(
    world_day,
    extent=[-180, 180, -90, 90],
    origin="lower"
)
plt.colorbar(label="Simulated AQI (Day)")
plt.title("Global AQI Simulation – Daytime")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# NIGHT MAP
plt.figure(figsize=(12,5))
plt.imshow(
    world_night,
    extent=[-180, 180, -90, 90],
    origin="lower"
)
plt.colorbar(label="Simulated AQI (Night)")
plt.title("Global AQI Simulation – Nighttime")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# -----------------------------
# GLOBAL AQI COMPOSITION MODEL
# -----------------------------

lat = np.linspace(-90, 90, 180)
lon = np.linspace(-180, 180, 360)
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Simulated pollutant AQI components
PM25 = 40 + 30 * np.exp(-(lat_grid/25)**2)            # high near equator
NO2  = 20 + 25 * np.cos(np.radians(lon_grid))         # urban belts
O3   = 15 + 20 * np.sin(np.radians(lat_grid))         # mid-latitudes
CO   = 10 + 15 * np.cos(np.radians(lat_grid / 2))     # biomass burning
SO2  = 8  + 12 * np.sin(np.radians(lon_grid / 3))     # industrial zones

pollutants = np.stack([PM25, NO2, O3, CO, SO2])
dominant = np.argmax(pollutants, axis=0)

plt.figure(figsize=(14,6))
plt.imshow(
    dominant,
    extent=[-180, 180, -90, 90],
    origin="lower",
    cmap="tab10"
)
plt.colorbar(
    ticks=[0,1,2,3,4],
    label="Dominant Pollutant"
)
plt.clim(-0.5, 4.5)

plt.title("Global AQI Composition – Dominant Pollutant")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()





























