*Kidspay Service Application* 


**Чтобы начать разработку**  
Установите python3.6 и virtualenv. После в зайдите директории проекта создайте окружение 

``virtualenv -p python3.6 venv``

Активируйте окружение:
``source venv/bin/activate``

Установите зависимости:

``pip install -r requirements.txt``

Запустите миграции:
``python manage.py migrate``


Готово можете начинать разработку.

**Чтобы отправить изменения на сервер**  

Создайте файл с названием `prod` в дериктории KidsPayAPI/config/deploy/hosts/

Сконфигрируйте его по примеру prod.sample

Отправьте измения в ветку `master`

Обновить исходный код на продакшн сервере запустите:
``python manage.py deploy --prod``

