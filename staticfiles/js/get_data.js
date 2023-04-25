let fetchRes = fetch(
    "http://127.0.0.1:8000/api/tickets/10000");
fetchRes.then(res =>
    res.json()).then(d => {
        console.log(d)
    })