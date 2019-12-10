import telebot
from telebot import types

import constants
from messages import *
from markov import  generate_random_sentence

import pickle
import random
import os

print('STARTED')

bot = telebot.TeleBot(constants.token)

print('BOT INITIALIZED')

with open('./models/model_ord_2_15000.pkl','rb') as f:
    model = pickle.load(f)

@bot.message_handler(commands = ['start'])
def handle_command(message):
    bot.send_message(message.chat.id,START_MESSAGE)

@bot.message_handler(commands = ['help'])
def handle_command(message):
    bot.send_message(message.chat.id,HELP_MESSAGE)

@bot.message_handler(commands = ['joke'])
def handle_command(message):
    bot.send_message(message.chat.id,generate_random_sentence(model))

@bot.message_handler(commands = ['joke_normally'])
def handle_command(message):
    path_to_joke = random.choice(os.listdir('./jokes/'))
    with open('./jokes/' + path_to_joke,'rb') as f:
        joke = pickle.load(f)
    bot.send_message(message.chat.id,joke)

@bot.message_handler(commands = ['change_model'])
def handle_command(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('1', '2', '3', '4', '5', '6')
    markup.row('7', '8', '9', '10', '11', '12')
    markup.row('13', '14', '15', '16', '17', '18')
    bot.send_message(message.chat.id,'Input number from 1 to 18', reply_markup=markup)
    bot.register_next_step_handler(message, change_model)

def change_model(message):
    global model
    window_size = message.text
    with open('./models/model_ord_{}_15000.pkl'.format(window_size),'rb') as f:
        model = pickle.load(f)
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,'Model changed', reply_markup=remove_markup)

while(True):
    try:
        if __name__ == "__main__":
            bot.polling(none_stop=True,interval=0)
    except:
        pass
