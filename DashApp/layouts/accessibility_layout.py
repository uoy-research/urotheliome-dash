from dash import html
import dash_bootstrap_components as dbc

def accessibility_layout() -> html.Div:
    """
    Create the accessibility statement layout
    Returns:
        Dash HTML Div containing the accessibility statement
    """
    # Common styles
    container_style = {"max-width": "1200px"}
    
    return html.Div([
        dbc.Container([
            # Page Header
            html.H1("Accessibility", className="mb-4"),
            
            # Accessibility Statement Section
            html.H2("Urotheliome Accessibility Statement", className="h3 mb-3"),
            
            html.P([
                "The University of York is committed to making its websites accessible, in accordance with the Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility Regulations 2018."
            ], className="lead"),
            
            html.P("This accessibility statement applies to the Urotheliome dashboard."),
            
            # Compliance Status
            html.H3("Compliance status", className="h4 mt-4 mb-3"),
            html.P("This website is fully compliant with the Web Content Accessibility Guidelines (WCAG) version 2.2 AA standard."),
            
            # Preparation Statement
            html.H3("Preparation of this accessibility statement", className="h4 mt-4 mb-3"),
            html.P("This statement was prepared on 5th June 2025."),
            
            html.P("We used a combination of methods to check the site:"),
            
            # Testing Methods
            html.H4("Accessibility Evaluation Tools", className="h5 mt-3 mb-2"),
            html.P("Used to scan a number of sample pages and highlight accessibility issues:"),
            html.Ul([
                html.Li("WAVE Web Accessibility Evaluation Tool"),
                html.Li("Chrome Lighthouse"),
            ]),
            
            # html.H4("Manual Testing", className="h5 mt-3 mb-2"),
            # html.P("We used an accessibility checklist to manually check a representative sample of pages from across our website, this included:"),
            # html.Ul([
            #     html.Li("Testing with the Apple VoiceOver screen reader"),
            #     html.Li("Manually testing site navigation by only using the keyboard"),
            #     html.Li([
            #         "Testing with high contrast mode enabled. To test this we used a Windows 10 operating system with 'black high contrast' mode enabled, using a Google Chrome browser with the ",
            #         html.A("High contrast extension", href="https://chrome.google.com/webstore/detail/high-contrast/djcfdncoelnlbldjfhinnjlhdjlikmph", target="_blank"),
            #         " enabled"
            #     ])
            # ]),
            
            # Feedback Section
            html.H3("Feedback and contact information", className="h4 mt-4 mb-3"),
            html.P([
                "If you find any problems or think we're not meeting accessibility requirements, please contact ",
                html.A("itsupport@york.ac.uk", href="mailto:itsupport@york.ac.uk"),
                "."
            ]),
            
            html.P([
                "If you are unable to access content on this website and require the information from this website to be provided in an alternative format, please contact ",
                html.A("itsupport@york.ac.uk", href="mailto:itsupport@york.ac.uk"),
                "."
            ]),
            
            # Enforcement Section
            html.H3("Enforcement procedure", className="h4 mt-4 mb-3"),
            html.P([
                "The Equality and Human Rights Commission (EHRC) is responsible for enforcing the Public Sector Bodies (Websites and Mobile Applications) (No. 2) Accessibility Regulations 2018 (the 'accessibility regulations')."
            ]),
            
            html.P([
                "If you're not happy with how we respond to your complaint, contact the ",
                html.A("Equality Advisory and Support Service (EASS)", 
                      href="https://www.equalityadvisoryservice.com/", 
                      target="_blank"),
                "."
            ]),
            
        ], style=container_style, className="py-4"),
    ]) 