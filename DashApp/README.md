# Urotheliome Gene Expression Dashboard

Interactive dashboard for visualizing JBU gene expression data using Dash and SQLite.

## Features

- Gene expression visualization with multiple plot types (Swarm, Violin, Box)
- Multi-dataset comparison
- Dynamic x-axis selection (Gene, NHU, Tissue, Gender, etc.)
- Easy to build on structure
- SQLite database backend

## Project Structure

```
urotheliome-dash/
├── app.py                       # Application entry point
├── urotheliome_data_indexed.db  # indexed SQLite database
├── urotheliome_data_2.db        # old unindexed SQLite database
├── assets/                      # CSS styles / images
├── callbacks/                   # Function callbacks (update ui based on user input)
├── components/                  # Dash UI components (Dropdowns, radio-buttons)
├── data/                        # Data fetching
├── db/                          # Database utilities
└── layouts/                     # Page layouts
```

## Usage

1. Run application:
```bash
python app.py
```
2. Open browser: `http://localhost:8050`
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