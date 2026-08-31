import pdfkit

def convert_email_to_pdf(email_id, html_content, subfolder):
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    print(f'Storing {email_id} to pdf')
    pdfkit.from_string(html_content, f'{subfolder}/{email_id}.pdf', configuration=config)

    