#!/usr/bin/python

import numpy as np
import reedsolo as rs
import argparse


def combine_bits(bytes_to_bin):
    return [str(x)+str(y) for x, y in zip(bytes_to_bin[0::2], bytes_to_bin[1::2])]


def mapper(to_be_mapped, mapping):
    return [mapping[b] for b in to_be_mapped]


def pack_bits(bit_pairs):
    return np.packbits([int(char) for ele in bit_pairs for char in ele])


def encode(in_str, ecsymbols, e_mapping):
    if not type(in_str) == bytes:
        in_str = bytes(in_str, 'utf8')
    rsc = rs.RSCodec(ecsymbols)
    barray = rsc.encode(in_str)
    combined_bits = combine_bits(np.unpackbits(barray))
    return mapper(combined_bits, e_mapping)


def decode(in_list, ecsymbols, d_mapping):
    assert all([type(ele) == str and ele in ['0', '1', '2', '3'] for ele in in_list]), \
            "Input has to be a list of strings comprised of the symbols '0', '1', '2' and '3'."
    rsc = rs.RSCodec(ecsymbols)
    bit_pairs = mapper(in_list, d_mapping)
    pbits = pack_bits(bit_pairs)
    return rsc.decode(pbits, ecsymbols)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='En- or Decode a string to a quaternary representation using Reed-Solomon as error-correction.')
    parser.add_argument('--encode', '-e', dest='encode', action='store_true',
                        help='Encode a string.')
    parser.add_argument('--decode', '-d', dest='decode', action='store_true',
                        help='Decode a list of quaternary symbols.')
    parser.add_argument('--ecsymbols', '-ec', dest='ecsymbols',  type=int, action='store',
                        help='The amount of error correction symbols to be used for encoding / the message was encoded with (decoding).')
    parser.add_argument('--input', '-i', dest='infile', type=str, action='store',
                        help='Input file for en-/decoding (plain textfile)')
    parser.add_argument('--output', '-o', dest='outfile', type=str, action='store',
                        help='Output file for en-/encoding (plain textfile)')
    args = parser.parse_args()

    if not args.ecsymbols:
        parser.error("Need number of error correction symbols.")
    if args.encode and not args.outfile:
        parser.error("Missing output file path for the encoded file.")
    if args.encode and args.decode:
        parser.error("Can only either encode or decode.")
    if args.decode and not args.infile:
        parser.error("Missing input file path.")
    if args.decode and not args.outfile:
        parser.error("Missing output file path for the decoded file.")
    if args.encode and not args.infile:
        parser.error("Missing input file path.")
    if not args.encode and not args.decode:
        parser.error("Have to set either encoding or decoding.")

    encode_mapping = {"00": "0", "01": "1", "10": "2", "11": "3"}
    decode_mapping = {value: key for key, value in encode_mapping.items()}

    if args.encode:
        with open(args.outfile, "w") as out, open(args.infile, "r") as inf:
            inp = bytes(inf.read(), 'utf8')
            enc = encode(inp, args.ecsymbols, encode_mapping)
            out.write("".join(enc))
        print("Encoding finished, file can be found under " + args.outfile)

    elif args.decode:
        with open(args.outfile, "w") as out, open(args.infile, "r") as inf:
            inp = list(inf.read())
            dec = decode(inp, args.ecsymbols, decode_mapping)
            out.write(dec[0].decode("utf8"))
        print("Decoded text: " + dec[0].decode("utf8"))
        print("Decoded text with error correction symbols: " + dec[1].decode("utf8"))
        print("Errors corrected: " + str(len(dec[2])))
        print("Decoding finished, file can be found under " + args.outfile)



