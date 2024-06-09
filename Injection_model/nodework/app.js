var express = require('express');
var http = require('http');
var app = express();
const cors = require('cors');
// const { createProxyMiddleware } = require('http-proxy-middleware');
var server = http.createServer(app);

app.use(cors({
    origin: '*', // 모든 출처 허용 옵션. true 를 써도 된다.
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // 허용할 HTTP 메서드 추가
    allowedHeaders: '*', // 모든 헤더를 허용
}));

// 정적 파일 경로 설정
app.use('/images', express.static('images'));
app.use('/datas', express.static('datas'));


// 서버가 정상적으로 요청을 수신하고 있는지를 확인
app.use(function(req, res, next) {
    console.log('Received a request to ' + req.originalUrl);
    next();
});

// predict - 예측
app.get('/', function (req, res) {
	// console.log('Received a request to /predict'); // 여기에 새로운 콘솔로그 추가
	res.sendFile(__dirname +"/predict.html")
});

server.listen(80, function() {
    console.log('Server started ...');
});
