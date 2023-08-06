# Project closed for now

# Protect sha256

- crypt_file(filename, output, key)          :    encrypt the given file
- generate_file(filename, key)               :    create a cypted version of the file (.crtph)
- decrypt_file(filename, key)                :    decrypt the file (.dcrtph)
- convert_file(filename, key)                :    encrypt the given file
- crypt_str(char, key)                       :    encrypt the str, return a str
- read_crypt_file(filename, key)             :    read the given file, return a str
- execute_crypt_file(filename, key)          :    python only, might bug


# Protect base64 + sha256

- crypt_file_v2(filename, output, key)     :    encrypt the given file
- generate_file_v2(filename, key)          :    create a cypted version of the file
- decrypt_file_v2(filename, key)           :    decrypt the file (.dcrtph)
- convert_file_v2(filename, key)           :    encrypt the given file
- crypt_str_v2(char, key)                  :    encrypt the str, return a str
- read_crypt_file_v2(filename, key)        :    read the given file, return a str
- execute_crypt_file_v2(filename, key)     :    python only, might bug
