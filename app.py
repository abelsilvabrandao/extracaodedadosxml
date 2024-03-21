from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import re
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/processar-xml', methods=['POST'])
def process_xml():
    try:
        xml_file = request.files['xml_file']
        if xml_file.filename == '':
            return 'Nenhum arquivo selecionado', 400

        xml_str = xml_file.read().decode('utf-8')

        root = ET.fromstring(xml_str)
        inf_adic = root.find('.//{http://www.portalfiscal.inf.br/nfe}infAdic')
        inf_cpl = inf_adic.find('.//{http://www.portalfiscal.inf.br/nfe}infCpl')

        texto_inf_cpl = inf_cpl.text

        di_match = re.search(r'DI (\d+-\d+)', texto_inf_cpl)
        navio_match = re.search(r'NAVIO (\w+(?: \w+)*)', texto_inf_cpl)

        if di_match:
            di = di_match.group(1)
            di_qr_code = generate_qr_code(di)
        else:
            di = "DI não encontrado - Xml fora do Padrão"
            di_qr_code = ""

        if navio_match:
            navio = navio_match.group(1)
            navio_qr_code = generate_qr_code(navio)
        else:
            navio = "Navio não encontrado - Xml fora do Padrão"
            navio_qr_code = ""

        return render_template('result.html', di=di, di_qr_code=di_qr_code, navio=navio, navio_qr_code=navio_qr_code)
    except Exception as e:
        return f"Erro ao processar o XML: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)



