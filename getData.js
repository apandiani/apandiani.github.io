getOWM();
getST2("https://apandiani.eu.pythonanywhere.com/st2");
getStromer("https://apandiani.eu.pythonanywhere.com/stromer");
getLKR("https://apandiani.eu.pythonanywhere.com/lkr");

async function getST2(url) {
    const get = await fetch(url);
    const txt = await get.text();
    const obj = JSON.parse(txt)
    const health = obj['Battery health']
    const date = obj['Date']
    const distance = obj['Total distance']
    output_tot = document.querySelector("#st2_tot")
    output_tot.innerText = Math.round(distance) + ' km'
    output_bat = document.querySelector("#st2_bat")
    output_bat.innerText = health + ' %'
    output_date = document.querySelector("#st2_date")
    output_date.innerText = 'Last update: ' + date
};

async function getStromer(url) {
    const get = await fetch(url);
    const txt = await get.text();
    const obj = JSON.parse(txt)
    let item = "";
    for (let x in obj) {
        item = obj[x];
        div = document.querySelector("#stromer_feed");
        child = document.createElement('p');
        child.innerText = item;
        div.appendChild(child);
    }
};

function owm_time(ts) {
    let time = new Date(ts * 1000);
    let options = {  
        hour: "2-digit", minute: "2-digit"  
    };
    time = time.toLocaleTimeString('de-CH', options);
    return time;
}

async function getOWM() {
    const lat = 47.25682498845265;
    const lon = 8.85427686073874;
    const api_key = '1de97342bb9f3b6c38127ff0d7b979bd';
    const url = `https://api.openweathermap.org/data/3.0/onecall?lat=${lat}&lon=${lon}&appid=${api_key}&units=metric`;
    const get = await fetch(url);
    const txt = await get.text();
    const obj = JSON.parse(txt);
    const current_temp = obj['current']['temp']
    output_temp = document.querySelector("#owm_tem")
    output_temp.innerText = current_temp.toFixed(1) + ' °C'
    let current_sunrise = obj['current']['sunrise']
    current_sunrise = owm_time(current_sunrise)
    output_rise = document.querySelector("#owm_ris")
    output_rise.innerText = current_sunrise
    let current_sunset = obj['current']['sunset']
    current_sunset = owm_time(current_sunset)
    output_set = document.querySelector("#owm_set")
    output_set.innerText = current_sunset
    const current_weather = obj['current']['weather'][0]['description']
    output_des = document.querySelector("#owm_des")
    output_des.innerText = current_weather
    const timestamp = obj['current']['dt']
    const time = owm_time(timestamp)
    output_date = document.querySelector("#owm_date")
    output_date.innerText = `Last update: ${time}`
    // output_date.innerText = formatDate(time, "HH:mm");
};

async function getLKR(url) {
    const get = await fetch(url);
    const txt = await get.text();
    const obj = JSON.parse(txt);
    const last = obj[obj.length-1];
    window.lkr = last['LKR'];
    const date = last['Date'];
    output_lkr = document.querySelector("#lkr");
    output_lkr.innerText = Math.round(lkr) + ' LKR';
    output_date = document.querySelector("#lkr_date");
    output_date.innerText = 'Last update: ' + date;
};

function temperatureConverter(source,valNum) {
    valNum = parseFloat(valNum);
    var input_chf = document.getElementById("input_chf");
    var input_lkr = document.getElementById("input_lkr");
    if (source=="input_chf") {
        input_lkr.value=(valNum * lkr).toFixed(0);
    }
    if (source=="input_lkr") {
        input_chf.value=(valNum / lkr).toFixed(2);
    }
}

function resetLKR() {
    chf_in = document.querySelector("#input_chf")
    chf_in.value = null
    lkr_in = document.querySelector("#input_lkr")
    lkr_in.value = null
}