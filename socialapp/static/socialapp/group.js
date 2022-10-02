
const sock = new WebSocket(`wss://${window.location.host}/ws/chat/group/${roomid}/`);


sock.onmessage = (e) => {
    const data = JSON.parse(e.data);
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