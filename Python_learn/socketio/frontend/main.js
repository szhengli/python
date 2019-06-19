
var socket = io('http://192.168.10.40:5000');


socket.on('connect', ()=> {

    socket.on('sub',(msg)=> {
        $('#status').append(msg+'<br>');
    });

});



