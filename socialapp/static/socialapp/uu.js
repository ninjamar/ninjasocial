
const sock = new WebSocket(`ws://${window.location.host}/ws/chat/uu/${u1}/${u2}/`);


sock.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if ("close" in data){
        sock.close();
        // show socket closed popup
    }
    const d = Math.floor((new Date(data["timestamp"])).getTime() /1000)
    appendNewMessage(data["username"], data["message"], getRelativeTime(d));
}
sock.onerror = (e) => {
    console.log("Socket closed unexpectedly", e);
}
sock.onclose = (e) => {
    console.log(`Socket got closed by the server: code ${e.code}`, e);
    showSockClosed(e);
}

function handleNewMessageSubmit(){
    const message = document.getElementById("room-new-message-input").value;
    sock.send(JSON.stringify({
        "message": message
    }));
    document.getElementById("room-new-message-input").value = "";
}