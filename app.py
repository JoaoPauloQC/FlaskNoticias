from flask import Flask, render_template, url_for, request, make_response, redirect


app = Flask(__name__)


users = {
    'joao': 2708,
    'vih': 305,
    'sofia': 2709,
}


dark = "none"


newsdict = {
    #     Title         : [ category , main link , img link ]
    'Mundial de Clubes': ['sport', 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.lance.com.br%2Fmundial-de-clubes%2Fconfira-os-times-classificados-e-ranking-para-o-mundial-de-clubes-de-2029.html&psig=AOvVaw3mwoQ3RZn3CI8ha1S7EhC&ust=1751997320970000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCLiH-uGoq44DFQAAAAAdAAAAABAE', 'https://lncimg.lance.com.br/cdn-cgi/image/width=950,quality=75,fit=pad,format=webp/uploads/2025/07/AFP__20250601__2218051340__v1__HighRes__LosAngelesFootballClubVClubAmericaFifaClubWo-scaled-aspect-ratio-512-320-1.jpg'],
    'Cidade cria aeroporto para OVNIs': ['geral', 'https://g1.globo.com/mt/mato-grosso/noticia/2025/07/13/luzes-estranhas-civilizacao-perdida-dia-do-et-por-que-cidade-em-mt-criou-ate-aeroporto-para-ovnis.ghtml', 'https://s2-g1.glbimg.com/k___F22qd1xPFuHRk7Bv6cFVoPg=/0x0:1920x1080/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/n/N/n3tCkNQAaAmhN6qfjaaA/barra-do-garca-mt-ets.jpg'],
    'Estevão no Chelsea?': ['sport', 'https://www.google.com/imgres?q=estevao%20chelsea&imgurl=https%3A%2F%2Fuploads.metroimg.com%2Fwp-content%2Fuploads%2F2025%2F07%2F04235909%2Festevao-palmeiras-chelsea-copa-do-mundo-de-clubes.jpg&imgrefurl=https%3A%2F%2Fwww.metropoles.com%2Fesportes%2Festevao-pode-jogar-pelo-chelsea-no-mundial-de-clubes-descubra&docid=cDA0qeH2VyPzTM&tbnid=DBmRcSHvakTXwM&vet=12ahUKEwjrt4OFtKuOAxUxALkGHbrAC14QM3oECBoQAA..i&w=2400&h=1684&hcb=2&ved=2ahUKEwjrt4OFtKuOAxUxALkGHbrAC14QM3oECBoQAA', 'data:image/jpeg;base64,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'],
    'Avião de pequeno porte cai em aeroporto em londres': ['geral', 'https://g1.globo.com/mundo/noticia/2025/07/13/aviao-de-pequeno-porte-cai-em-aeroporto-nos-arredores-de-londres.ghtml', 'https://fly.metroimg.com/upload/q_85,w_700/https://uploads.metroimg.com/wp-content/uploads/2025/07/13135858/Aviao-de-pequeno-porte-cai-no-aeroporto-de-Londres.jpg'],
    'PSG ganha do Real Madrid no mundial de clubes': ['sport', 'https://ge.globo.com/futebol/mundial-de-clubes/jogo/09-07-2025/parissaintgermain-realmadrid.ghtml', 'https://s2-ge.glbimg.com/b85_kU9Q-rgnmphZTQ1NmIN3pJc=/0x0:4783x2691/640x360/smart/https://i.s3.glbimg.com/v1/AUTH_bc8228b6673f488aa253bbcb03c80ec5/internal_photos/bs/2025/z/v/5c5UghRhuOlS7rzQtYgQ/gettyimages-2224327324.jpg'],
    'Trump anuncia aumento de tarifa nas importações': ['economia', 'https://g1.globo.com/economia/noticia/2025/07/12/trump-tarifas.ghtml', 'https://s2-g1.glbimg.com/xDUyrY-Z2ROHumNl2zsM-wsTrhY=/0x0:5500x3697/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/q/1/MLCjh9RJ26dNJwH54OUQ/2025-06-22t022319z-1477768578-rc2e7fatvext-rtrmadp-3-iran-nuclear.jpg'],
    'Comportamento decepcionante do Balanço Geral RJ': ['geral', 'https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://oglobo.globo.com/play/noticia/2025/07/04/nota-0-o-comportamento-do-apresentador-do-balanco-geral-rj-apos-abrir-uma-enquete.ghtml&ved=2ahUKEwjJ_960tKuOAxVmDrkGHep7NW0QxfQBKAB6BAgIEAE&usg=AOvVaw0cNT8XtyfmVmKfZxHlKlam', 'data:image/jpeg;base64,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'],
    'IA pode acabar com até 92 milhões de empregos': ['tecnologia', 'https://g1.globo.com/trabalho-e-carreira/noticia/2025/07/13/ia-pode-eliminar-ate-92-milhoes-de-empregos-mas-essas-profissoes-devem-sobreviver.ghtml',  'https://s2-g1.glbimg.com/KGrnH-rnrj1WYMXeKVnWwxT0VmE=/0x0:1200x525/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/x/b/dWwp2RQwO4fogDeOmvSQ/72575862-1004-1-.webp'],
    'Entenda os sinais que ansiedade causa na mente e no corpo': ['saude', 'https://g1.globo.com/saude/bem-estar/noticia/2025/07/13/sintomas-de-ansiedade-entenda-os-sinais-fisicos-e-mentais.ghtml', 'https://s2-g1.glbimg.com/1MiHjelkcn3KkT4fe2L1gz5nVIc=/0x0:5011x3341/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/H/q/KJrAzaTxSxuEYCjLa5eQ/retrato-de-um-homem-na-mesa-perto-laptop-tarde-da-noite.jpg'],
    'Veja como e onde encontrar rios escondidos em SP': ['geral', 'https://g1.globo.com/sp/sao-paulo/noticia/2025/07/13/veja-onde-encontrar-rios-escondidos-na-cidade-de-sp.ghtml', 'https://s2-g1.glbimg.com/NqfhgIfDesYyql8Hkn0isd3DXV0=/0x0:4160x3120/1000x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/W/6/gy1BOLRz62d4LVgwfAwg/nascente-saracura.jpeg'],
    'Conheça a famosa cirurgia que aumenta sua estatura': ['geral', 'https://g1.globo.com/sp/campinas-regiao/noticia/2025/07/13/alongamento-osseo-conheca-cirurgia-que-coloca-haste-eletronica-no-osso-e-faz-a-perna-crescer-ate-8-centimetros.ghtml', 'https://s2-g1.glbimg.com/Un2m6b45nHWW5l9LJJrLG9NRDrs=/0x0:1615x905/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/Q/a/IxxgizSTqaW1sKAMO7RQ/screenshot-6.jpg'],
    'Drástica mudança das vaquejadas graças as bets': ['geral', 'https://g1.globo.com/politica/noticia/2025/07/13/bets-mudam-vaquejadas-no-nordeste-e-transformam-vaqueiros-em-influencers-de-jogos-de-azar.ghtml', 'https://s2-g1.glbimg.com/A0NNj1-DGgjfClWATdhoGrIZ_F4=/0x98:681x605/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2025/F/i/9AAl4cTCyBG2u2l7u2AQ/captura-de-tela-2025-07-10-185653.png']
}


@app.route("/")
def login_page():
    if request.cookies.get('username'):
        if request.cookies.get('times'):
            times = int(request.cookies.get('times'))
            resp = make_response(redirect(url_for('news')))
            resp.set_cookie('times', str(times+1))
            return resp
        else:
            resp = make_response(redirect(url_for('news')))
            resp.set_cookie('times', "1")
            return resp
    return render_template("login_page.html")

@app.route("/signin", methods=['POST'])
def signin():
    name = request.form['name']
    if name in users:
        password = int(request.form['password'])
        if users[name] == password:
            resp = make_response(redirect(url_for('news')))
            resp.set_cookie('username', name)
            return resp
    return redirect(url_for('login_page'))

@app.route('/byecookies')
def byecookies():
    resp = make_response(redirect(url_for('login_page')))
    resp.delete_cookie('username')
    resp.delete_cookie('dark')
    return resp

@app.route('/getcookies')
def cookies():
    return request.cookies

@app.route('/home')
def news():
    sendnews = []
    for i in newsdict:
        newdict = {
            'name': i,
            'link': newsdict[i][1],
            'img': newsdict[i][2]
        }
        sendnews.append(newdict)
    if request.cookies.get('dark'):
        dark = request.cookies.get('dark')
    else:
        dark = ''
    return render_template('home.html', news=sendnews, dark=dark, user=request.cookies.get('username'))

@app.route('/darkmode')
def darkmode():
    if request.cookies.get('dark'):
        resp = make_response(redirect(url_for("news")))
        resp.delete_cookie('dark')
        return resp
    else:
        resp = make_response(redirect(url_for("news")))
        resp.set_cookie('dark', 'dark', max_age=1800)
        return resp

@app.route('/filter', methods=['POST'])
def filter():
    filterctg = request.form['ctg']
    if request.cookies.get('dark'):
        dark = request.cookies.get('dark')
    else:
        dark = ''
    if filterctg == 'todas':
        return redirect(url_for('news'))

    sendnews = []
    for i in newsdict:
        if newsdict[i][0] == filterctg:
            new = {
                'name': i,
                'link': newsdict[i][1],
                'img': newsdict[i][2]
            }
            sendnews.append(new)

    return render_template('home.html', news=sendnews, dark=dark, user=request.cookies.get('username'))

if __name__ == '__main__':
    app.run(debug=True)