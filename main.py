#!/usr/bin/python
# -*- coding: utf-8 -*-

#****** Made by S.F based on Pablo - 2019******#

import settings

import codecs
import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqttPublish
if settings.USE_LEDS:
	import pixels
import sys
from threading import Timer
import time

import logging

logging.basicConfig(
	format='%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s',
	level=logging.INFO,
	filename='homielogs.log',
	filemode='w'
)

OPEN_GAME 			= 'hermes/intent/MagicBoxEi2i:Ouvrejeu'
GET_LETTER			= 'hermes/intent/MagicBoxEi2i:quelleLettre'

HERMES_ON_HOTWORD 		= 'hermes/hotword/default/detected'
HERMES_START_LISTENING 		= 'hermes/asr/startListening'
HERMES_SAY 			= 'hermes/tts/say'
HERMES_CAPTURED 		= 'hermes/asr/textCaptured'
HERMES_HOTWORD_TOGGLE_ON 	= 'hermes/hotword/toggleOn'

def onConnect(client, userData, flags, rc):
	mqttClient.subscribe(OPEN_GAME)
	mqttClient.subscribe(GET_LETTER)

	mqttClient.subscribe(HERMES_ON_HOTWORD)
	mqttClient.subscribe(HERMES_START_LISTENING)
	mqttClient.subscribe(HERMES_SAY)
	mqttClient.subscribe(HERMES_CAPTURED)
	mqttClient.subscribe(HERMES_HOTWORD_TOGGLE_ON)
	mqttPublish.single('hermes/feedback/sound/toggleOn', payload=json.dumps({'siteId': 'default'}), hostname='127.0.0.1', port=1883)

def onMessage(client, userData, message):
	global lang

	intent = message.topic

	if intent == HERMES_ON_HOTWORD:
		if settings.USE_LEDS:
			leds.wakeup()
		return

	elif intent == HERMES_SAY:
		if settings.USE_LEDS:
			leds.speak()
		return

	elif intent == HERMES_CAPTURED:
		if settings.USE_LEDS:
			leds.think()
		return

	elif intent == HERMES_START_LISTENING:
		if settings.USE_LEDS:
			leds.listen()
		return

	elif intent == HERMES_HOTWORD_TOGGLE_ON:
		if settings.USE_LEDS:
			leds.off()
		return

	global game, currentStep, timers, confirm, tofind

	payload = json.loads(message.payload)
	sessionId = payload['sessionId']

	if intent == OPEN_GAME:
		if 'slots' not in payload:
			error(sessionId)
			return

		slotGameName = payload['slots'][0]['value']['value'].encode('utf-8')


		if game is not None and currentStep > 0:
			if confirm <= 0:
				confirm = 1
				endTalk(sessionId, text=lang['warningGameAlreadyOpen'])
				return
			else:
				confirm = 0
				currentStep = 0

		if os.path.isfile('./games/{}/{}.json'.format(settings.LANG, slotGameName.lower())):
			endTalk(sessionId, text=lang['confirmOpening'].format(payload['slots'][0]['rawValue']))
			currentStep = 0

			file = codecs.open('./games/{}/{}.json'.format(settings.LANG, slotGameName.lower()), 'r', encoding='utf-8')
			string = file.read()
			file.close()
			game = json.loads(string)

			time.sleep(2)

			gameName = game['name'] if 'phonetic' not in game else game['phonetic']
			
			currentStep = 1

			say(text=lang['gamePresentation'].format(
				gameName,
				game['difficulty'],
				game['consigne']
			))
			if gameName == 'VisioBebe':
				cmd = 'sudo motion'
				os.system(cmd)
		else:
			endTalk(sessionId, text=lang['gameNotFound'])

	elif intent == GET_LETTER:
		if game is None:
			endTalk(sessionId, text=lang['sorryNoGameOpen'])

		else:
			if game is not None:
				endTalk(sessionId, text=lang['nextStep'].format(
				game['steps'][str(currentStep)]))
				currentStep +=1
				slotLetter = payload['slot'].encode('utf-8')
                                letter1 = 'h'
                        if slotLetter == 'h':
                                 endTalk(sessionId, text=lang['debug'])

def error(sessionId):
	endTalk(sessionId, lang['error'])

def endTalk(sessionId, text):
	mqttClient.publish('hermes/dialogueManager/endSession', json.dumps({
		'sessionId': sessionId,
		'text': text
	}))

def say(text):
	mqttClient.publish('hermes/dialogueManager/startSession', json.dumps({
		'init': {
			'type': 'notification',
			'text': text
		}
	}))

def onTimeUp(*args, **kwargs):
	global timers
	wasStep = args[0]
	step = args[1]
	del timers[wasStep]
	say(text=lang['timerEnd'].format(step['textAfterTimer']))


mqttClient = None
leds = None
running = True
game = None
currentStep = 0
timers = {}
confirm = 0
lang = ''
tofind = 'homie'

logger = logging.getLogger('homiebox')
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
	logger.info('******HOMIE BOX******')

	if settings.USE_LEDS:
		leds = pixels.Pixels()
		leds.off()

	try:
		file = codecs.open('./languages/{}.json'.format(settings.LANG), 'r', encoding='utf-8')
		string = file.read()
		file.close()
		lang = json.loads(string)
	except:
		logger.error('Error loading language file, exiting')
		sys.exit(0)

	mqttClient = mqtt.Client()
	mqttClient.on_connect = onConnect
	mqttClient.on_message = onMessage
	mqttClient.connect('localhost', 1883)
	logger.info(lang['appReady'])
	mqttClient.loop_start()
	try:
		while running:
			time.sleep(0.1)
	except KeyboardInterrupt:
		mqttClient.loop_stop()
		mqttClient.disconnect()
		running = False
	finally:
		logger.info(lang['stopping'])
