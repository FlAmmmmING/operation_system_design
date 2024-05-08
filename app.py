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
    min_value = IntegerField('最小值', validators=[validators.NumberRange(min=1, max=500)])
    max_value = IntegerField('最大值', validators=[validators.NumberRange(min=1, max=500)])
    url_queue_number = IntegerField('爬虫通道数量', validators=[NumberRange(min=3, max=10)])
    data_queue_number = IntegerField('解析通道数量', validators=[NumberRange(min=3, max=10)])
    submit1 = SubmitField('上传')
    submit2 = SubmitField('查询')


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

    if form.submit1.data and form.validate_on_submit():
        # 选择爬取的内容
        minimum = form.min_value.data
        maximum = form.max_value.data

        dividing_number = form.text_number.data
        n1 = form.url_queue_number.data
        n2 = form.data_queue_number.data
        # debug 的时候用这个
        # text = []
        # total_time = 0
        csv_data = []
        with open('webpage_text_size.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if minimum <= i + 1 <= maximum:  # 注意索引从1开始，所以要加1
                    csv_data.append(row)
                elif i + 1 > maximum:  # 超出最大值范围则退出循环
                    break
        text, total_time = multi_thread_start('divided_data', n1, n2, dividing_number, minimum, maximum)
        make_figure_duration.figure()
        make_figure_start_end_time.figure()
        make_main_table.figure()
        return render_template('front_end.html', form=form, text=text, total_consumption=total_time, csv_data=csv_data)

    if form.submit2.data and form.validate_on_submit():
        # minimum = 0
        # maximum = 0
        minimum = form.min_value.data
        maximum = form.max_value.data
        # print(1)
        # print(minimum)
        # print(maximum)
        csv_data = []
        with open('webpage_text_size.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if minimum <= i + 1 <= maximum:  # 注意索引从1开始，所以要加1
                    csv_data.append(row)
                elif i + 1 > maximum:  # 超出最大值范围则退出循环
                    break
        return render_template('front_end.html', form=form, text=text, total_consumption=total_time,
                               csv_data=csv_data)
        # 这里可以将处理结果返回给前端
    return render_template('front_end.html', form=form, text=text, total_consumption=total_time, csv_data=csv_data)


if __name__ == '__main__':
    app.run()
