const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});


function nextPostPage(){
    window.location.href = `/posts?o=${Number(params.o)+10}`;
}
function prevPostPage(){
    window.location.href = `/posts?o=${Number(params.o)-10}`;
}

function nextReportPage(){
    window.location.href = `/reports?o=${Number(params.o)+10}`;
}
function prevReportPage(){
    window.location.href = `/reports?o=${Number(params.o)-10}`;
}

function search(){
    var user = document.getElementById("input_search_user").value;
    var q = document.getElementById("input_search_text").value;
    var urlparams = new URLSearchParams("");
    
    if (user != ''){
        urlparams.append("user", user);
    }
    if (q != ''){
        urlparams.append("q", q);
    }
    window.location.href = `/search?${urlparams.toString()}`
}

function nextSearchPage(){
    var q = params.q;
    var user = params.user;
    var o = Number(params.o);
    if (q == null){
        q = '';
    }
    if (user == null){
        user = '';
    }

    var urlparams = new URLSearchParams("")
    if (user != ''){
        urlparams.append("user", user);
    }
    if (q != ''){
        urlparams.append("q", q);
    }
    urlparams.append("o", o+10);
    
    window.location.href = `/search?${urlparams.toString()}`;
}
function prevSearchPage(){
    var q = params.q;
    var user = params.user;
    var o = Number(params.o);
    if (q == null){
        q = '';
    }
    if (user == null){
        user = '';
    }

    var urlparams = new URLSearchParams("")
    if (user != ''){
        urlparams.append("user", user);
    }
    if (q != ''){
        urlparams.append("q", q);
    }
    urlparams.append("o", o-10);
    
    window.location.href = `/search?${urlparams.toString()}`;
}

function nextLikedPost(){
    var lo = Number(params.lo);
    var co = Number(params.co);
    var username = window.location.pathname.split("/")[2];

    var urlparams = new URLSearchParams("");

    urlparams.append("lo", lo+10);
    urlparams.append("co", co);
    
    console.log(username);
    window.location.href = `/profile/${username}?${urlparams.toString()}`;
}
function prevLikedPost(){
    var lo = Number(params.lo);
    var co = Number(params.co);
    var username = window.location.pathname.split("/")[2];

    var urlparams = new URLSearchParams("");

    urlparams.append("lo", lo-10);
    urlparams.append("co", co);
    
    window.location.href = `/profile/${username}?${urlparams.toString()}`;
}
function nextCreatedPost(){
    var lo = Number(params.lo);
    var co = Number(params.co);
    var username = window.location.pathname.split("/")[2];

    var urlparams = new URLSearchParams("");

    urlparams.append("lo", lo);
    urlparams.append("co", co+10);
    
    console.log(username);
    window.location.href = `/profile/${username}?${urlparams.toString()}`;
}
function prevCreatedPost(){
    var lo = Number(params.lo);
    var co = Number(params.co);
    var username = window.location.pathname.split("/")[2];

    var urlparams = new URLSearchParams("");

    urlparams.append("lo", lo);
    urlparams.append("co", co-10);
    
    console.log(username);
    window.location.href = `/profile/${username}?${urlparams.toString()}`;
}


// in miliseconds
var units = {
    year  : 24 * 60 * 60 * 1000 * 365,
    month : 24 * 60 * 60 * 1000 * 365/12,
    day   : 24 * 60 * 60 * 1000,
    hour  : 60 * 60 * 1000,
    minute: 60 * 1000,
    second: 1000
};
  
var rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

var getRelativeTime = (d1) => {
    const d2 = new Date().getTime() / 1000000
    var elapsed = d2 - d1;
    // "Math.abs" accounts for both "past" & "future" scenarios
    for (var u in units){
        if (Math.abs(elapsed) > units[u] || u == 'second'){
            return rtf.format(Math.round(elapsed/units[u]), u);
        }
    }
}
function sanitizeInput(s){
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      };
      return s.replace(/[&<>"']/g, function(m) { return map[m]; });
}
function appendNewMessage(username, message, d){
    // This needs major re-writing
    var e = document.getElementById("message-area");
    var c = `
    <div class="box">
        <article class="media">
            <div class="media-content">
                <div class="content">
                    <div>
                        <span style="display:inline;"> 
                            <strong>${sanitizeInput(username)}</strong>:
                        </span>
                        <div class="_message-text mb" style="display:inline;">
                            ${sanitizeInput(message)}
                        </div>
                    </div>
                    <small>${d}</small>
                </div>
            </div>
        </article>
    </div>
    `
    e.innerHTML += c;
}

function showSockClosed(e){
    document.getElementById("room-new-message-input").disabled = true;
    document.getElementById("room-new-message-submit").disabled = true;
    document.getElementById("sock_closed").classList.add("is-active");
}