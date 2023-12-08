import base64

def get_css(color):
    font = '"Calibri", Arial, Helvetica, sans-serif' 
    return f"""
    body                         {{ font-family: "Calibri"; font-size: 10pt; padding: 2px 7px; }}
    p, h2, h3, h4, h5, h6, TD    {{ {font} }}
    h1                           {{ {font}; color:#{color}; border-bottom: solid 1px }}
    .dateheader {{ padding-left: 1pt; font-size:14pt }}
    .underline  {{ border-bottom: solid 1px; margin-bottom:20pt; padding-bottom: 5pt; color: #{color} }}
    .report thead tr {{ background-color: #{color}; color: white }}
    .report {{ border-collapse: collapse; margin: 10px; }}
    .banner{color}     {{ 
        $FONT; 
        background-color: #{color}; 
	color: #ffffff; 
	font-size: 16pt; 
	padding: 5pt 10pt; 
	text-align: left; 
	background: linear-gradient(45deg, #{color}, #{color}55); 
    }}
    
    """


def banner(date, title, banner_title, banner_subtitle, imagelink, color, body = ""):
    style = get_css(color)
    return f"""
    <html>
<Title>{title}</Title>
        <head>
            <style>{style}</style>
        </head>
        <body>

<table style='width: 100%'><tr>
	<td style='width:85px'><img align=left src='{imagelink}' height=70></td>
	<td  class=banner{color}><B>{banner_title}</B><BR><font-size=-1>{banner_subtitle}</font></td>
	</tr>
</table>
<br>		
<a class=dateheader>{date}</a><BR>
<div class='dateheader underline'><b>{title}</b></div>
{body}
</body>
</html>
"""

def encode_image(filename):
    encoded_string = ""
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        file = encoded_string
    return file.decode('ascii')

def data_url(filename):
    return f'data:image/gif;base64,{encode_image(filename)}'

def color_map():
    return \
    {
        'blue': '125AAA',
    #    'blanchedalmond': 'FFEBCD',
        'brown': 'A52A2A',
        'cadetblue': '5F9EA0',
        'chocolate': 'D2691E',
    #    'cornsilk': 'FFF8DC',
        'crimson': 'DC143C',
        'darkblue': '00008B',
        'darkmagenta': '8B008B',
        'darkorchid': '9932CC',
        'darkgreen': '006400',
        'darkslateblue': '483D8B',
        'darkslategray': '2F4F4F',
        'firebrick': 'B22222',
        'indigo': '4B0082',
        'orangered': 'FF4500',
        'teal': '008080',
        'gold': 'FFD700'
    }


if __name__ == "__main__":
    date,title,banner_title, banner_subtitle = 'Monday, July 6th 2020', 'Fancy sales report', 'Team Name', 'Sales & Marketing'
    imagelink, color = '', '125aaa'

    colors = color_map()
    with open(f'output/test-all.html','w') as f:
       for name,color in colors.items():
          print(color, name)
          html = banner(date,title,banner_title , f"{banner_subtitle} - theme = {name}",  imagelink,  color)
          f.write(html)
        

    for name,color in colors.items():
       with open(f'output/test-{name}.html','w') as f:
          print(color, name)
          html = banner(date,title,banner_title, banner_subtitle,  imagelink,  color)
          f.write(html)
