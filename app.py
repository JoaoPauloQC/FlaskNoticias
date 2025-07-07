from flask import Flask,render_template,url_for,request,make_response,redirect

app = Flask(__name__)

users = {

    'joao' : 1234


}

newsdict = {

    'bla1': ['sport','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.lance.com.br%2Fmundial-de-clubes%2Fconfira-os-times-classificados-e-ranking-para-o-mundial-de-clubes-de-2029.html&psig=AOvVaw3mwoiQ3RZn3CI8ha1S7EhC&ust=1751997320970000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCLiH-uGoq44DFQAAAAAdAAAAABAE' , 'https://lncimg.lance.com.br/cdn-cgi/image/width=950,quality=75,fit=pad,format=webp/uploads/2025/07/AFP__20250601__2218051340__v1__HighRes__LosAngelesFootballClubVClubAmericaFifaClubWo-scaled-aspect-ratio-512-320-1.jpg'],
    'bla2': 'sport',
    'bla3': 'geral'


}


@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signin", methods=['POST'])
def signin():
    name = request.form['name']
    if name in users:
        password = int(request.form['password'])
        if users[name] == password:
            return redirect(url_for('news'))
    return redirect(url_for('login_page'))




@app.route('/home')
def news():
    sendnews = []
    for i in newsdict:
        sendnews.append(i)
    return render_template('home.html', news=sendnews)


@app.route('/filter', methods=['POST'])
def filter():
    filterctg = request.form['ctg']
    sendnews = []
    for i in newsdict:
        if newsdict[i][0] == filterctg:
            new = {
                'name': i ,
                'link' : newsdict[i][1]

            }
            sendnews.append(i)
    return render_template('home.html', news=sendnews)



if __name__ == '__main__':
    app.run(debug=True)



