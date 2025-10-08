from dash import html
import dash_bootstrap_components as dbc

def home_layout() -> html.Div:
    """
    Create the home page layout with mission statement, logos, and usage guide
    Returns:
        Dash HTML Div containing the home page layout
    """
    # Container style for consistent look
    container_style = {"max-width": "1200px"}
    
    # Mission statement section
    mission_section = dbc.Card(
        dbc.CardBody([
            html.H3("About", className="card-title text-primary"),
            html.P(
                "All somatic cells in our body contain the same DNA, with approximately 20,000 different genes providing the instructions (transcripts) for making proteins. Our cells become specialised by controlling which of those genes are “on” or “off”, and how much transcript “on” genes can produce. Each cell type therefore has a specific “transcriptomic profile” which can be observed, measured and manipulated to understand its regulation, plasticity and potential. Crucially for research into cancers (and other diseases), we can compare the profile of normal cells to cancers to understand what has gone wrong, and to identify particular processes which could be targeted therapeutically.",
                className="card-text-1"
            ),
            html.P(
                "The Jack Birch Unit for Molecular Carcinogenesis began to profile the urothelial (bladder and ureter) transcriptomes in the early 2000s. This was accelerated through The Astellas European Foundation Prize in Urology awarded to Professor Jennifer Southgate and Dr Simon Baker in 2010 with the aim of deriving \"The Urotheliome\" - a high resolution transcriptomic map of urothelial differentation and plasticity. We have now developed datasets of urothelial differentiation, stimulations by particular gene regulators and drugs, characterised bladder cancer cell lines, and developed specific transcriptomic signatures of immune activation, viral infection and metabolic dysregulation. These datasets are all interrogated with reference to international bladder cancer cohorts, such as The Cancer Genome Atlas (TCGA) and UROMOL consortia. By working with normal data we are also able to understand which genes are transcribed in urothelium, and which transcripts correspond to immune and muscle contamination of tumours.",
                className="card-text-2"
            ),
            html.P(
                "We have now amassed a large database of RNA sequencing data from hundreds of patients and experimental conditions. This website is a visualisation tool for these data, which has been developed for the academic community to facilitate urothelial research, collaboration, and advancement of FAIR principles in the life sciences. Please contact Dr Andrew Mason (Lecturer in Cancer Informatics within the Jack Birch Unit) to discuss bioinformatic analysis beyond visualisation, including opportunities for new collaborations.",
                className="card-text-3"
            ),
        ]),
        className="mb-4 shadow-sm"
    )
    
    # Usage guide section
    guide_section = dbc.Card(
        dbc.CardBody([
            html.H3("How to Use", className="card-title text-primary"),
            html.P("Follow these steps to get started with exploring Urotheliome data:"),
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.Strong("1. Navigate to the Gene Explorer: "),
                    "Click on 'Gene Explorer' in the navigation bar to access the interactive visualization tools."
                ]),
                dbc.ListGroupItem([
                    html.Strong("2. Select genes of interest: "),
                    "Use the searchable dropdown menu to select the gene you wish to analyze."
                ]),
                dbc.ListGroupItem([
                    html.Strong("3. Choose visualization options: "),
                    "Select the desired plot type (box, points, or violin) and axis variables."
                ]),
                dbc.ListGroupItem([
                    html.Strong("4. Compare specific genes: "),
                    "Use the Gene Comparison tab to directly compare expression patterns between two selected genes."
                ]),
            ]),
        ]),
        className="mb-4 shadow-sm"
    )
    
    # Logo section - now positioned at the bottom with alternating heights
    partners_heading = html.H3("Supported by", className="text-primary text-center mt-5 mb-5")
    
    # Top row with 1 logo (taller)
    logo_row_top = dbc.Row([
        dbc.Col(html.Img(src="/assets/Logos/YAC-logo-long.png", className="img-fluid", style={"height": "110px", "padding": "10px"}, alt="York Against Cancer logo"), 
                width="auto", className="text-center mx-5"),   
    ], justify="center", align="center", className="mb-4")
    
    # Bottom row with 4 logos (shorter)
    logo_row_bottom = dbc.Row([
        dbc.Col(html.Img(src="/assets/Logos/ybri-white-logo.png", className="img-fluid", style={"height": "70px", "background-color": "gray", "padding": "0px"}, alt="York Biomedical Research Institute logo"), 
                width="auto", className="text-center mx-5"),
        dbc.Col(html.Img(src="/assets/Logos/york-biology-logo.jpg", className="img-fluid", style={"height": "70px"}, alt="University of York Biology Department logo"), 
                width="auto", className="text-center mx-5 px-4"),
        dbc.Col(html.Img(src="/assets/Logos/ukri-bbsrc-square-logo.png", className="img-fluid", style={"height": "70px"}, alt="UKRI BBSRC funding logo"), 
                width="auto", className="text-center mx-5 px-4"),
        dbc.Col(html.Img(src="/assets/Logos/Astellas-logo.svg", className="img-fluid", style={"height": "70px", "padding": "0px"}, alt="Astellas Pharma logo"), 
                width="auto", className="text-center mx-5"),
    ], justify="center", align="center", className="mb-5")
    
    return html.Div([
        dbc.Container([
            html.H1("Welcome to the Urotheliome Project", 
                   className="text-center my-4 text-primary"),
            
            dbc.Row([
                dbc.Col([mission_section], md=12)
            ]),
            
            dbc.Row([
                dbc.Col([guide_section], md=12)
            ]),
            
            partners_heading,
            logo_row_top,
            logo_row_bottom
        ], style=container_style),
    ]) 