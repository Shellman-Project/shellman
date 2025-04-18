#!/usr/bin/env bats

setup() {
  mkdir -p tmp secure plain
  echo "Secret message" > tmp/secret.txt
}

teardown() {
  rm -rf tmp secure plain
}

@test "encrypts a file using AES" {
  run ./bin/shellman encrypt_files --mode encrypt --password test123 --ext txt --path tmp --out secure
  [ "$status" -eq 0 ]
  [ -f "secure/secret.txt.enc" ]
}

@test "decrypts a file back to original content" {
  ./bin/shellman encrypt_files --mode encrypt --password test123 --ext txt --path tmp --out secure
  run ./bin/shellman encrypt_files --mode decrypt --password test123 --ext enc --path secure --out plain
  [ "$status" -eq 0 ]
  [ -f "plain/secret.txt" ]
  grep -q "Secret message" plain/secret.txt
}
