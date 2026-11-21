from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):
    """View da página inicial que renderiza o template base.html com home.html."""
    content = render_to_string("home.html")
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Albion Market & Craft</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        p {{ color: #666; line-height: 1.6; }}
        .footer {{ margin-top: 40px; text-align: center; color: #999; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>&copy; 2026 Albion Market & Craft - Fase 1 (Infraestrutura)</p>
        </div>
    </div>
</body>
</html>"""
    
    return HttpResponse(html_content, content_type="text/html")