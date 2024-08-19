from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def gen_frames():  
    while True:
        success, frame = capture.read()  # 현재 영상을 받아옴
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)   # 현재 영상을 그림파일의형태로 바꿈
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 그림파일들을 쌓아두고 호출을 기다림


@app.route('/')
def index():
    return render_template('index4#2.html')             # index4#2.html의 형식대로 웹페이지를 보여줌

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') # 그림파일들을 쌓아서 보여줌

if __name__ == "__main__":  # 웹사이트를 호스팅항 접속자에게 보여주기 위한 부분
   app.run(host="192.168.5.3", port = "18010")
   # host는 현재 라즈베리파이의 내부 IP, port는 임의로 설정
   # 해당 내부 IP와 port를 포트포워딩 해두면 외부에서도 접속가능