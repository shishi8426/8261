from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>挖矿模拟器</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
        #counter { font-size: 48px; margin-top: 20px; }
        button { font-size: 24px; padding: 10px 30px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🪙 点击开始挖矿</h1>
    <button onclick="startMining()">开始挖矿</button>
    <div id="counter">0</div>

    <script>
        let count = 0;
        let intervalId = null;

        function startMining() {
            if (intervalId !== null) return; // 防止重复点击
            intervalId = setInterval(() => {
                count += 1;
                document.getElementById("counter").innerText = count;
            }, 1000);
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
