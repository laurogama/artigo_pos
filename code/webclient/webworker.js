var username = 'sensor_node';
var password = '123456';
var host = 'http://10.8.0.135:15674/stomp';

var client = null;
var app = angular.module('wsnApp', []);
app.controller('FPController', ['$scope', function ($scope) {
    $scope.messages = [];
    function connect() {
        var ws = new SockJS(host);
        var client = Stomp.over(ws);
        client.heartbeat.outgoing = 0;
        client.heartbeat.incoming = 0;
        return client;
    }

    client = connect();
    var subscription = null;

    var on_connect = function () {
        console.log('open');
        subscription = client.subscribe("/exchange/logs", on_message);
    };
    var on_error = function (e) {
        client.close();
        client = connect();
        client.connect(username, password, on_connect, on_error, '/');
    };
    var on_message = function (e) {
        whatToDoWhenMessageComming(e)
    };

    function whatToDoWhenMessageComming(message) {
        $scope.$apply(function () {
            $scope.messages.push(JSON.parse(message.body));
        });
    }

    client.connect(username, password, on_connect, on_error, '/');
}]);

