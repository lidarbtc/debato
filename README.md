<div align=center>
 
# Debato : 오픈소스 한국형 커뮤니티 CMS
 <p>
 <img src="https://img.shields.io/github/stars/lidarbtc/dongbaek-life?color=%23DF0067&style=for-the-badge"/> &nbsp;
 <img src="https://img.shields.io/github/forks/lidarbtc/dongbaek-life?color=%239999FF&style=for-the-badge"/> &nbsp;
 <img src="https://img.shields.io/github/license/lidarbtc/dongbaek-life?color=%23E8E8E8&style=for-the-badge"/> &nbsp;

Under a maintenance : 미완성 상태입니다.

## Language</br>

<img src="https://img.shields.io/badge/Rust-black?style=for-the-badge&logo=rust&logoColor=#E57324"/></br>

</div>

## Usage on Debian

```sh
 sudo apt install cargo

 git clone https://github.com/lidarbtc/debato.git
 cd debato

 cargo build --release

 # 여기부터 mysql

    ```
    CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'abcd1234';

    CREATE DATABASE debato;

    grant all privileges on debato.* to 'dbuser'@'localhost';

    flush privileges;

    여기서 script.sql cmd에 그대로 복사 붙여넣기

    exit;
    ```

 # 여기가 mysql 끝

 # 실행 명령어
 ./target/release/debato
 
 # 접속하는 방법
 그 후 http://127.0.0.1:8000 접속
 또한 http://127.0.0.1:8000/board/free 접속

```

## Contact Developer : 개발자 연락처

```
 session : 05c67e3461a3b17896f063535c2ade0b91639be688a6de6d5665258995f0fec660
```
