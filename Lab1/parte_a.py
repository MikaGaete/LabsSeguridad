import utils

ENCODER = ("cc5327.hackerlab.cl", 5312)

encoder_input, encoder_output = utils.create_socket(ENCODER)

for i in range(73):
    try:
        resp = utils.send_message(encoder_input, encoder_output, "0" * i)
        print(f"{i} ceros, largo del mensaje cifrado recibido: {len(resp)}")
    except Exception as e:
        print(e)
        print("Closing...")
        encoder_input.close()
        break