from flask import Flask, request, render_template, redirect, url_for, send_file
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

def parse_xml(xml_str):
    try:
        root = ET.fromstring(xml_str)
        
        # Suponha que aqui você tenha a lógica para analisar o XML e extrair os valores corretamente
        nNF = 'valor_nNF'
        emit_CNPJ = 'valor_emit_CNPJ'
        dest_CNPJ = 'valor_dest_CNPJ'
        produtos = ['valor_produto1', 'valor_produto2']  # Exemplo de lista de produtos
        vProd = 'valor_vProd'
        vNF = 'valor_vNF'

        return nNF, emit_CNPJ, dest_CNPJ, produtos, vProd, vNF
    except Exception as e:
        print(f"Erro ao analisar o XML: {str(e)}")
        # Se ocorrer um erro, retorne valores padrão
        return None, None, None, [], None, None

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

        return redirect(url_for('editar_xml_page', xml_str=xml_str))
    except Exception as e:
        return f"Erro ao processar o XML: {str(e)}", 500

@app.route('/editar-xml-page', methods=['GET', 'POST'])
def editar_xml_page():
    if request.method == 'GET':
        try:
            xml_str = request.args.get('xml_str')
            if xml_str is None:
                return "Erro: XML não fornecido", 400

            nNF, emit_CNPJ, dest_CNPJ, produtos, vProd, vNF = parse_xml(xml_str)
            if nNF is None:
                return "Erro ao abrir o XML para edição: não foi possível analisar o XML", 500
            
            return render_template('edit_xml.html', nNF=nNF, emit_CNPJ=emit_CNPJ, dest_CNPJ=dest_CNPJ, produtos=produtos, vProd=vProd, vNF=vNF)
        except Exception as e:
            return f"Erro ao abrir o XML para edição: {str(e)}", 500
    elif request.method == 'POST':
        try:
            xml_str = request.form['xml_str']
            if xml_str is None:
                return "Erro: XML não fornecido", 400

            # Salva o XML modificado em um novo arquivo temporário
            temp_filename = 'temp.xml'
            if save_xml(xml_str, temp_filename):
                return redirect(url_for('download_xml'))
            else:
                return "Erro ao salvar o XML", 500
        except Exception as e:
            return f"Erro ao salvar o XML: {str(e)}", 500

@app.route('/download-xml')
def download_xml():
    filename = 'temp.xml'
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
