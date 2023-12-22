from flask import Flask, render_template, request, send_file, redirect
from conversores.conversores import conversor_vale_transporte_file, conversor_insalubridade

app = Flask(__name__)



@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vale-transporte')
def vale_transporte():
    return render_template('vale-transporte.html')

@app.route('/insalubridade')
def insalubridade():
    return render_template('insalubridade.html')

@app.route('/vale-alimentacao')
def vale_alimentacao():
    return render_template('vale-alimentacao.html')


@app.route('/upload-transporte', methods=['POST'])
def upload_vale_transporte():
    return processar_vt(conversor_vale_transporte_file)

@app.route('/upload-insalubridade', methods=['POST'])
def upload_insalubridade():
    return processar_insalubridade(conversor_insalubridade)

@app.route('/upload-alimentacao', methods=['POST'])
def upload_alimentacao():
    return processar_alimentacao(conversor_insalubridade)

def processar_vt(funcao_processamento):
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    # Chame a função de processamento específica
    output_buffer = funcao_processamento(file)

    # Envie o arquivo convertido para o usuário
    return send_file(output_buffer, download_name='Vale_Transporte.xml', as_attachment=True)

def processar_insalubridade(funcao_processamento):
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    # Chame a função de processamento específica
    output_buffer = funcao_processamento(file)

    # Envie o arquivo convertido para o usuário
    return send_file(output_buffer, download_name='Insalubridade.txt', as_attachment=True)

def processar_alimentacao(funcao_processamento):
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    # Chame a função de processamento específica
    output_buffer = funcao_processamento(file)

    # Envie o arquivo convertido para o usuário
    return send_file(output_buffer, download_name='Alimetacao.csv', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)