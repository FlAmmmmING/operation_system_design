from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField, validators
from wtforms.validators import NumberRange
import make_figure_duration
import make_figure_start_end_time
import make_main_table
from multi_Spider import multi_thread_start
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '823725'


class URLForm(FlaskForm):
    text_number = IntegerField('文本分割数量', validators=[NumberRange(min=1, max=100)])
    url_queue_number = IntegerField('爬虫通道数量', validators=[NumberRange(min=3, max=10)])
    data_queue_number = IntegerField('解析通道数量', validators=[NumberRange(min=3, max=10)])
    min_value = IntegerField('最小值', validators=[validators.NumberRange(min=1, max=500)])
    max_value = IntegerField('最大值', validators=[validators.NumberRange(min=1, max=500)])
    submit = SubmitField('上传')


@app.route('/', methods=['GET', 'POST'])
def front_end():
    text = []
    total_time = 0
    form = URLForm()
    # 读取CSV文件内容
    csv_data = []
    with open('webpage_text_size.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_data.append(row)
    if form.validate_on_submit():
        # 选择爬取的内容
        minimum = form.min_value.data
        maximum = form.max_value.data

        dividing_number = form.text_number.data
        n1 = form.url_queue_number.data
        n2 = form.data_queue_number.data
        # print(url_set)
        # text 是爬取的文本
        text, total_time = multi_thread_start('divided_data', n1, n2, dividing_number, minimum, maximum)
        # text = ['111']
        # print(text)
        make_figure_duration.figure()
        make_figure_start_end_time.figure()
        make_main_table.figure()
        # 这里可以将处理结果返回给前端
    return render_template('front_end.html', form=form, total_consumption=total_time, csv_data=csv_data)


if __name__ == '__main__':
    app.run()
