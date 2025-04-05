import utils

ENCODER = ("cc5327.hackerlab.cl", 5312)
DECODER = ("cc5327.hackerlab.cl", 5313)

encoder_input, encoder_output = utils.create_socket(ENCODER)
decoder_input, decoder_output = utils.create_socket(DECODER)

resp = utils.send_message(encoder_input, encoder_output, "a" * 5)
blocks = utils.split_blocks(utils.hex_to_bytes(resp), 16)

def decode(ciphertext: bytes) -> bool:
    hex_modified_block = utils.bytes_to_hex(ciphertext)
    server_response = utils.send_message(decoder_input, decoder_output, hex_modified_block)

    if server_response == "pkcs7: invalid padding (last byte is larger than total length)":
        print(".", end="")
        return False
    if server_response == "pkcs7: invalid padding (last byte does not match padding)":
        print(".", end="")
        return False
    else:
        print("\nServer Response: ", server_response)
        return True


def decrypt_block(current_block: bytes, previous_block: bytes) -> bytes:
    block_size = 16
    decrypted = [0] * block_size
    plain_text = [0] * block_size

    print("Decrypting Character: 15")

    for guess in range(256):
        candidate = bytearray(previous_block)

        for j in range(15 , block_size):
            candidate[j] = decrypted[j] ^ 1

        candidate[15] = guess
        modified_ciphertext = bytes(candidate) + current_block

        if decode(modified_ciphertext):
            decrypted[15] = guess ^ 1
            plain_text[15] = decrypted[15] ^ previous_block[15]
            break

    return bytes(plain_text[15:])

plain_text = decrypt_block(current_block=blocks[len(blocks) - 1], previous_block=blocks[len(blocks) - 2])

print("Recovered plain_text:", plain_text)