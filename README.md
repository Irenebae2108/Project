# Project Overview

This project implements a Hybrid Air Quality Simulation Model combining:

Agent-Based Modeling (ABM)

CMAQ-style diffusion simulation

OSSE (Observing System Simulation Experiment) sensor modeling

Global spatial AQI visualization

The system simulates pollutant emission, diffusion, sensor-based AQI estimation, and global pollutant composition analysis using real air quality data.

# Objectives

Load and preprocess real-world AQI data (air1.csv)

Simulate pollutant diffusion over a 2D spatial grid

Model emission sources as agents

Simulate OSSE-based sensor observations

# Data Description

The study utilizes the dataset air1.csv, which contains recorded air quality measurements including the overall Air Quality Index (AQI Value) and pollutant-specific indicators such as PM2.5 AQI Value. Each row in the dataset represents a time-based observation (e.g., hourly or daily), while columns correspond to different air quality parameters. The AQI Value serves as the primary observed indicator of air pollution levels and is used as the ground truth for comparison with simulated results. Missing numerical values are handled using mean imputation to maintain data continuity and ensure robustness in simulation. The PM2.5 AQI values are specifically used to scale emission intensity within the hybrid modeling framework, as fine particulate matter is a major contributor to overall air pollution dynamics.

# Methodology

The project adopts a hybrid modeling framework combining data-driven analysis with spatial simulation techniques. First, the dataset is preprocessed to handle missing values and extract relevant AQI variables. A two-dimensional spatial grid (20×20) is initialized to simulate pollutant concentration distribution over time. The simulation progresses across multiple time steps equal to the length of the dataset. At each step, pollutant concentration undergoes chemical decay, emission injection, and diffusion processes. Emission strength is dynamically scaled based on observed PM2.5 AQI values, linking real-world data with simulated spatial behavior. The resulting simulated AQI is compared with observed AQI to evaluate system performance. Additional scenario-based modeling, such as Day vs Night scaling and global pollutant distribution, is implemented to analyze spatial and temporal variations.

🌍 CMAQ-like Simulation Model

The modeling framework incorporates a simplified representation inspired by the CMAQ (Community Multiscale Air Quality) system. In this implementation, a 20×20 spatial grid represents the atmospheric environment. Pollutant concentrations evolve over time according to three core processes: chemical decay, emissions, and diffusion. Chemical decay reduces pollutant concentration at each time step to simulate atmospheric reactions and natural dissipation. Emission sources are modeled as fixed agents placed randomly within the grid, and their emission intensity is scaled proportionally to PM2.5 AQI values from the dataset. Diffusion is simulated using a neighbor-averaging approach, where pollutant concentration spreads across adjacent grid cells, mimicking atmospheric transport processes. Although simplified compared to real CMAQ systems, this approach captures essential spatial dispersion behavior in a computationally efficient manner.

# OSSE (Observing System Simulation Experiment) Framework

The model integrates an Observing System Simulation Experiment (OSSE) component to simulate virtual sensor measurements. A set of sensor agents is randomly positioned within the spatial grid to represent monitoring stations. At each time step, these sensors record local pollutant concentrations from the simulated grid. The average of these sensor readings is scaled to estimate a simulated AQI value. This OSSE-based AQI is then compared with the observed AQI from the dataset to assess how well the simulated atmospheric model approximates real-world conditions. The OSSE framework helps evaluate sensor placement strategies, measurement variability, and the relationship between spatial pollutant distribution and observed air quality indicators.

