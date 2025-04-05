import utils

ENCODER = ("cc5327.hackerlab.cl", 5312)
DECODER = ("cc5327.hackerlab.cl", 5313)

encoder_input, encoder_output = utils.create_socket(ENCODER)
decoder_input, decoder_output = utils.create_socket(DECODER)

resp = utils.send_message(encoder_input, encoder_output, "a" * 5)
blocks = utils.split_blocks(utils.hex_to_bytes(resp), 16)

plain_text_blocks = []


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

    for i in range(block_size - 1, -1, -1):
        print("Decrypting Character: ", i)
        padding_value = block_size - i

        for guess in range(256):
            candidate = bytearray(previous_block)

            for j in range(i + 1, block_size):
                candidate[j] = decrypted[j] ^ padding_value

            candidate[i] = guess
            modified_ciphertext = bytes(candidate) + current_block

            if decode(modified_ciphertext):
                decrypted[i] = guess ^ padding_value
                plain_text[i] = decrypted[i] ^ previous_block[i]
                break

    return bytes(plain_text)


for i in range(len(blocks) - 1, -1, -1):
    print("Decripting Block ", i + 1)
    decrypted_block = decrypt_block(current_block=blocks[i], previous_block=blocks[i - 1])
    plain_text_blocks.append(decrypted_block)

plain_text = b"".join(plain_text_blocks)

print("Recovered plain_text:", plain_text)