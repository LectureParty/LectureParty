var joinParty = false;
var createParty = false;
var myParties = false;

function switchJoinParty() {
    event.stopPropagation();
    createParty = false;
    document.getElementById('createparty').classList.remove('show');
    if (joinParty === false){
        joinParty = true;
        document.getElementById('joinparty').classList.toggle('show');
    } else {
        joinParty = false;
        document.getElementById('joinparty').classList.remove('show');
    }
}

function switchCreateParty() {
    event.stopPropagation();
    joinParty = false;
    document.getElementById('joinparty').classList.remove('show');
    if (createParty === false){
        createParty = true;
        document.getElementById('createparty').classList.toggle('show');
    } else {
        createParty = false;
        document.getElementById('createparty').classList.remove('show')
    }
}

/*
window.onclick = function(event) {
    joinParty = false;
    createParty = false;
    document.getElementById('joinparty').classList.remove('show');
    document.getElementById('createparty').classList.remove('show');
}
*/