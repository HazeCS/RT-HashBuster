
# Rainbow Table Hash Buster

Hash Buster is a Python tool for generating Rainbow Tables and cracking hashes using Rainbow Tables. It supports the following hash algorithms: md5, sha1, sha224, sha256, sha384, sha512.

Find my Rainbow Tables list here - https://mega.nz/folder/ys8VyY5T#kZsRbSZCL9WS4T3GEoPo6g

![image](https://user-images.githubusercontent.com/93849885/218319656-99b5b446-2f4d-4d38-bd7b-d3f764fd1626.png)

## Usage
Hash Buster can be used in two modes: build and brute.

## Build mode

In build mode, Hash Buster generates a Rainbow Table from a given wordlist and a hash algorithm, and saves it to an output file. To use build mode, run the following command:

```
python3 hash_buster.py build -o [output_file] -w [wordlist_file] -H [hash_algorithm] [-v]

    [output_file]: The name of the output file for the generated Rainbow Table.
    [wordlist_file]: The name of the wordlist file to generate the Rainbow Table from.
    [hash_algorithm]: The hash algorithm to use for generating the Rainbow Table.
    -v: (Optional) Enable verbose output.
```

## Brute mode

In brute mode, Hash Buster searches a Rainbow Table for a given hash and outputs the corresponding plaintext. To use brute mode, run the following command:

```
python3 hash_buster.py brute -rt [rainbow_table_file] -H [hash] [-v]

    [rainbow_table_file]: The name of the Rainbow Table file to search.
    [hash]: The hash to search for.
    -v: (Optional) Enable verbose output.
```

## Example

Here is an example usage of Hash Buster in build mode:

`python hash_buster.py build -o my_table.rt -w my_wordlist.txt -H sha256`

This command generates a Rainbow Table from the file my_wordlist.txt using the sha256 hash algorithm, and saves it to the file my_table.rt.

And here is an example usage of Hash Buster in brute mode:

`python hash_buster.py brute -rt my_table.rt -H 5f4dcc3b5aa765d61d8327deb882cf99`

This command searches the Rainbow Table in the file my_table.rt for the hash 5f4dcc3b5aa765d61d8327deb882cf99 and outputs the corresponding plaintext, if found.
Dependencies

Hash Buster requires the following Python modules to be installed:

    argparse
    colorama
    hashlib

## License

Hash Buster is licensed under the MIT License. See the LICENSE file for details.
