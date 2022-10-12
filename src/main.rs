#[macro_use]
extern crate rocket;
extern crate bcrypt;

use rocket::fs::{relative, FileServer};

use std::net::SocketAddr;

// 직렬화 함수
use rocket::serde::{Deserialize, Serialize};

// 폼 함수
use rocket::form::{Form, FromForm};

// 쿠키 함수
use rocket::http::{Cookie, CookieJar};

// 플래시, 리다이렉트 함수
use rocket::response::{Flash, Redirect};

// DB 함수
use rocket_db_pools::sqlx::Row;

// DB 연결 함수
use rocket_db_pools::{
    sqlx::{self, mysql::MySqlRow},
    Connection, Database,
};

// SSR 렌더링 함수
use rocket_dyn_templates::{context, Template};

// 해시 함수
use bcrypt::{hash, verify, DEFAULT_COST};

// DB 정보 정의
#[derive(Database)]
#[database("debato")]
struct Debato(sqlx::MySqlPool);

// 메인 화면
#[get("/")]
fn index(jar: &CookieJar<'_>) -> Template {
    let userid = jar
        .get_private("userid")
        .map(|crumb| format!("{}", crumb.value()));

    if userid == None {
        Template::render(
            "index",
            context! {
                isusername : false,
                footer: 123,
            },
        )
    } else {
        Template::render(
            "index",
            context! {
                isusername : true,
                username: userid,
                footer: 123,
            },
        )
    }
}

// 게시판 화면
#[derive(Serialize, Deserialize)]
#[serde(crate = "rocket::serde")]
struct Rowpost {
    id: i32,
    title: String,
    time: String,
    like: i32,
    author: String,
}

#[get("/board/<boardname>")]
async fn board(mut db: Connection<Debato>, jar: &CookieJar<'_>, boardname: &str) -> Template {
    let content: String = format!(
        r#"SELECT id, title, DATE_FORMAT(posttime, '%Y-%m-%d.'), likecount, username FROM posttbl WHERE boardname="{}""#,
        boardname
    );
    let query = sqlx::query(&content);

    let posts: Vec<Rowpost> = query
        .map(|r: MySqlRow| Rowpost {
            id: r.get("id"),
            title: r.get("title"),
            time: r.get("DATE_FORMAT(posttime, '%Y-%m-%d.')"),
            like: r.get("likecount"),
            author: r.get("username"),
        })
        .fetch_all(&mut *db)
        .await
        .unwrap();

    let username = jar
        .get_private("userid")
        .map(|crumb| format!("{}", crumb.value()));

    if username == None {
        Template::render(
            "board",
            context! {
                post : posts,
                isusername : false,
                footer: 123,
            },
        )
    } else {
        Template::render(
            "board",
            context! {
                post : posts,
                isusername : true,
                username: username,
                footer: 123,
            },
        )
    }
}

// 관리자 페이지
#[get("/debato")]
fn admin() -> Template {
    Template::render(
        "debato",
        context! {
            foo: 123,
        },
    )
}

// 회원가입 페이지
#[get("/register")]
fn register() -> Template {
    Template::render(
        "login",
        context! {
            sitename: 123,
            footer: 123,
        },
    )
}

#[derive(FromForm)]
struct Userregister {
    name: String,
    password: String,
    email: String,
    id: String,
}

#[post("/register", data = "<user>")]
async fn registerpost(
    mut db: Connection<Debato>,
    jar: &CookieJar<'_>,
    user: Form<Userregister>,
    addr: SocketAddr,
) -> Flash<Redirect> {
    let ipv4 = addr.ip();
    let useragent = "true";
    let hashed = hash(user.password.clone(), DEFAULT_COST).unwrap();

    let content: String = format!("INSERT INTO usertable(userid, userpw, useremail, username, ua, ip) VALUE({}, {}, {}, {}, {}, {})", user.id, hashed, user.email, user.name, useragent, ipv4);

    match sqlx::query(&content).execute(&mut *db).await {
        Err(_e) => Flash::success(Redirect::to(uri!(register)), "중복된 아이디입니다."),
        Ok(_e) => {
            jar.add_private(Cookie::new("userid", user.id.clone()));
            Flash::success(Redirect::to(uri!(index)), "가입 되었습니다.")
        }
    }
}

