import datetime as dt
import pandas as pd
from getpass import getpass
from report_generator.html_tools import banner, color_map, data_url
from report_generator.smtp import sendHTMLmailwithattachments, set_credentials, set_password

# TEsting
config_map = {
    'team1': ('Team Name','Sales & Marketing','blue')
}


class Report:
    def __init__(self, team, title):
        assert team in config_map.keys(), f"{team} is not found in config_map"
        self.team = team
        self.title = title
        self.widgets = []
        self.attachments = []

    def add(self,widget,header=""):
        if type(widget) == pd.DataFrame:
            html = widget.to_html(classes='report')
        else:
            html = f"{widget}<br>"
        if header != "":
            html = f'<h2>{header}</h2>{html}'
        self.widgets.append(html)

    def add_image(self,file_name,header=""):
        name = 'attachment' + str(len(self.attachments))
        self.attachments.append({
            'name': name,
            'filename': file_name
        })
        html = f"<img src='cid:{name}'>"
#        html = f"<img src='{data_url(file_name)}'>"
        self.add(html, header)


    def to_html(self):
        date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        config = config_map[self.team]
        body = "\n".join(self.widgets)
        color = color_map()[config[2]]
        html = banner(date,self.title,config[0],config[1],'',color,body=body)
        return html

    def save(self):
        html = self.to_html()
        with open('./report_generator/test.html','w') as f:
            f.write(html)
    
    def send(self, sender, to):
        body = self.to_html()
        subject = self.title
        sendHTMLmailwithattachments(sender, to, subject, body, attachments=self.attachments)

if __name__ == "__main__":
    report = Report('team1',"Fancy report")
    report.add("This is a test","Header of this section")
    report.add("This is another test", "Header of another section")
    report.add_image('./report_generator/spmini.png', "Sample image")
    report.add(pd.read_csv('http://bit.ly/drinksbycountry').head(15), "Sample dataframe")
    sender = 'sender@gmail.com'
    #set_password()
    set_credentials('smtp.gmail.com',sender,sender)
    #report.send(sender,[sender])
    report.save()
