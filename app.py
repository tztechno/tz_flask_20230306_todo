from flask import Flask, render_template, request
from flask import redirect, url_for
from datetime import date
from sqlalchemy import Column, Integer, Date, String, create_engine, select, delete, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('sqlite:///static/todo_list.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class TodoItem(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    text = Column(String)

    def __repr__(self):
        return f'<TodoItem(id={self.id}, date={self.date}, text="{self.text}")>'

Base.metadata.create_all(engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # リクエストがPOSTの場合
        session = Session()
        todo_items = session.query(TodoItem).all()
        session.close()  # セッションをクローズ
        return render_template('index.html', todo_items=todo_items)
    else:
        # リクエストがGETの場合
        return render_template('index.html')

# engine.connect() を使用してエンジンに接続
with engine.connect() as conn:
    todo_items = conn.execute(select(TodoItem)).fetchall()
    print(todo_items)

@app.route('/insert', methods=['POST'])
def insert():
    date_str = request.form['date']
    text = request.form['text']
    print('run insert')
    try:
        year, month, day = map(int, date_str.split('-'))
        item_date = date(year, month, day)
    except ValueError:
        item_date = None
    if text and item_date:
        session = Session()
        item = TodoItem(date=item_date, text=text)
        session.add(item)
        session.commit()
    return index()

@app.route('/delete', methods=['POST'])
def delete_item():
    item_id = request.form['id']
    print('run delete')
    if item_id:
        session = Session()
        item = session.query(TodoItem).filter_by(id=item_id).first()
        if item:
            session.delete(item)
            session.commit()
    return index()

if __name__ == '__main__':
    app.run(debug=True)
