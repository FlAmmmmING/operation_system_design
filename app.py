from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField
from wtforms.validators import NumberRange
import make_figure_duration
import make_figure_start_end_time
from multi_Spider import data_1000_n1_10_n2_10_number

app = Flask(__name__)
app.config['SECRET_KEY'] = '823725'


class URLForm(FlaskForm):
    url = TextAreaField('URL')
    text_number = IntegerField('文本分割数量', validators=[NumberRange(min=5, max=100)])
    url_queue_number = IntegerField('爬虫通道数量', validators=[NumberRange(min=3, max=10)])
    data_queue_number = IntegerField('解析通道数量', validators=[NumberRange(min=3, max=10)])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def front_end():
    form = URLForm()
    if form.validate_on_submit():
        # 在这里处理提交的表单数据，比如打印或者处理URL
        url_set = form.url.data
        # print(url_set)
        data_1000_n1_10_n2_10_number(1)
        make_figure_duration.figure()
        make_figure_start_end_time.figure()
        # print("Submitted URL:", url)
        # 这里可以将处理结果返回给前端
    return render_template('front_end.html', form=form)


if __name__ == '__main__':
    app.run()
