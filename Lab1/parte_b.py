import utils

ENCODER = ("cc5327.hackerlab.cl", 5312)
DECODER = ("cc5327.hackerlab.cl", 5313)

encoder_input, encoder_output = utils.create_socket(ENCODER)
decoder_input, decoder_output = utils.create_socket(DECODER)

for i in range(25):
    try:
        print(f"Mensaje enviado: {'0' * i}")
        resp = utils.send_message(encoder_input, encoder_output, "0" * i)
        print(f"Codificación recibida: {resp}")
        resp2 = utils.send_message(decoder_input, decoder_output, resp)
        print(f"Decodificación recibida: {resp2}\n")

    except Exception as e:
        print(e)
        print("Closing...")
        encoder_input.close()
        break