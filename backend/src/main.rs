use rand::Rng;
use rocket::fs::FileServer;
use rocket::serde::json::{json, Json, Value};
use rocket::serde::{Deserialize, Serialize};
use rocket_dyn_templates::{context, Template};
use std::sync::atomic::{AtomicU8, Ordering};

#[derive(Deserialize)]
struct Input {
    id: u8,
}

#[derive(Serialize)]
struct Output {
    result: bool,
}

#[rocket::post("/", format = "json", data = "<input>")]
fn index(input: Json<Input>) -> Json<Output> {
    let id = input.0.id;
    let result = id == 3;
    Json(Output { result })
}

#[rocket::get("/")]
fn indexload() -> Template {
    Template::render(
        "index",
        context! {
            this: 0,
        },
    )
}

#[rocket::launch]
fn rocket() -> _ {
    let id = AtomicU8::new(rand::random::<u8>() % 2);
    rocket::build()
        .mount("/", FileServer::from("static"))
        .mount("/", rocket::routes![indexload])
        .mount("/api", rocket::routes![index])
        .attach(Template::fairing())
}
