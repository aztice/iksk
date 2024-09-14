class iksk:
    def encrypt(self, value, salt='iksk', mode=[1, 1, 1, 1, 1]):
        sn = self._similarity(value,salt+value+salt)
        value = self._invert(value, mode[0])
        value = self._offset_encrypt(value, mode[3])
        value = self._block_encrypt(value, salt)
        value = self._invert(value, mode[1])
        value = self._custom_invert(value, mode[2] * 2)
        value = self._block_encrypt(value, salt)
        if mode[4]==1:
            value = self._block_encrypt(value, str(sn))
            value = [value, sn]
        return value
    def decrypt(self, value, salt='iksk', mode=[1, 1, 1, 1, 1], sn=None):
        if mode[4]==1:
            value = self._block_decrypt(value, str(sn))
        value = self._block_decrypt(value, salt)
        value = self._custom_deinvert(value, mode[2] * 2)
        value = self._invert(value, mode[1])
        value = self._block_decrypt(value, salt)
        value = self._offset_decrypt(value, mode[3])
        value = self._invert(value, mode[0])
        return value
    def _levenshtein_distance(self, s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,dp[i][j - 1] + 1,dp[i - 1][j - 1] + cost)
        return dp[m][n]
    def _similarity(self,s1, s2):
        distance = self._levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1 - distance / max_len
    def _offset_encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shift_amount = shift
                if char.islower():
                    start = ord('a')
                    shifted = (ord(char) - start + shift_amount) % 26 + start
                elif char.isupper():
                    start = ord('A')
                    shifted = (ord(char) - start + shift_amount) % 26 + start
                encrypted_text += chr(shifted)
            else:
                 encrypted_text += char
        return encrypted_text
    def _offset_decrypt(self,encrypted_text, shift):
        decrypted_text = ""
        for char in encrypted_text:
            if char.isalpha():
                shift_amount = -shift
                if char.islower():
                    start = ord('a')
                    shifted = (ord(char) - start + shift_amount) % 26 + start
                elif char.isupper():
                    start = ord('A')
                    shifted = (ord(char) - start + shift_amount) % 26 + start
                decrypted_text += chr(shifted)
            else:
                decrypted_text += char
        return decrypted_text
    def _invert(self, value, mode):
        chars = list(value)  # 将字符串转换为字符列表
        if mode == 0:
            indices_to_invert = [i for i in range(1, len(chars), 2)]
        elif mode == 1:
            indices_to_invert = [i for i in range(0, len(chars), 2)]
        else:
            print('[iksk] mode-0:: invalid')
            exit()

        inverted_chars = [chars[i] for i in indices_to_invert][::-1]
        for idx, orig_idx in enumerate(indices_to_invert):
            chars[orig_idx] = inverted_chars[idx]

        return ''.join(chars)

    def _custom_invert(self, value, step):
        chars = list(value)
        indices_to_invert = [i for i in range(0, len(chars), step)]
        
        inverted_chars = [chars[i] for i in indices_to_invert][::-1]
        for idx, orig_idx in enumerate(indices_to_invert):
            if orig_idx < len(chars):
                chars[orig_idx] = inverted_chars[idx]

        return ''.join(chars)
    def _custom_deinvert(self, value, step):
        chars = list(value)
        indices_to_invert = [i for i in range(0, len(chars), step)]  
        inverted_chars = [chars[i] for i in indices_to_invert][::-1]
        for idx, orig_idx in enumerate(indices_to_invert):
            if orig_idx < len(chars):
                chars[orig_idx] = inverted_chars[idx]
        return ''.join(chars)

    def _block_encrypt(self, message, key):
        encrypted_blocks = [] 
        blocks = [message[i:i+8] for i in range(0, len(message), 8)]
        for block in blocks:
            encrypted_block = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(block))
            encrypted_blocks.append(encrypted_block)
            key = self._update_key(key, block)
        return ''.join(encrypted_blocks)

    def _block_decrypt(self, encrypted_message, key):
        decrypted_blocks = []    
        blocks = [encrypted_message[i:i+8] for i in range(0, len(encrypted_message), 8)]
        for block in blocks:
            decrypted_block = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(block))
            decrypted_blocks.append(decrypted_block)
            key = self._update_key(key, decrypted_block)
        return ''.join(decrypted_blocks)

    def _update_key(self, key, block):
        updated_key = ''.join(chr(ord(key[i]) ^ ord(block[i % len(block)])) for i in range(len(key)))
        return updated_key
