from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse

from twilio.rest import Client
import requests
app = Flask(__name__)

sid = "AC8bdafcb272a9a9d62df9a93a38757436"
auth = "3b25682626e159fc55ab64eecdd4058e"

whatsapp_client = Client(sid,auth)

def singleMessage(string, from_number):
    '''Function used to send whatsapp message with a simpler syntax'''
    whatsapp_client.messages.create(body=string,
                                    from_= "whatsApp:+14155238886",
                                    to = from_number)

@app.route('/bot', methods=['POST'])
def bot():
    #session.clear()
    from_number = str(request.values.get("From"))
    body = request.values.get('Body', '').lower()
    counter = session.get("counter", 0)
    counter += 1
    session["counter"] = counter
    resp = MessagingResponse()

    if (session["counter"] == 1 and body != "salir"):
        session["messages"] = []
        session["messages"].append(body)
        print(session["messages"])

        singleMessage("¡¡Hola!!. Bienvenido al bot de tasa de cambio. Por favor selecciona alguna de las siguientes opciones:\n 1) Conversión de dólar américano a peso mexicano\n 2) Conversión de peso mexicano a dólar americano", from_number)
        resp.message("")
        return str(resp)
    
    elif len(session["messages"]) >=1:
        user_response = body
        session["messages"].append(user_response)   
        
        if user_response == "salir":
            session.clear()
            resp.message("!Hasta luego!")
            return str(resp)

        else:
            if len(session["messages"]) == 2:
                if(session["messages"][len(session["messages"])-1] == "1"):
                    singleMessage("Por favor ingresa el numero de dólares que deseas convertir", from_number)
                elif(session["messages"][len(session["messages"])-1] == "2"):
                    singleMessage("Por favor ingresa el numero de pesos que deseas convertir", from_number)
                else:
                    singleMessage("Por favor ingresa un número que esté dentro de las opciones (1,2)", from_number)
                    session["messages"].pop(len(session["messages"])-1)
            if len(session["messages"]) == 3:

                response = requests.get("https://tasa-de-cambio.herokuapp.com/latest?base=USD")
                dolar = response.json()["rates"]["MXN"]
                dolar = round(dolar,2)
                peso = 1/response.json()["rates"]["MXN"]
                peso = round(peso,2)
                
                try:

                    if(float(session["messages"][len(session["messages"])-1]) <= 0):
                        singleMessage("Por favor ingresa un numero mayor a 0", from_number)
                        session["messages"].pop(len(session["messages"])-1)

                except:
                    singleMessage("Favor de ingresar un número válido", from_number)
                    session["messages"].pop(len(session["messages"])-1)
                
                if(session["messages"][len(session["messages"])-2] == "1"):

                    singleMessage("La tasa de cambio es: 1 dólar = " + str(dolar) + " pesos mexicanos", from_number)
                    singleMessage("Tus dólares equivalen a " + str(round(float(session["messages"][len(session["messages"])-1]) * dolar,2)) + " pesos", from_number)    

                    singleMessage("Gracias por usar el bot de conversión de moneda, nos vemos!!", from_number)
                    session.clear()

                elif(session["messages"][len(session["messages"])-2] == "2"):
                    singleMessage("La tasa de cambio es: 1 peso mexicano = " + str(peso) + " dólares", from_number)
                    singleMessage("Tus pesos equivalen a " + str(round(float(session["messages"][len(session["messages"])-1]) * peso,2)) + " dólares", from_number)

                    singleMessage("Gracias por usar el bot de conversión de moneda, nos vemos!!", from_number)
                    session.clear()
              
        return str(resp)

    


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug = False, port = 5000)