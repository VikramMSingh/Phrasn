from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sys
import os, base64
from app import *
from config import Config
from flask_wtf import *
from forms import *
from models import *
from utils.helperCreateEmbedding import *
from dotenv import load_dotenv
import google.generativeai as genai
#from google.cloud import translate_v2
import google.cloud.translate_v2 as translate
import vertexai
from vertexai.preview import tokenization
from google.cloud import aiplatform

genai.configure(api_key=app.config['KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")
#translate_client = translate.Client()

@app.route('/')
def index():
    if 'token' in session:
        google.token = session['token']
        print(google.token)
        try:
            me = google.token.get('userinfo')
            return redirect(url_for('high_bandwidth_chat'))
        except Exception as e:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    nonce = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
    session['nonce'] = nonce
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)    

@app.route('/callback')
def authorized():
    token = oauth.google.authorize_access_token()
    if token is None:
        return f'Access Denied {args.reason} {args.description}'
    nonce = session.pop('nonce', None)
    if not nonce:
        return "Error: Nonce not found in session", 400
    user_info = oauth.google.parse_id_token(token,nonce)
    email = user_info['email']
    name = user_info['name']
    user = User.query.filter_by(email=email).first()
    
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    session['token'] = token
    return redirect(url_for('select_options'))


@app.route('/select_options', methods=['GET','POST'])
def select_options():
    form = LanguageStdForm()
    if form.validate_on_submit():
        language = form.lang.data
        standard = form.std.data
        user = User.query.get(session['user_id'])
        user.language = language
        user.standard = standard
        db.session.commit()
        session['lang'] = user.language
        print(session['lang'])
        return redirect(url_for('high_bandwidth_chat'))
    return render_template('lang_select.html',form=form)



@app.route('/process_chat', methods=['POST'])
def process_chat():
    user = User.query.get(session['user_id'])
    subjects = ['Mathematics','Physics','Chemistry','Biology','History']
    data = request.json
    question = data['question']
    subject = data['subject']
    print(user.language)
    l = lang_mapping(user.language)
    # Translate question to English
    if user.language != 'en':
        translated_question = str(generate_answer(f'Translate {question} to english', model, max_tokens=1000))
        #translated_question = translate_client.translate(question, target_language='en')['translatedText']
    else:
        translated_question = str(question)

    # Get context from Vertex AI
    if subject in subjects:
        context = get_context_from_vertex_ai(subject, translated_question)
        #context = f"{subject}"
        logger.info(f"Context for {subject}")
    print(context)

    prompt_en = generate_prompt(translated_question, context, subject, l)
    # Generate answer
    answer = generate_answer(prompt_en, model, max_tokens=1000)

    # Translate answer back to user's language
    #answer = answer_en
    # Save to database
    
    chat_history = ChatHistory(user_id=user.id, question=question, answer=answer)
    db.session.add(chat_history)
    db.session.commit()
    print(answer)
    return jsonify({'answer': answer})


@app.route('/high_bandwidth_chat', methods=['GET', 'POST'])
def high_bandwidth_chat():
    user = User.query.get(session['user_id'])
    subjects = ['Mathematics','Physics','Chemistry','Biology','History']
    greeting = f'Hello {user.name}! Please select a subject:'

    return render_template('advanced_chat.html', 
                           greeting=greeting, 
                           subjects=subjects,
                           user_language=user.language)

@app.route('/chat_history')
def chat_history():
    user = User.query.get(session['user_id'])
    history = ChatHistory.query.filter_by(user_id=user.id).order_by(ChatHistory.id.desc()).limit(10).all()
    chat_history = [{'id': chat.id, 'question': chat.question, 'answer': chat.answer} for chat in history]
    return jsonify(chat_history)
    #return render_template('chat_history.html', history=history, chat_history=chat_history)

@app.route('/replay_session', methods=['POST'])
def replay_session():
    data = request.json
    question = data['question']
    history_item = ChatHistory.query.filter_by(user_id=session['user_id'], question=question).first()
    if history_item:
        return jsonify({'answer': history_item.answer})
    return jsonify({'error': 'Session not found'}), 404

@app.route('/logout')
def logout():
    session.pop('token')
    return redirect(url_for('index'))

