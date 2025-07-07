# Urotheliome Gene Expression Dashboard

Interactive web application for visualizing JBU gene expression data, built with Dash and SQLite. This project provides researchers with tools to explore gene expression patterns across multiple datasets.

## Live Application

The application is hosted at: **https://urotheliome.york.ac.uk/**

## Project Background

This project was originally started by a PhD student and has been rewritten as part of an RSE internship. The new implementation uses a Dash-based architecture with SQLite for efficient data storage and retrieval.

## Features

### Gene Explorer
- **Gene Visualization**: 
  - Visualize multiple genes simultaneously across different datasets
  - Multiple plot types (Swarm, Violin, Box plots)
  - Configurable x-axis variables (Gene, NHU, Tissue, Gender, etc.)
  - TER (Transepithelial Electrical Resistance) threshold filtering
  - Real-time plot updates and interactive filtering

- **Gene Comparison**:
  - Compare two genes with correlation analysis
  - Regression line visualization
  - Multiple correlation metrics and statistical analysis

### Additional Features
- **Genome Browser**: Proof of concept (work in progress)
- **Containerized Deployment**: Docker and Docker Compose support
- **Dependabot Setup**: Keeps dependencies up to date

## Architecture

```
urotheliome-dash/
├── DashApp/                     # Main web application
│   ├── app.py                   # Application entry point
│   ├── assets/                  # CSS styles and images
│   ├── callbacks/               # UI interaction callbacks
│   ├── components/              # Reusable UI components
│   ├── data/                    # Data fetching utilities
│   ├── db/                      # Database connection utilities
│   └── layouts/                 # Page layouts and navigation
├── db-generation/               
│   ├── import_data.ipynb        # Jupyter notebook for database creation
│   └── schema.sql               # SQLite database schema
├── JBU_data/                    # Source data files
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Container build instructions
└── README.md                    # This file
```

## Technology Stack

- **Backend**: Python, Dash, SQLite
- **Frontend**: Dash components, Plotly.js, Bootstrap components
- **Database**: SQLite with indexed gene expression data
- **Deployment**: Docker Compose, Apache (with SSL)
- **Infrastructure**: University VM with Puppet configuration

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Jupyter Notebook (for database generation)

## Database Setup

The application requires a SQLite database containing gene expression data and metadata.

1. **Generate Database**:
   ```bash
   cd db-generation/
   jupyter notebook import_data.ipynb
   ```
   
2. **Run All Cells** in the notebook to create `UrotheliomeData.db`

3. **Set Environment Variable**:
   ```bash
   export DATABASE_PATH=/path/to/UrotheliomeData.db
   ```

## Local Development

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd urotheliome-dash
   ```

2. **Set Database Path**:
   ```bash
   export DATABASE_PATH=/path/to/UrotheliomeData.db
   ```

3. **Run with Docker Compose**:
   ```bash
   docker compose up -d
   ```

4. **Access Application**:
   Open browser to `http://localhost:8050`

## Production Deployment

The application is managed by Puppet and deployed on a University of York VM with the following configuration:

- **Server**: University VM - `urotheliome.york.ac.uk`
- **Web Server**: Apache with SSL certificates
- **Puppet Manifest**: `urotheliomen` branch of `sys-puppet-control-its` repository
- **Apache Module**: `its_apache` module for vhost and SSL configuration

## Data Flow

1. **User Input**: Gene selection, plot parameters, dataset filters
2. **Data Retrieval**: SQL queries to indexed SQLite database
3. **Processing**: Data transformation and aggregation
4. **Visualization**: Dynamic plot generation with Plotly

## Database Schema

The SQLite database contains the following key tables:

- `Gene`: Gene names and identifiers
- `Sample`: Sample metadata (tissue, gender, treatment, etc.)
- `GeneExpression`: TPM values linking genes to samples
- `Dataset`: Dataset names

## Usage

1. **Select Genes**: Choose genes of interest from the dropdown
2. **Configure X-axis**: Select grouping variable (Dataset, Tissue, Gender, etc.)
3. **Choose Plot Type**: Select visualization method (Swarm, Violin, Box)
4. **Filter Datasets**: Select specific datasets for comparison
5. **View Results**: Interactive plots update automatically

## Environment Variables

- `DATABASE_PATH`: Path to SQLite database file (required)

## Acknowledgments

- [Original project repository](https://github.com/vladUng/visualisation)
- Data sources: JBU research group

---

**Note**: The original project documentation has been preserved in `README - old.md` for reference. 