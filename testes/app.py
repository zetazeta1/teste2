try:
    import requests
    import time
    from flask import Flask,render_template,request,jsonify
    import json
    from datetime import datetime
    import pytz
    import pandas as pd
    import base64
    from solders.signature import Signature
    from solders.pubkey import Pubkey
    from solders.message import Message
    from solders.hash import Hash
    import os
    import random
    import string
    
    app=Flask(__name__)

    @app.route('/')
    def index():
        return render_template('menu.html')
    @app.route('/cad')
    def cadastro():
       
        return render_template('cadastro.html')
        
    @app.route('/pags')
    def pagamentos():
        qry=request.args.get('q')
        val=request.args.get('v')
        if qry=="mpay":
            url='solana:89BBgM9DZSgMUSkc3zptNzXw7Zt7tjgJyUVx4RrkXBzW?amount='+str(val).replace('Preço:','')+'&spl-token=SOL&network=devnet'
            return render_template('pagamento.html',link=url,valor=str(val))


    @app.route('/reg')
    def registro():
        def rgs():
            mtx=[]
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/imgs.json", "r") as arquivo2:
                dadosI = json.load(arquivo2)
            mtxI=[]
            for i in range(len(dadosI)):
                mtxI.append(dadosI[str(i+1)])

            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "r") as arquivo:
                dados = json.load(arquivo)
                if dados!={}:
                    prods = list(dados.keys())
                    val = list(dados.values())
                    for i in range(len(val)):
                        mtx.append(['Produto:'+prods[i],'Preço:'+val[i]])
            return {"regs":mtx,"imgs":mtxI}
            #solana:89BBgM9DZSgMUSkc3zptNzXw7Zt7tjgJyUVx4RrkXBzW?amount=0.08&network=devnet&label=Minha%20Loja&message=Pagamento%20da%20compra
            #solana:https://solanapay.com/pay/89BBgM9DZSgMUSkc3zptNzXw7Zt7tjgJyUVx4RrkXBzW?amount=0.08

        
            
         
        return render_template('prods.html',**rgs())
    
    @app.route('/src')
    def src():
        qry=request.args.get('q')
        mtxn=[]
        mQry=qry.split('E')
        for z in range(len(mQry)):
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "r") as arquivo:
                sQry=mQry[z]
                dados = json.load(arquivo)
                prods = list(dados.keys())
                val = list(dados.values())
                for i in range(len(prods)):
                    strProds=prods[i].split(' ')
                    for w in range(len(strProds)):
                        if strProds[w]==sQry:
                            mtxn.append(i)
            def rgs():
                mtx=[]
                with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/imgs.json", "r") as arquivo2:
                    dadosI = json.load(arquivo2)
                mtxI=[]
                for i in range(len(dadosI)):
                    mtxI.append(dadosI[str(i+1)])

                with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "r") as arquivo:
                    dados = json.load(arquivo)
                    if dados!={}:
                        prods = list(dados.keys())
                        val = list(dados.values())
                        for i in range(len(val)):
                            mtx.append(['Produto:'+prods[i],'Preço:'+val[i]])
                return {"regs":mtx,"imgs":mtxI}
        return render_template('prods.html',**rgs())


            


        pass        

    @app.route('/create', methods=['POST'])
    def create():
        if request.referrer!='/reg':
            prod=request.form['prod']
            val=request.form['val']
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "r") as arquivo:
                dados = json.load(arquivo)
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/imgs.json", "r") as arquivo2:
                dadosI = json.load(arquivo2)
            dados[prod]=str(val)
            file = request.files["img"]
            if file.filename!="":
                file.save("C:/Users/lucas/Downloads/Projetos/MyBC&T/static/"+file.filename)
                dadosI[str(len(dadosI)+1)]=file.filename
            else:
                dadosI[str(len(dadosI)+1)]="N"
            mtxI=[]
            for i in range(len(dadosI)):
                mtxI.append(dadosI[str(len(dadosI))])

        
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/imgs.json", "w", encoding="utf-8") as arquivo2:
                json.dump(dadosI, arquivo2, indent=4, ensure_ascii=False)
            def rgs():
                mtx=[]

                with open("C:/Users/lucas/Downloads/Projetos/MyBC&T/regs.json", "r") as arquivo:
                    dados2 = json.load(arquivo)
                    if dados2!={}:
                        prods = list(dados2.keys())
                        val = list(dados2.values())
                        for i in range(len(val)):
                            mtx.append(['Produto:'+prods[i],'Preço:'+val[i]])
                return {"regs":mtx}

        return render_template('prods.html',**rgs(),imgs=mtxI)

    challenges = {}
    

    # 🛠️ Função para gerar um challenge aleatório
    def generate_challenge():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    @app.route("/get_challenge", methods=["POST"])
    def get_challenge():
        """ Retorna um challenge aleatório para o usuário assinar. """
        data = request.get_json()
        pubkey = data.get("pubkey")

        if not pubkey:
            return jsonify({"error": "Chave pública não fornecida"}), 400

        challenge = generate_challenge()
        challenges[pubkey] = challenge  # Salva temporariamente

        return jsonify({"challenge": challenge})

    @app.route("/verify_signature", methods=["POST"])
    def verify_signature():
        if request.referrer=='/verif':
            pass
        """ Verifica se a assinatura é válida para o challenge enviado. """
        data = request.get_json()
        pubkey = data.get("pubkey")
        signature_b64 = data.get("signature")

        if not pubkey or not signature_b64:
            print('erro')
            return jsonify({"error": "Dados incompletos"}), 400

        challenge = challenges.get(pubkey)

        if not challenge:
            print('erro')
            return jsonify({"error": "Challenge não encontrado"}), 400

        try:
            # Converter chave pública e assinatura para objetos da Solana
            pubkey_obj = Pubkey.from_string(pubkey)
            signature_bytes = base64.b64decode(signature_b64)
            signature_obj = Signature.from_bytes(signature_bytes)

            # Verificar a assinatura
            is_valid = signature_obj.verify(pubkey_obj, challenge.encode())


            if is_valid:
                return jsonify({"status": "success", "url1": "/reg?"+str(pubkey_obj),"url2":'/pags'}), 200
        
        


            else:
                print('erro')
                return jsonify({"error": "Assinatura inválida"}), 401
        except Exception as e:
            print(f'erro:{e}')

    @app.route("/verify_signature2", methods=["POST"])
    def verify_signature2():
        """ Verifica se a assinatura é válida para o challenge enviado. """
        data = request.get_json()
        pubkey = data.get("pubkey")
        signature_b64 = data.get("signature")

        if not pubkey or not signature_b64:
            print('erro')
            return jsonify({"error": "Dados incompletos"}), 400

        challenge = challenges.get(pubkey)

        if not challenge:
            print('erro')
            return jsonify({"error": "Challenge não encontrado"}), 400

        try:
            # Converter chave pública e assinatura para objetos da Solana
            pubkey_obj = Pubkey.from_string(pubkey)
            signature_bytes = base64.b64decode(signature_b64)
            signature_obj = Signature.from_bytes(signature_bytes)

            # Verificar a assinatura
            is_valid = signature_obj.verify(pubkey_obj, challenge.encode())


            if is_valid:
                return jsonify({"status": "success", "redirect_url": "solana:89BBgM9DZSgMUSkc3zptNzXw7Zt7tjgJyUVx4RrkXBzW?amount=0.08&network=devnet"}), 200
                


            else:
                print('erro')
                return jsonify({"error": "Assinatura inválida"}), 401

        except Exception as e:
            print(f'erro:{e}')
        finally:
            print('Pressione enter para sair ')


    if __name__ == '__main__':
        app.run(debug=True)
except Exception as e:
    print(f'erro:{e}')
finally:
    print('Pressione enter para sair ')