// 글 작성 페이지
#[get("/board/<boardname>/write")]
fn write(jar: &CookieJar<'_>, boardname: &str) -> Template {
    let userid = jar
        .get_private("userid")
        .map(|crumb| format!("{}", crumb.value()));

    if userid == None {
        Template::render(
            "write",
            context! {
                boardname: boardname,
                isusername : false,
                footer: 123,
            },
        )
    } else {
        Template::render(
            "write",
            context! {
                boardname: boardname,
                isusername : true,
                username: userid,
                footer: 123,
            },
        )
    }
}

#[derive(FromForm)]
struct Content {
    title: String,
    content: String,
}

#[post("/board/<boardname>/write", data = "<content>")]
async fn writepost(
    mut db: Connection<Debato>,
    jar: &CookieJar<'_>,
    addr: SocketAddr,
    content: Form<Content>,
    boardname: &str,
) -> Flash<Redirect> {
    let ipv4 = addr.ip();
    let useragent = "true";
    let userid = jar
        .get_private("userid")
        .map(|crumb| format!("{}", crumb.value()));
    let title = &content.title;
    let content = &content.content;

    match userid {
        Some(userid) => {
            let dbcontent = format!("SELECT username FROM usertbl WHERE userid={}", userid);

            let query = sqlx::query(&dbcontent);
            let userdata = query.fetch_one(&mut *db).await.unwrap();

            let username: String = userdata.get("username");

            let dbcontent: String = format!("INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE({}, {}, {}, {}, {}, {}, {}, {})", boardname, username, 0, title, content, 0, ipv4, useragent);

            match sqlx::query(&dbcontent).execute(&mut *db).await {
                Err(_e) => Flash::success(
                    Redirect::to(uri!(board(boardname))),
                    "작성되지 않았습니다. DB 연결중 오류.",
                ),
                Ok(_e) => Flash::success(Redirect::to(uri!(index)), "작성되었습니다."),
            }
        }
        None => Flash::success(
            Redirect::to(uri!(board(boardname))),
            "작성되지 않았습니다. 쿠키 오류.",
        ),
    }
}

// 로그인 페이지
#[get("/login")]
fn login() -> Template {
    Template::render(
        "sign",
        context! {
            sitename: 123,
        },
    )
}

#[derive(FromForm)]
struct Userlogin {
    name: String,
    password: String,
}

#[post("/login", data = "<user>")]
async fn loginpost(
    mut db: Connection<Debato>,
    jar: &CookieJar<'_>,
    user: Form<Userlogin>,
) -> Flash<Redirect> {
    let username = user.name.clone();
    let userpw = user.password.clone();

    let content = format!("SELECT password FROM usertbl WHERE userid={}", username);

    let query = sqlx::query(&content);
    let userdata = query.fetch_one(&mut *db).await.unwrap();

    let hashed: String = userdata.get("password");

    let valid = verify(userpw, &hashed).unwrap();

    if valid {
        jar.add_private(Cookie::new("userid", username));
        Flash::success(Redirect::to(uri!(index)), "성공적으로 로그인 되었습니다.")
    } else {
        Flash::success(Redirect::to(uri!(login)), "비밀번호가 맞지 않습니다.")
    }
}

// 로그아웃 페이지
#[get("/logout")]
fn logout(jar: &CookieJar<'_>) -> Flash<Redirect> {
    jar.remove_private(Cookie::named("userid"));
    Flash::success(Redirect::to(uri!(index)), "로그아웃 되었습니다.")
}

// 로켓 실행 함수
#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount(
            "/",
            routes![
                index,
                admin,
                board,
                register,
                registerpost,
                login,
                loginpost,
                logout,
                write,
                writepost
            ],
        )
        .mount("/", FileServer::from(relative!("static")))
        .attach(Template::fairing())
        .attach(Debato::init())
}
