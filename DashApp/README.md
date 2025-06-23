# Urotheliome Gene Expression Dashboard

Interactive dashboard for visualizing JBU gene expression data using Dash and SQLite.

## Features

- Gene expression visualization with multiple plot types (Swarm, Violin, Box)
- Multi-dataset comparison
- Dynamic x-axis selection (Gene, NHU, Tissue, Gender, etc.)
- Easy to build on structure
- SQLite database backend
- Docker Compose

## Project Structure

```
urotheliome-dash/
├── app.py                       # Application entry point
├── assets/                      # CSS styles / images
├── callbacks/                   # Function callbacks (update ui based on user input)
├── components/                  # Dash UI components (Dropdowns, radio-buttons)
├── data/                        # Data fetching
├── db/                          # Database utilities
└── layouts/                     # Page layouts
```

UrotheliomeData.db can be placed anywhere.
Remember to set the DATABASE_PATH env variable.
```
├── UrotheliomeData.db           # indexed SQLite database
```

## Usage

0. Set the DATABASE_PATH env variable
1. Run application:
```bash
docker compose up -d
```
2. Open browser: `http://localhost:8080`
3. Select:
   - Genes to visualize
   - X-axis variable
   - Plot type
   - Datasets to compare
4. Admire the graph

## Data Flow

1. User selects parameters via UI
2. Callbacks fetch data from SQLite
3. Data transformed into selected plot type
4. Plot updates (some automatic formatting applied e.g. rotating lables when > 10)