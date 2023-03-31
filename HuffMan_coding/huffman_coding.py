import os
import heapq


class TreeNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def get_freq_dict(self, text):
        frequency = {}

        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def build_heap(self, dic):
        for key in dic:
            node = TreeNode(key, dic[key])
            heapq.heappush(self.heap, node)

    def build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            freq_sum = node1.freq + node2.freq
            new_node = TreeNode(None, freq_sum)
            new_node.left = node1
            new_node.right = node2
            heapq.heappush(self.heap, new_node)
        return

    def build_codes_helper(self, root, curr_bits):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = curr_bits
            self.reverse_codes[curr_bits] = root.char
        self.build_codes_helper(root.left, curr_bits + "0")
        self.build_codes_helper(root.right, curr_bits + "1")

    def build_codes(self):
        root = heapq.heappop(self.heap)
        self.build_codes_helper(root, "")

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]

        return encoded_text

    def get_padded_text(self, enc_text):
        pad_amount = 8 - (len(enc_text) % 8)
        enc_text += "0" * pad_amount

        pad_info = "{0:08b}".format(pad_amount)
        padded_enc_text = pad_info + enc_text

        return padded_enc_text

    def get_byte_array(self, pad_enc_text):
        byte_array = []

        for i in range(0, len(pad_enc_text), 8):
            curr_bit = pad_enc_text[i:i + 8]
            byte_array.append(int(curr_bit, 2))
        return byte_array

    def compress(self):
        file_add, file_ext = os.path.splitext(self.path)
        output_path = file_add + ".bin"
        with open(self.path, mode="r", encoding="utf-8") as file, open(output_path, mode="wb") as output:
            text = file.read()
            text = text.rstrip()
            frequency = self.get_freq_dict(text)

            self.build_heap(frequency)

            self.build_tree()

            self.build_codes()

            encoded_text = self.get_encoded_text(text)

            padded_encoded_text = self.get_padded_text(encoded_text)

            byte_array = self.get_byte_array(padded_encoded_text)

            final_bytes = bytes(byte_array)
            output.write(final_bytes)

        print("compressed")
        return output_path

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]

        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]

        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        decoded_text = ""
        current_code = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                character = self.reverse_codes[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    def decompress(self, input_path):
        file_name, file_ext = os.path.splitext(input_path)
        output_path = file_name + "_decompressed.bin"
        with open(input_path, "rb") as file, open(output_path, "w") as output:
            bit_string = ""
            byte = file.read(1)

            while len(byte) > 0:
                byte = ord(byte)

                bits = bin(byte)[2:].rjust(8, "0")
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decoded_text = self.decode_text(encoded_text)

            output.write(decoded_text)
        print("decompressed")
        return






path = os.getcwd()
path = path+r"\new.txt"
h = HuffmanCoding(path)

out = h.compress()

h.decompress(out)