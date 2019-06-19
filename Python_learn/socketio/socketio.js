/**
 * Created by Administrator on 2019/6/19 0019.
 */
// npm install socketio

var io = require('socket.io')(5000);

io.on('connection', function (socket) {
    io.emit('this', { will: 'be received by everyone'});
    console.log('connected');

    socket.on('pub', function (msg) {
        console.log('I received a private message by '+  msg);
        io.emit('sub',msg);
    });

    socket.on('disconnect', function () {
        io.emit('user disconnected');
    });
});
