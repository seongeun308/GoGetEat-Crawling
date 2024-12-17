from flask import Flask, request, jsonify
import service
import config
app = Flask(__name__)

# POST 요청을 처리하는 엔드포인트
@app.route('/api/menu', methods=['POST'])
def get_menu_data():
    urls = request.get_json()
    if urls:
        menu_data = []
        driver = config.create_chrome_driver()
        for url in urls:
            menu_dto = service.get_kakaoMap_menu(driver, url) 
            menu_data.append(menu_dto.__dict__)
        driver.quit()

        response = {
            'message': 'Data received successfully!',
            'received_data': menu_data
        }
        return jsonify(response), 200
    else:
        response = {'message': 'No data received.'}
        return jsonify(response), 400

if __name__ == '__main__':
    app.run(debug=True)

